import time
from collections import deque
from typing import Dict, List, Any, Optional
import statistics
import logging

from .constants import TelemetryConstants, ValidationConstants
from .exceptions import TelemetryDataError, ValidationError


class TelemetryBuffer:
    """Буфер для накопления и анализа телеметрических данных с улучшенной обработкой ошибок"""
    
    def __init__(self, max_size: int = None, lap_detection_threshold: float = None):
        self.max_size = max_size or TelemetryConstants.DEFAULT_BUFFER_SIZE
        self.lap_detection_threshold = lap_detection_threshold or TelemetryConstants.LAP_COMPLETION_THRESHOLD
        
        # Основные буферы данных
        self.data_buffer = deque(maxlen=self.max_size)
        self.lap_data = []  # Данные текущего круга
        self.completed_laps = []  # Завершенные круги
        
        # Буферы для конкретных параметров
        self.rpm_history = deque(maxlen=self.max_size)
        self.speed_history = deque(maxlen=self.max_size)
        self.throttle_history = deque(maxlen=self.max_size)
        self.brake_history = deque(maxlen=self.max_size)
        self.steering_history = deque(maxlen=self.max_size)
        
        # Состояние для детекции кругов
        self.last_lap_completion = 0.0
        self.current_lap_progress = 0.0
        self.lap_start_time = time.time()
        
        # Статистика
        self.total_data_points = 0
        self.invalid_data_points = 0
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Telemetry buffer initialized with max_size=%d", self.max_size)
    
    def add_data(self, telemetry_data: Dict[str, Any]) -> bool:
        """Добавление новых телеметрических данных с валидацией"""
        try:
            # Валидируем входные данные
            if not self._validate_telemetry_data(telemetry_data):
                self.invalid_data_points += 1
                return False
            
            # Добавляем временную метку если её нет
            if 'timestamp' not in telemetry_data:
                telemetry_data['timestamp'] = time.time()
            
            # Создаем копию данных для безопасности
            data_copy = telemetry_data.copy()
            
            # Добавляем в основной буфер
            self.data_buffer.append(data_copy)
            
            # Добавляем в специализированные буферы
            self._update_parameter_buffers(data_copy)
            
            # Проверяем завершение круга
            self._check_lap_completion(data_copy)
            
            # Добавляем в данные текущего круга
            self.lap_data.append(data_copy)
            
            self.total_data_points += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding telemetry data: {e}")
            self.invalid_data_points += 1
            return False
    
    def _validate_telemetry_data(self, data: Dict[str, Any]) -> bool:
        """Валидация телеметрических данных"""
        try:
            if not isinstance(data, dict):
                self.logger.warning("Telemetry data is not a dictionary")
                return False
            
            # Проверяем базовые поля
            required_fields = ['rpm', 'speed', 'gear']
            for field in required_fields:
                if field not in data:
                    self.logger.debug(f"Missing required field: {field}")
                    return False
            
            # Валидируем значения
            rpm = data.get('rpm', 0)
            if not isinstance(rpm, (int, float)) or not (ValidationConstants.MIN_RPM <= rpm <= ValidationConstants.MAX_RPM):
                self.logger.debug(f"Invalid RPM value: {rpm}")
                return False
            
            speed = data.get('speed', 0)
            if not isinstance(speed, (int, float)) or not (ValidationConstants.MIN_SPEED <= speed <= ValidationConstants.MAX_SPEED):
                self.logger.debug(f"Invalid speed value: {speed}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Error validating telemetry data: {e}")
            return False
    
    def _update_parameter_buffers(self, data: Dict[str, Any]):
        """Обновление буферов для отдельных параметров"""
        try:
            self.rpm_history.append(data.get('rpm', 0))
            self.speed_history.append(data.get('speed', 0))
            self.throttle_history.append(data.get('throttle', 0.0))
            self.brake_history.append(data.get('brake', 0.0))
            self.steering_history.append(data.get('steering', 0.0))
        except Exception as e:
            self.logger.warning(f"Error updating parameter buffers: {e}")
    
    def _check_lap_completion(self, data: Dict[str, Any]):
        """Детекция завершения круга"""
        try:
            lap_progress = data.get('lap_completion', data.get('lap_distance', 0.0))
            
            # Детекция пересечения финишной прямой
            if (self.current_lap_progress > self.lap_detection_threshold and 
                lap_progress < 0.1 and 
                len(self.lap_data) >= TelemetryConstants.MIN_LAP_DATA_POINTS):
                
                self._complete_lap()
            
            self.current_lap_progress = lap_progress
            
        except Exception as e:
            self.logger.warning(f"Error checking lap completion: {e}")
    
    def _complete_lap(self):
        """Завершение текущего круга и начало нового"""
        try:
            if not self.lap_data:
                return
            
            lap_time = time.time() - self.lap_start_time
            
            # Анализ завершенного круга
            lap_analysis = self._analyze_lap(self.lap_data, lap_time)
            
            completed_lap = {
                'data': self.lap_data.copy(),
                'analysis': lap_analysis,
                'lap_time': lap_time,
                'timestamp': time.time(),
                'lap_number': len(self.completed_laps) + 1
            }
            
            self.completed_laps.append(completed_lap)
            
            self.logger.info(f"Lap {completed_lap['lap_number']} completed: {lap_time:.3f}s")
            
            # Начинаем новый круг
            self.lap_data.clear()
            self.lap_start_time = time.time()
            
            # Ограничиваем количество сохраненных кругов
            max_laps = TelemetryConstants.DEFAULT_BUFFER_SIZE // 100  # Примерно 10 кругов
            if len(self.completed_laps) > max_laps:
                self.completed_laps.pop(0)
                
        except Exception as e:
            self.logger.error(f"Error completing lap: {e}")
    
    def _analyze_lap(self, lap_data: List[Dict], lap_time: float) -> Dict[str, Any]:
        """Анализ завершенного круга"""
        if not lap_data:
            return {}
        
        try:
            # Извлекаем данные для анализа
            rpm_values = [d.get('rpm', 0) for d in lap_data if d.get('rpm', 0) > 0]
            speed_values = [d.get('speed', 0) for d in lap_data if d.get('speed', 0) > 0]
            throttle_values = [d.get('throttle', 0) for d in lap_data]
            brake_values = [d.get('brake', 0) for d in lap_data]
            steering_values = [d.get('steering', 0) for d in lap_data]
            
            analysis = {
                'lap_time': lap_time,
                'data_points': len(lap_data),
                'avg_speed': statistics.mean(speed_values) if speed_values else 0,
                'max_speed': max(speed_values) if speed_values else 0,
                'avg_rpm': statistics.mean(rpm_values) if rpm_values else 0,
                'max_rpm': max(rpm_values) if rpm_values else 0,
                'brake_avg': statistics.mean(brake_values) if brake_values else 0,
                'throttle_avg': statistics.mean(throttle_values) if throttle_values else 0,
                'steering_smoothness': self._calculate_steering_smoothness(steering_values),
                'throttle_exit': self._calculate_throttle_exit_performance(throttle_values),
                'braking_consistency': self._calculate_braking_consistency(brake_values),
                'is_valid': self._validate_lap(lap_data, lap_time)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing lap: {e}")
            return {'error': str(e)}
    
    def _calculate_steering_smoothness(self, steering_values: List[float]) -> float:
        """Расчет плавности рулежки"""
        if len(steering_values) < 2:
            return 1.0
        
        try:
            # Рассчитываем изменения угла поворота
            steering_changes = []
            for i in range(1, len(steering_values)):
                change = abs(steering_values[i] - steering_values[i-1])
                steering_changes.append(change)
            
            if not steering_changes:
                return 1.0
            
            # Чем меньше резких изменений, тем выше плавность
            avg_change = statistics.mean(steering_changes)
            max_change = max(steering_changes)
            
            # Нормализуем от 0 до 1 (1 = максимальная плавность)
            smoothness = max(0, 1 - (avg_change / max(max_change, 0.1)))
            return smoothness
            
        except Exception as e:
            self.logger.warning(f"Error calculating steering smoothness: {e}")
            return 1.0
    
    def _calculate_throttle_exit_performance(self, throttle_values: List[float]) -> float:
        """Расчет эффективности работы с газом на выходе из поворотов"""
        if len(throttle_values) < 10:
            return 0.0
        
        try:
            # Находим точки выхода из поворотов (резкое увеличение газа)
            exit_points = []
            for i in range(1, len(throttle_values) - 1):
                if (throttle_values[i-1] < 0.3 and 
                    throttle_values[i] > 0.5 and 
                    throttle_values[i+1] > throttle_values[i]):
                    exit_points.append(throttle_values[i])
            
            if not exit_points:
                return statistics.mean(throttle_values)
            
            return statistics.mean(exit_points)
            
        except Exception as e:
            self.logger.warning(f"Error calculating throttle exit performance: {e}")
            return 0.0
    
    def _calculate_braking_consistency(self, brake_values: List[float]) -> float:
        """Расчет постоянства торможения"""
        if not brake_values:
            return 1.0
        
        try:
            # Находим точки торможения
            braking_points = [v for v in brake_values if v > 0.1]
            
            if len(braking_points) < 2:
                return 1.0
            
            # Рассчитываем стандартное отклонение
            std_dev = statistics.stdev(braking_points)
            avg_brake = statistics.mean(braking_points)
            
            # Нормализуем (меньше отклонение = больше постоянство)
            consistency = max(0, 1 - (std_dev / max(avg_brake, 0.1)))
            return consistency
            
        except Exception as e:
            self.logger.warning(f"Error calculating braking consistency: {e}")
            return 1.0
    
    def _validate_lap(self, lap_data: List[Dict], lap_time: float) -> bool:
        """Валидация корректности круга"""
        try:
            # Минимальное количество данных
            if len(lap_data) < TelemetryConstants.MIN_LAP_DATA_POINTS:
                return False
            
            # Разумное время круга
            if not (ValidationConstants.MIN_LAP_TIME <= lap_time <= ValidationConstants.MAX_LAP_TIME):
                return False
            
            # Проверяем наличие движения
            speed_values = [d.get('speed', 0) for d in lap_data]
            max_speed = max(speed_values) if speed_values else 0
            
            if max_speed < 10:  # Минимальная скорость для валидного круга
                return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Error validating lap: {e}")
            return False
    
    def get_current_lap_data(self) -> List[Dict[str, Any]]:
        """Получение данных текущего круга"""
        return self.lap_data.copy()
    
    def get_completed_laps(self) -> List[Dict[str, Any]]:
        """Получение завершенных кругов"""
        return self.completed_laps.copy()
    
    def get_best_lap(self) -> Optional[Dict[str, Any]]:
        """Получение лучшего круга"""
        if not self.completed_laps:
            return None
        
        try:
            valid_laps = [lap for lap in self.completed_laps 
                         if lap.get('analysis', {}).get('is_valid', False)]
            
            if not valid_laps:
                return None
                
            return min(valid_laps, key=lambda lap: lap['lap_time'])
            
        except Exception as e:
            self.logger.error(f"Error getting best lap: {e}")
            return None
    
    def get_recent_data(self, seconds: float = 10.0) -> List[Dict[str, Any]]:
        """Получение данных за последние N секунд"""
        try:
            current_time = time.time()
            cutoff_time = current_time - seconds
            
            return [data for data in self.data_buffer 
                    if data.get('timestamp', 0) >= cutoff_time]
                    
        except Exception as e:
            self.logger.error(f"Error getting recent data: {e}")
            return []
    
    def get_parameter_history(self, parameter: str, count: int = 100) -> List[float]:
        """Получение истории конкретного параметра"""
        try:
            history_map = {
                'rpm': self.rpm_history,
                'speed': self.speed_history,
                'throttle': self.throttle_history,
                'brake': self.brake_history,
                'steering': self.steering_history
            }
            
            history = history_map.get(parameter)
            if history is None:
                self.logger.warning(f"Unknown parameter: {parameter}")
                return []
                
            return list(history)[-count:]
            
        except Exception as e:
            self.logger.error(f"Error getting parameter history: {e}")
            return []
    
    def clear_data(self):
        """Очистка всех данных"""
        try:
            self.data_buffer.clear()
            self.lap_data.clear()
            self.completed_laps.clear()
            self.rpm_history.clear()
            self.speed_history.clear()
            self.throttle_history.clear()
            self.brake_history.clear()
            self.steering_history.clear()
            
            self.lap_start_time = time.time()
            self.current_lap_progress = 0.0
            self.total_data_points = 0
            self.invalid_data_points = 0
            
            self.logger.info("Telemetry buffer cleared")
            
        except Exception as e:
            self.logger.error(f"Error clearing telemetry buffer: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение общей статистики"""
        try:
            current_time = time.time()
            
            return {
                'total_data_points': self.total_data_points,
                'invalid_data_points': self.invalid_data_points,
                'valid_data_rate': ((self.total_data_points - self.invalid_data_points) / 
                                  max(self.total_data_points, 1)) * 100,
                'buffer_size': len(self.data_buffer),
                'buffer_usage': len(self.data_buffer) / self.max_size * 100,
                'completed_laps': len(self.completed_laps),
                'current_lap_duration': current_time - self.lap_start_time,
                'current_lap_data_points': len(self.lap_data),
                'current_lap_progress': self.current_lap_progress * 100,
                'best_lap_time': self.get_best_lap_time()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {}
    
    def get_best_lap_time(self) -> Optional[float]:
        """Получение времени лучшего круга"""
        best_lap = self.get_best_lap()
        return best_lap['lap_time'] if best_lap else None
    
    def export_data(self, filename: str) -> bool:
        """Экспорт данных в файл"""
        try:
            import json
            
            export_data = {
                'metadata': {
                    'export_time': time.time(),
                    'total_laps': len(self.completed_laps),
                    'total_data_points': self.total_data_points
                },
                'completed_laps': self.completed_laps,
                'statistics': self.get_statistics()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            self.logger.info(f"Data exported to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting data: {e}")
            return False
