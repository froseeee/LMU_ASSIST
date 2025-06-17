import time
from collections import deque
from typing import Dict, List, Any, Optional
import statistics
import logging

class TelemetryBuffer:
    """Буфер для накопления и анализа телеметрических данных"""
    
    def __init__(self, max_size=1000, lap_detection_threshold=0.95):
        self.max_size = max_size
        self.lap_detection_threshold = lap_detection_threshold
        
        # Основные буферы данных
        self.data_buffer = deque(maxlen=max_size)
        self.lap_data = []  # Данные текущего круга
        self.completed_laps = []  # Завершенные круги
        
        # Буферы для конкретных параметров
        self.rpm_history = deque(maxlen=max_size)
        self.speed_history = deque(maxlen=max_size)
        self.throttle_history = deque(maxlen=max_size)
        self.brake_history = deque(maxlen=max_size)
        self.steering_history = deque(maxlen=max_size)
        
        # Состояние для детекции кругов
        self.last_lap_completion = 0.0
        self.current_lap_progress = 0.0
        self.lap_start_time = time.time()
        
        self.logger = logging.getLogger(__name__)
    
    def add_data(self, telemetry_data: Dict[str, Any]):
        """Добавление новых телеметрических данных"""
        try:
            # Добавляем временную метку
            telemetry_data['timestamp'] = time.time()
            
            # Добавляем в основной буфер
            self.data_buffer.append(telemetry_data.copy())
            
            # Добавляем в специализированные буферы
            self._update_parameter_buffers(telemetry_data)
            
            # Проверяем завершение круга
            self._check_lap_completion(telemetry_data)
            
            # Добавляем в данные текущего круга
            self.lap_data.append(telemetry_data.copy())
            
        except Exception as e:
            self.logger.error(f"Error adding telemetry data: {e}")
    
    def _update_parameter_buffers(self, data: Dict[str, Any]):
        """Обновление буферов для отдельных параметров"""
        self.rpm_history.append(data.get('rpm', 0))
        self.speed_history.append(data.get('speed', 0))
        self.throttle_history.append(data.get('throttle', 0))
        self.brake_history.append(data.get('brake', 0))
        self.steering_history.append(data.get('steering', 0))
    
    def _check_lap_completion(self, data: Dict[str, Any]):
        """Детекция завершения круга"""
        lap_progress = data.get('lap_completion', 0.0)
        
        # Детекция пересечения финишной прямой
        if (self.current_lap_progress > self.lap_detection_threshold and 
            lap_progress < 0.1 and 
            len(self.lap_data) > 10):  # Минимум данных для валидного круга
            
            self._complete_lap()
        
        self.current_lap_progress = lap_progress
    
    def _complete_lap(self):
        """Завершение текущего круга и начало нового"""
        if not self.lap_data:
            return
        
        lap_time = time.time() - self.lap_start_time
        
        # Анализ завершенного круга
        lap_analysis = self._analyze_lap(self.lap_data, lap_time)
        
        self.completed_laps.append({
            'data': self.lap_data.copy(),
            'analysis': lap_analysis,
            'lap_time': lap_time,
            'timestamp': time.time()
        })
        
        self.logger.info(f"Lap completed: {lap_time:.3f}s")
        
        # Начинаем новый круг
        self.lap_data.clear()
        self.lap_start_time = time.time()
        
        # Ограничиваем количество сохраненных кругов
        if len(self.completed_laps) > 50:
            self.completed_laps.pop(0)
    
    def _analyze_lap(self, lap_data: List[Dict], lap_time: float) -> Dict[str, Any]:
        """Анализ завершенного круга"""
        if not lap_data:
            return {}
        
        try:
            # Извлекаем данные для анализа
            rpm_values = [d.get('rpm', 0) for d in lap_data]
            speed_values = [d.get('speed', 0) for d in lap_data]
            throttle_values = [d.get('throttle', 0) for d in lap_data]
            brake_values = [d.get('brake', 0) for d in lap_data]
            steering_values = [d.get('steering', 0) for d in lap_data]
            
            # Фильтруем нулевые значения для корректного анализа
            rpm_values = [v for v in rpm_values if v > 0]
            speed_values = [v for v in speed_values if v > 0]
            
            analysis = {
                'lap_time': lap_time,
                'avg_speed': statistics.mean(speed_values) if speed_values else 0,
                'max_speed': max(speed_values) if speed_values else 0,
                'avg_rpm': statistics.mean(rpm_values) if rpm_values else 0,
                'max_rpm': max(rpm_values) if rpm_values else 0,
                'brake_avg': statistics.mean(brake_values) if brake_values else 0,
                'throttle_avg': statistics.mean(throttle_values) if throttle_values else 0,
                'steering_smoothness': self._calculate_steering_smoothness(steering_values),
                'throttle_exit': self._calculate_throttle_exit_performance(throttle_values),
                'braking_consistency': self._calculate_braking_consistency(brake_values)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing lap: {e}")
            return {}
    
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
            
        except Exception:
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
            
        except Exception:
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
            
        except Exception:
            return 1.0
    
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
        
        return min(self.completed_laps, 
                  key=lambda lap: lap['lap_time'])
    
    def get_recent_data(self, seconds: float = 10.0) -> List[Dict[str, Any]]:
        """Получение данных за последние N секунд"""
        current_time = time.time()
        cutoff_time = current_time - seconds
        
        return [data for data in self.data_buffer 
                if data.get('timestamp', 0) >= cutoff_time]
    
    def get_parameter_history(self, parameter: str, count: int = 100) -> List[float]:
        """Получение истории конкретного параметра"""
        history_map = {
            'rpm': self.rpm_history,
            'speed': self.speed_history,
            'throttle': self.throttle_history,
            'brake': self.brake_history,
            'steering': self.steering_history
        }
        
        history = history_map.get(parameter, deque())
        return list(history)[-count:]
    
    def clear_data(self):
        """Очистка всех данных"""
        self.data_buffer.clear()
        self.lap_data.clear()
        self.completed_laps.clear()
        self.rpm_history.clear()
        self.speed_history.clear()
        self.throttle_history.clear()
        self.brake_history.clear()
        self.steering_history.clear()
        
        self.lap_start_time = time.time()
        self.logger.info("Telemetry buffer cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение общей статистики"""
        return {
            'total_data_points': len(self.data_buffer),
            'completed_laps': len(self.completed_laps),
            'current_lap_duration': time.time() - self.lap_start_time,
            'current_lap_data_points': len(self.lap_data),
            'buffer_usage': len(self.data_buffer) / self.max_size
        }
