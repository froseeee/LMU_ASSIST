import socket
import json
import logging
from typing import Optional, Dict, Any
import threading
import queue
import time

class TelemetryReceiver:
    def __init__(self, port=20777, timeout=1.0):
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.is_running = False
        self.data_queue = queue.Queue()
        self.thread = None
        
        # Настройка логирования
        self.logger = logging.getLogger(__name__)
        
        self._setup_socket()
    
    def _setup_socket(self):
        """Настройка UDP сокета с обработкой ошибок"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(self.timeout)
            self.sock.bind(("0.0.0.0", self.port))
            self.logger.info(f"Telemetry receiver bound to port {self.port}")
            return True
        except socket.error as e:
            self.logger.error(f"Failed to bind socket: {e}")
            return False
    
    def start_listening(self):
        """Запуск прослушивания в отдельном потоке"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        self.logger.info("Started telemetry listening thread")
    
    def stop_listening(self):
        """Остановка прослушивания"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        if self.sock:
            self.sock.close()
        self.logger.info("Stopped telemetry receiver")
    
    def _listen_loop(self):
        """Основной цикл прослушивания"""
        consecutive_errors = 0
        max_consecutive_errors = 10
        
        while self.is_running:
            try:
                data, addr = self.sock.recvfrom(1024)
                telemetry_data = self._parse_telemetry(data)
                
                if telemetry_data:
                    # Добавляем в очередь без блокировки
                    try:
                        self.data_queue.put_nowait(telemetry_data)
                        consecutive_errors = 0  # Сброс счетчика ошибок
                    except queue.Full:
                        # Очищаем старые данные
                        try:
                            self.data_queue.get_nowait()
                            self.data_queue.put_nowait(telemetry_data)
                        except queue.Empty:
                            pass
                            
            except socket.timeout:
                # Таймаут - это нормально
                continue
            except socket.error as e:
                consecutive_errors += 1
                self.logger.warning(f"Socket error: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    self.logger.error("Too many consecutive errors, stopping")
                    break
                    
                time.sleep(0.1)  # Небольшая пауза при ошибках
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                consecutive_errors += 1
                
                if consecutive_errors >= max_consecutive_errors:
                    break
                    
                time.sleep(0.1)
    
    def _parse_telemetry(self, data):
        """Парсинг телеметрических данных с валидацией"""
        try:
            telemetry_data = json.loads(data.decode("utf-8"))
            
            # Базовая валидация структуры данных
            required_fields = ['gear', 'rpm', 'speed']
            if not all(field in telemetry_data for field in required_fields):
                self.logger.warning("Received incomplete telemetry data")
                return None
            
            # Валидация значений
            if not self._validate_telemetry_values(telemetry_data):
                return None
                
            return telemetry_data
            
        except json.JSONDecodeError as e:
            self.logger.warning(f"JSON decode error: {e}")
            return None
        except UnicodeDecodeError as e:
            self.logger.warning(f"Unicode decode error: {e}")
            return None
        except Exception as e:
            self.logger.warning(f"Parse error: {e}")
            return None
    
    def _validate_telemetry_values(self, data):
        """Валидация значений телеметрии"""
        try:
            # Проверка RPM
            rpm = data.get('rpm', 0)
            if not (0 <= rpm <= 20000):  # Разумные границы для RPM
                return False
            
            # Проверка скорости
            speed = data.get('speed', 0)
            if not (0 <= speed <= 500):  # км/ч
                return False
            
            # Проверка передачи
            gear = data.get('gear', 0)
            if not (-1 <= gear <= 8):  # R, N, 1-8
                return False
            
            return True
        except (TypeError, ValueError):
            return False
        except Exception:
            return False
    
    def get_latest_data(self):
        """Получение последних данных телеметрии"""
        try:
            return self.data_queue.get_nowait()
        except queue.Empty:
            return None
        except Exception:
            return None
    
    def is_connected(self):
        """Проверка состояния подключения"""
        return self.is_running and self.sock is not None
    
    def get_queue_size(self):
        """Размер очереди данных"""
        try:
            return self.data_queue.qsize()
        except Exception:
            return 0

    def listen(self):
        """Совместимость с оригинальным интерфейсом"""
        return self.get_latest_data()