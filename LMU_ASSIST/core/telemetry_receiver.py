import socket
import struct
import threading
import time
import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass

from .constants import TelemetryConstants, NetworkConstants, ValidationConstants
from .exceptions import TelemetryConnectionError, TelemetryDataError, TelemetryTimeoutError


@dataclass
class TelemetryData:
    """Структура данных телеметрии Le Mans Ultimate"""
    # Базовые данные
    timestamp: float
    lap_time: float
    lap_distance: float
    lap_completion: float
    
    # Движение
    speed: float  # км/ч
    rpm: float
    gear: int
    
    # Управление
    throttle: float  # 0.0 - 1.0
    brake: float     # 0.0 - 1.0
    steering: float  # -1.0 - 1.0 (градусы/45)
    
    # Позиция
    position_x: float
    position_y: float
    position_z: float
    
    # Физика
    velocity_x: float
    velocity_y: float
    velocity_z: float
    
    # Дополнительные данные
    fuel_level: float
    tire_temp_fl: float
    tire_temp_fr: float
    tire_temp_rl: float
    tire_temp_rr: float
    
    @classmethod
    def from_udp_data(cls, raw_data: bytes) -> 'TelemetryData':
        """Создание объекта из UDP данных"""
        # Простой парсинг UDP пакета LMU
        # Формат может отличаться в зависимости от версии игры
        try:
            if len(raw_data) < 200:  # Минимальный размер пакета
                raise TelemetryDataError("UDP packet too small")
            
            # Распаковываем основные поля (примерная структура)
            values = struct.unpack('<ffffffffiifffffffffffffffff', raw_data[:100])
            
            return cls(
                timestamp=time.time(),
                lap_time=values[0],
                lap_distance=values[1],
                lap_completion=values[2],
                speed=values[3],
                rpm=values[4],
                gear=values[5],
                throttle=max(0.0, min(1.0, values[6])),
                brake=max(0.0, min(1.0, values[7])),
                steering=max(-1.0, min(1.0, values[8])),
                position_x=values[9],
                position_y=values[10],
                position_z=values[11],
                velocity_x=values[12],
                velocity_y=values[13],
                velocity_z=values[14],
                fuel_level=values[15],
                tire_temp_fl=values[16],
                tire_temp_fr=values[17],
                tire_temp_rl=values[18],
                tire_temp_rr=values[19]
            )
            
        except (struct.error, IndexError) as e:
            raise TelemetryDataError(f"Failed to parse UDP data: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            'timestamp': self.timestamp,
            'lap_time': self.lap_time,
            'lap_distance': self.lap_distance,
            'lap_completion': self.lap_completion,
            'speed': self.speed,
            'rpm': self.rpm,
            'gear': self.gear,
            'throttle': self.throttle,
            'brake': self.brake,
            'steering': self.steering,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'position_z': self.position_z,
            'velocity_x': self.velocity_x,
            'velocity_y': self.velocity_y,
            'velocity_z': self.velocity_z,
            'fuel_level': self.fuel_level,
            'tire_temp_fl': self.tire_temp_fl,
            'tire_temp_fr': self.tire_temp_fr,
            'tire_temp_rl': self.tire_temp_rl,
            'tire_temp_rr': self.tire_temp_rr
        }


class TelemetryReceiver:
    """UDP приемник телеметрии для Le Mans Ultimate"""
    
    def __init__(self, port: int = None, timeout: float = None):
        self.port = port or TelemetryConstants.DEFAULT_PORT
        self.timeout = timeout or TelemetryConstants.DEFAULT_TIMEOUT
        
        self.logger = logging.getLogger(__name__)
        
        # Состояние соединения
        self.socket = None
        self.is_listening = False
        self.is_connected = False
        
        # Буферы данных
        self.latest_data = None
        self.data_history = []
        
        # Потоки
        self.listen_thread = None
        self._stop_event = threading.Event()
        
        # Колбэки
        self.data_callbacks: List[Callable[[Dict], None]] = []
        
        # Статистика
        self.packets_received = 0
        self.packets_invalid = 0
        self.connection_errors = 0
        self.last_packet_time = 0
        
        self.logger.info(f"Telemetry receiver initialized on port {self.port}")
    
    def add_data_callback(self, callback: Callable[[Dict], None]):
        """Добавление колбэка для обработки данных"""
        self.data_callbacks.append(callback)
    
    def remove_data_callback(self, callback: Callable[[Dict], None]):
        """Удаление колбэка"""
        if callback in self.data_callbacks:
            self.data_callbacks.remove(callback)
    
    def start_listening(self) -> bool:
        """Запуск прослушивания UDP"""
        if self.is_listening:
            self.logger.warning("Already listening")
            return True
        
        try:
            self._create_socket()
            self._stop_event.clear()
            
            # Запускаем поток прослушивания
            self.listen_thread = threading.Thread(
                target=self._listen_loop,
                name="TelemetryReceiver",
                daemon=True
            )
            self.listen_thread.start()
            
            self.is_listening = True
            self.logger.info(f"Started listening on port {self.port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start listening: {e}")
            self._cleanup_socket()
            raise TelemetryConnectionError(f"Failed to bind to port {self.port}: {e}")
    
    def stop_listening(self):
        """Остановка прослушивания"""
        if not self.is_listening:
            return
        
        self.logger.info("Stopping telemetry receiver...")
        
        # Сигнализируем потоку остановиться
        self._stop_event.set()
        self.is_listening = False
        
        # Закрываем сокет
        self._cleanup_socket()
        
        # Ждем завершения потока
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2.0)
        
        self.logger.info("Telemetry receiver stopped")
    
    def _create_socket(self):
        """Создание UDP сокета"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(self.timeout)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Биндим к порту
            self.socket.bind((NetworkConstants.DEFAULT_BIND_ADDRESS, self.port))
            
            self.is_connected = True
            self.logger.debug(f"Socket bound to port {self.port}")
            
        except OSError as e:
            if e.errno == 10048:  # Address already in use
                raise TelemetryConnectionError(
                    f"Port {self.port} is already in use. "
                    f"Close other telemetry applications or change port."
                )
            else:
                raise TelemetryConnectionError(f"Failed to create socket: {e}")
    
    def _cleanup_socket(self):
        """Очистка сокета"""
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                self.logger.warning(f"Error closing socket: {e}")
            finally:
                self.socket = None
                self.is_connected = False
    
    def _listen_loop(self):
        """Основной цикл прослушивания"""
        self.logger.info("Telemetry listening loop started")
        consecutive_errors = 0
        
        while not self._stop_event.is_set() and self.is_listening:
            try:
                # Получаем UDP пакет
                data, addr = self.socket.recvfrom(NetworkConstants.UDP_BUFFER_SIZE)
                
                if data:
                    # Сбрасываем счетчик ошибок при успешном получении данных
                    consecutive_errors = 0
                    
                    # Обрабатываем данные
                    self._process_packet(data, addr)
                
            except socket.timeout:
                # Таймаут - это нормально, проверяем нужно ли останавливаться
                continue
                
            except Exception as e:
                consecutive_errors += 1
                self.connection_errors += 1
                
                self.logger.warning(f"Error receiving data: {e}")
                
                # Если слишком много ошибок подряд, останавливаемся
                if consecutive_errors >= NetworkConstants.MAX_CONSECUTIVE_ERRORS:
                    self.logger.error("Too many consecutive errors, stopping receiver")
                    break
                
                # Небольшая пауза перед повтором
                time.sleep(NetworkConstants.CONNECTION_RETRY_DELAY)
        
        self.logger.info("Telemetry listening loop ended")
    
    def _process_packet(self, data: bytes, addr: tuple):
        """Обработка полученного UDP пакета"""
        try:
            # Парсим данные телеметрии
            telemetry = TelemetryData.from_udp_data(data)
            
            # Валидируем данные
            if not self._validate_telemetry_data(telemetry):
                self.packets_invalid += 1
                return
            
            # Обновляем статистику
            self.packets_received += 1
            self.last_packet_time = time.time()
            
            # Сохраняем как последние данные
            telemetry_dict = telemetry.to_dict()
            self.latest_data = telemetry_dict
            
            # Добавляем в историю (ограниченный размер)
            self.data_history.append(telemetry_dict)
            if len(self.data_history) > TelemetryConstants.DEFAULT_BUFFER_SIZE:
                self.data_history.pop(0)
            
            # Вызываем колбэки
            self._notify_callbacks(telemetry_dict)
            
        except TelemetryDataError as e:
            self.packets_invalid += 1
            self.logger.debug(f"Invalid telemetry data: {e}")
            
        except Exception as e:
            self.packets_invalid += 1
            self.logger.warning(f"Error processing packet: {e}")
    
    def _validate_telemetry_data(self, telemetry: TelemetryData) -> bool:
        """Валидация данных телеметрии"""
        try:
            # Проверяем RPM
            if not (ValidationConstants.MIN_RPM <= telemetry.rpm <= ValidationConstants.MAX_RPM):
                return False
            
            # Проверяем скорость
            if not (ValidationConstants.MIN_SPEED <= telemetry.speed <= ValidationConstants.MAX_SPEED):
                return False
            
            # Проверяем передачу
            if not (-1 <= telemetry.gear <= 8):
                return False
            
            # Проверяем педали
            if not (0.0 <= telemetry.throttle <= 1.0):
                return False
            if not (0.0 <= telemetry.brake <= 1.0):
                return False
            
            # Проверяем руль
            if not (-1.0 <= telemetry.steering <= 1.0):
                return False
            
            return True
            
        except Exception as e:
            self.logger.debug(f"Validation error: {e}")
            return False
    
    def _notify_callbacks(self, data: Dict[str, Any]):
        """Уведомление колбэков о новых данных"""
        for callback in self.data_callbacks:
            try:
                callback(data)
            except Exception as e:
                self.logger.warning(f"Error in data callback: {e}")
    
    def get_latest_data(self) -> Optional[Dict[str, Any]]:
        """Получение последних данных телеметрии"""
        return self.latest_data.copy() if self.latest_data else None
    
    def get_data_history(self, count: int = 100) -> List[Dict[str, Any]]:
        """Получение истории данных"""
        return self.data_history[-count:] if self.data_history else []
    
    def is_receiving_data(self) -> bool:
        """Проверка получения данных"""
        if not self.last_packet_time:
            return False
        
        time_since_last = time.time() - self.last_packet_time
        return time_since_last < TelemetryConstants.CONNECTION_TIMEOUT
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Получение статуса соединения"""
        return {
            'is_listening': self.is_listening,
            'is_connected': self.is_connected,
            'is_receiving_data': self.is_receiving_data(),
            'port': self.port,
            'packets_received': self.packets_received,
            'packets_invalid': self.packets_invalid,
            'connection_errors': self.connection_errors,
            'last_packet_time': self.last_packet_time,
            'time_since_last_packet': time.time() - self.last_packet_time if self.last_packet_time else None
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики"""
        status = self.get_connection_status()
        
        total_packets = self.packets_received + self.packets_invalid
        valid_rate = (self.packets_received / total_packets * 100) if total_packets > 0 else 0
        
        status.update({
            'total_packets': total_packets,
            'valid_packet_rate': round(valid_rate, 2),
            'data_history_size': len(self.data_history),
            'has_latest_data': self.latest_data is not None
        })
        
        return status
    
    def reset_statistics(self):
        """Сброс статистики"""
        self.packets_received = 0
        self.packets_invalid = 0
        self.connection_errors = 0
    
    def __enter__(self):
        """Context manager entry"""
        self.start_listening()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_listening()


# Фабричная функция для создания приемника
def create_telemetry_receiver(config: Dict[str, Any] = None) -> TelemetryReceiver:
    """Создание приемника телеметрии с конфигурацией"""
    if config is None:
        config = {}
    
    port = config.get('udp_port', TelemetryConstants.DEFAULT_PORT)
    timeout = config.get('timeout', TelemetryConstants.DEFAULT_TIMEOUT)
    
    receiver = TelemetryReceiver(port=port, timeout=timeout)
    
    return receiver


# Простая функция для тестирования
def test_telemetry_receiver():
    """Тестирование приемника телеметрии"""
    print("Testing telemetry receiver...")
    
    def data_handler(data):
        print(f"Received: RPM={data.get('rpm', 0):.0f}, "
              f"Speed={data.get('speed', 0):.0f}, "
              f"Gear={data.get('gear', 0)}")
    
    try:
        with TelemetryReceiver() as receiver:
            receiver.add_data_callback(data_handler)
            print(f"Listening on port {receiver.port}...")
            print("Start Le Mans Ultimate with UDP telemetry enabled")
            print("Press Ctrl+C to stop")
            
            while True:
                time.sleep(1)
                status = receiver.get_connection_status()
                if status['is_receiving_data']:
                    print(f"Packets: {status['packets_received']}")
                
    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_telemetry_receiver()
