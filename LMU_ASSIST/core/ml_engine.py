# core/ml_engine.py
"""
Machine Learning движок для оптимизации настроек автомобиля
Использует данные телеметрии и результатов для обучения оптимальных настроек
"""

import numpy as np
import pandas as pd
import pickle
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

@dataclass
class MLPrediction:
    """Результат ML предсказания"""
    predicted_setup: Dict[str, float]
    confidence: float
    expected_improvement: float
    reasoning: List[str]
    alternative_setups: List[Dict[str, float]]

@dataclass
class TrainingData:
    """Данные для обучения ML модели"""
    setup_parameters: Dict[str, float]
    track_conditions: Dict[str, Any]
    car_model: str
    driver_metrics: Dict[str, float]
    lap_time: float
    sector_times: List[float]
    consistency_score: float

class MLSetupOptimizer:
    """ML оптимизатор настроек автомобиля"""
    
    def __init__(self, model_path: str = "models/setup_optimizer.pkl", database=None):
        self.model_path = Path(model_path)
        self.database = database
        self.logger = logging.getLogger(__name__)
        
        # ML модели
        self.models = {
            'lap_time': RandomForestRegressor(n_estimators=100, random_state=42),
            'consistency': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'sector_performance': MLPRegressor(hidden_layer_sizes=(100, 50), random_state=42)
        }
        
        # Предобработчики
        self.scalers = {}
        self.encoders = {}
        
        # Обучающие данные
        self.training_data = []
        self.is_trained = False
        
        # Создаем директорию для моделей
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Загружаем существующую модель или создаем новую
        self.load_model()
    
    def load_model(self):
        """Загружает сохраненную модель"""
        try:
            if self.model_path.exists():
                with open(self.model_path, 'rb') as f:
                    saved_data = pickle.load(f)
                
                self.models = saved_data.get('models', self.models)
                self.scalers = saved_data.get('scalers', {})
                self.encoders = saved_data.get('encoders', {})
                self.training_data = saved_data.get('training_data', [])
                self.is_trained = saved_data.get('is_trained', False)
                
                self.logger.info(f"ML model loaded from {self.model_path}")
            else:
                self.logger.info("No existing model found, will train from scratch")
                
        except Exception as e:
            self.logger.error(f"Error loading ML model: {e}")
            self.logger.info("Starting with fresh model")
    
    def save_model(self):
        """Сохраняет обученную модель"""
        try:
            save_data = {
                'models': self.models,
                'scalers': self.scalers,
                'encoders': self.encoders,
                'training_data': self.training_data,
                'is_trained': self.is_trained
            }
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(save_data, f)
            
            self.logger.info(f"ML model saved to {self.model_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving ML model: {e}")
    
    def add_training_data(self, data: TrainingData):
        """Добавляет новые данные для обучения"""
        self.training_data.append(data)
        
        # Переобучаем модель каждые 50 новых записей
        if len(self.training_data) % 50 == 0:
            self.train_models()
    
    def prepare_features(self, setup_params: Dict, track_conditions: Dict, 
                        car_model: str, driver_metrics: Dict) -> np.ndarray:
        """Подготавливает признаки для ML модели"""
        features = {}
        
        # Параметры настройки
        setup_features = {
            'front_wing': setup_params.get('front_wing', 5),
            'rear_wing': setup_params.get('rear_wing', 5),
            'brake_bias': setup_params.get('brake_bias', 60),
            'tire_pressure_front': setup_params.get('tire_pressure_front', 25),
            'tire_pressure_rear': setup_params.get('tire_pressure_rear', 25),
            'front_spring': setup_params.get('front_spring', 50),
            'rear_spring': setup_params.get('rear_spring', 50),
            'differential_power': setup_params.get('differential_power', 50),
            'differential_coast': setup_params.get('differential_coast', 50)
        }
        features.update(setup_features)
        
        # Условия трассы
        track_features = {
            'temperature': track_conditions.get('temperature', 25),
            'track_length': track_conditions.get('track_length', 5.0),
            'weather_dry': 1 if track_conditions.get('weather', 'dry') == 'dry' else 0,
            'weather_rain': 1 if track_conditions.get('weather', 'dry') == 'rain' else 0,
            'track_type_fast': 1 if 'fast' in track_conditions.get('characteristics', []) else 0,
            'track_type_technical': 1 if 'technical' in track_conditions.get('characteristics', []) else 0
        }
        features.update(track_features)
        
        # Модель автомобиля (кодирование)
        car_features = {
            'car_hypercar': 1 if 'hypercar' in car_model.lower() else 0,
            'car_lmp2': 1 if 'lmp2' in car_model.lower() else 0,
            'car_lmgt3': 1 if 'lmgt3' in car_model.lower() else 0,
            'car_gte': 1 if 'gte' in car_model.lower() else 0
        }
        features.update(car_features)
        
        # Метрики водителя
        driver_features = {
            'brake_smoothness': driver_metrics.get('brake_smoothness', 0.8),
            'throttle_smoothness': driver_metrics.get('throttle_smoothness', 0.8),
            'steering_smoothness': driver_metrics.get('steering_smoothness', 0.8),
            'consistency': driver_metrics.get('consistency', 0.8),
            'aggression': driver_metrics.get('aggression', 0.5)
        }
        features.update(driver_features)
        
        return np.array(list(features.values()))
    
    def train_models(self):
        """Обучает ML модели на накопленных данных"""
        if len(self.training_data) < 10:
            self.logger.warning("Insufficient training data (need at least 10 samples)")
            return
        
        self.logger.info(f"Training ML models on {len(self.training_data)} samples")
        
        try:
            # Подготавливаем данные
            X = []
            y_lap_time = []
            y_consistency = []
            y_sector_avg = []
            
            for data in self.training_data:
                features = self.prepare_features(
                    data.setup_parameters,
                    data.track_conditions,
                    data.car_model,
                    data.driver_metrics
                )
                
                X.append(features)
                y_lap_time.append(data.lap_time)
                y_consistency.append(data.consistency_score)
                y_sector_avg.append(np.mean(data.sector_times) if data.sector_times else data.lap_time)
            
            X = np.array(X)
            y_lap_time = np.array(y_lap_time)
            y_consistency = np.array(y_consistency)
            y_sector_avg = np.array(y_sector_avg)
            
            # Нормализация данных
            if 'features' not in self.scalers:
                self.scalers['features'] = StandardScaler()
                X_scaled = self.scalers['features'].fit_transform(X)
            else:
                X_scaled = self.scalers['features'].transform(X)
            
            # Обучаем модели
            self.models['lap_time'].fit(X_scaled, y_lap_time)
            self.models['consistency'].fit(X_scaled, y_consistency)
            self.models['sector_performance'].fit(X_scaled, y_sector_avg)
            
            # Оцениваем качество моделей
            lap_time_score = cross_val_score(self.models['lap_time'], X_scaled, y_lap_time, cv=3, scoring='r2')
            consistency_score = cross_val_score(self.models['consistency'], X_scaled, y_consistency, cv=3, scoring='r2')
            
            self.is_trained = True
            
            self.logger.info(f"Model training completed:")
            self.logger.info(f"  Lap time R²: {lap_time_score.mean():.3f} ± {lap_time_score.std():.3f}")
            self.logger.info(f"  Consistency R²: {consistency_score.mean():.3f} ± {consistency_score.std():.3f}")
            
            # Сохраняем модель
            self.save_model()
            
        except Exception as e:
            self.logger.error(f"Error during model training: {e}")
    
    def predict_optimal_setup(self, track_conditions: Dict, driver_style: Dict, 
                            car_model: str, current_setup: Dict = None) -> MLPrediction:
        """Предсказывает оптимальные настройки"""
        if not self.is_trained:
            return self._fallback_prediction(track_conditions, driver_style, car_model)
        
        try:
            # Если нет текущих настроек, используем базовые
            if current_setup is None:
                current_setup = self._get_baseline_setup(car_model)
            
            # Генерируем кандидатов настроек
            setup_candidates = self._generate_setup_candidates(current_setup, car_model)
            
            best_setup = None
            best_score = float('inf')
            all_predictions = []
            
            for candidate in setup_candidates:
                features = self.prepare_features(candidate, track_conditions, car_model, driver_style)
                
                if 'features' in self.scalers:
                    features_scaled = self.scalers['features'].transform([features])
                    
                    # Предсказываем производительность
                    predicted_lap_time = self.models['lap_time'].predict(features_scaled)[0]
                    predicted_consistency = self.models['consistency'].predict(features_scaled)[0]
                    
                    # Комбинированная оценка (время + консистентность)
                    combined_score = predicted_lap_time - (predicted_consistency * 0.5)
                    
                    all_predictions.append({
                        'setup': candidate,
                        'lap_time': predicted_lap_time,
                        'consistency': predicted_consistency,
                        'score': combined_score
                    })
                    
                    if combined_score < best_score:
                        best_score = combined_score
                        best_setup = candidate
            
            if best_setup is None:
                return self._fallback_prediction(track_conditions, driver_style, car_model)
            
            # Расчет уверенности на основе разброса предсказаний
            scores = [p['score'] for p in all_predictions]
            confidence = 1.0 - (np.std(scores) / np.mean(scores)) if np.mean(scores) > 0 else 0.5
            confidence = max(0.1, min(0.95, confidence))
            
            # Ожидаемое улучшение
            baseline_features = self.prepare_features(current_setup, track_conditions, car_model, driver_style)
            if 'features' in self.scalers:
                baseline_scaled = self.scalers['features'].transform([baseline_features])
                baseline_time = self.models['lap_time'].predict(baseline_scaled)[0]
                expected_improvement = max(0, baseline_time - all_predictions[0]['lap_time'])
            else:
                expected_improvement = 0.0
            
            # Генерируем объяснения
            reasoning = self._generate_reasoning(best_setup, current_setup, track_conditions)
            
            # Альтернативные настройки (топ-3)
            sorted_predictions = sorted(all_predictions, key=lambda x: x['score'])
            alternatives = [p['setup'] for p in sorted_predictions[1:4]]
            
            return MLPrediction(
                predicted_setup=best_setup,
                confidence=confidence,
                expected_improvement=expected_improvement,
                reasoning=reasoning,
                alternative_setups=alternatives
            )
            
        except Exception as e:
            self.logger.error(f"Error in ML prediction: {e}")
            return self._fallback_prediction(track_conditions, driver_style, car_model)
    
    def _generate_setup_candidates(self, base_setup: Dict, car_model: str) -> List[Dict]:
        """Генерирует кандидатов настроек для тестирования"""
        candidates = [base_setup.copy()]
        
        # Параметры для варьирования
        variations = {
            'front_wing': [-2, -1, 0, 1, 2],
            'rear_wing': [-2, -1, 0, 1, 2],
            'brake_bias': [-3, -1.5, 0, 1.5, 3],
            'tire_pressure_front': [-1.5, -0.5, 0, 0.5, 1.5],
            'tire_pressure_rear': [-1.5, -0.5, 0, 0.5, 1.5]
        }
        
        # Генерируем варианты
        for param, changes in variations.items():
            for change in changes:
                if change != 0:
                    candidate = base_setup.copy()
                    if param in candidate:
                        candidate[param] += change
                        # Проверяем ограничения
                        candidate = self._validate_setup_limits(candidate, car_model)
                        candidates.append(candidate)
        
        # Комбинированные изменения
        for _ in range(20):  # 20 случайных комбинаций
            candidate = base_setup.copy()
            for param in variations.keys():
                if param in candidate and np.random.random() < 0.3:  # 30% шанс изменения
                    change = np.random.choice(variations[param])
                    candidate[param] += change
            
            candidate = self._validate_setup_limits(candidate, car_model)
            candidates.append(candidate)
        
        return candidates
    
    def _validate_setup_limits(self, setup: Dict, car_model: str) -> Dict:
        """Проверяет и корректирует настройки в пределах допустимых значений"""
        limits = {
            'front_wing': (1, 15),
            'rear_wing': (1, 15),
            'brake_bias': (50, 70),
            'tire_pressure_front': (20, 30),
            'tire_pressure_rear': (20, 30),
            'front_spring': (10, 100),
            'rear_spring': (10, 100),
            'differential_power': (10, 90),
            'differential_coast': (10, 90)
        }
        
        validated = setup.copy()
        for param, (min_val, max_val) in limits.items():
            if param in validated:
                validated[param] = max(min_val, min(max_val, validated[param]))
        
        return validated
    
    def _get_baseline_setup(self, car_model: str) -> Dict:
        """Возвращает базовые настройки для модели автомобиля"""
        baselines = {
            'hypercar': {
                'front_wing': 8, 'rear_wing': 8, 'brake_bias': 58,
                'tire_pressure_front': 24, 'tire_pressure_rear': 24,
                'front_spring': 60, 'rear_spring': 60,
                'differential_power': 40, 'differential_coast': 30
            },
            'lmp2': {
                'front_wing': 6, 'rear_wing': 6, 'brake_bias': 62,
                'tire_pressure_front': 25, 'tire_pressure_rear': 25,
                'front_spring': 55, 'rear_spring': 55,
                'differential_power': 45, 'differential_coast': 35
            },
            'lmgt3': {
                'front_wing': 4, 'rear_wing': 4, 'brake_bias': 60,
                'tire_pressure_front': 27, 'tire_pressure_rear': 27,
                'front_spring': 50, 'rear_spring': 50,
                'differential_power': 50, 'differential_coast': 40
            },
            'gte': {
                'front_wing': 5, 'rear_wing': 5, 'brake_bias': 62,
                'tire_pressure_front': 26, 'tire_pressure_rear': 26,
                'front_spring': 52, 'rear_spring': 52,
                'differential_power': 48, 'differential_coast': 38
            }
        }
        
        # Определяем тип автомобиля
        car_type = 'lmgt3'  # По умолчанию
        for car_class in baselines.keys():
            if car_class in car_model.lower():
                car_type = car_class
                break
        
        return baselines[car_type]
    
    def _generate_reasoning(self, recommended: Dict, current: Dict, conditions: Dict) -> List[str]:
        """Генерирует объяснения для рекомендаций"""
        reasoning = []
        
        # Анализируем основные изменения
        for param, new_value in recommended.items():
            if param in current:
                old_value = current[param]
                diff = new_value - old_value
                
                if abs(diff) > 0.5:  # Значимое изменение
                    if 'wing' in param:
                        if diff > 0:
                            reasoning.append(f"Increased {param.replace('_', ' ')} for better cornering grip")
                        else:
                            reasoning.append(f"Reduced {param.replace('_', ' ')} for higher top speed")
                    
                    elif 'brake_bias' in param:
                        if diff > 0:
                            reasoning.append("Forward brake bias for better turn-in")
                        else:
                            reasoning.append("Rearward brake bias for stability under braking")
                    
                    elif 'tire_pressure' in param:
                        if diff > 0:
                            reasoning.append(f"Higher tire pressure for reduced wear")
                        else:
                            reasoning.append(f"Lower tire pressure for better grip")
        
        # Анализируем условия
        temp = conditions.get('temperature', 25)
        if temp > 30:
            reasoning.append("Hot conditions: setup optimized for tire temperature management")
        elif temp < 15:
            reasoning.append("Cold conditions: setup optimized for tire warm-up")
        
        if not reasoning:
            reasoning.append("Minor adjustments for optimal performance")
        
        return reasoning
    
    def _fallback_prediction(self, track_conditions: Dict, driver_style: Dict, car_model: str) -> MLPrediction:
        """Fallback предсказание когда ML модель недоступна"""
        baseline = self._get_baseline_setup(car_model)
        
        # Простые эвристические корректировки
        adjustments = baseline.copy()
        
        # Температурные корректировки
        temp = track_conditions.get('temperature', 25)
        if temp > 30:
            adjustments['tire_pressure_front'] += 1.0
            adjustments['tire_pressure_rear'] += 1.0
        elif temp < 15:
            adjustments['tire_pressure_front'] -= 1.0
            adjustments['tire_pressure_rear'] -= 1.0
        
        # Корректировки по типу трассы
        characteristics = track_conditions.get('characteristics', [])
        if 'fast' in characteristics:
            adjustments['front_wing'] -= 1
            adjustments['rear_wing'] -= 1
        elif 'technical' in characteristics:
            adjustments['front_wing'] += 1
            adjustments['rear_wing'] += 1
        
        return MLPrediction(
            predicted_setup=adjustments,
            confidence=0.6,
            expected_improvement=0.2,
            reasoning=["Baseline recommendations with temperature and track adjustments"],
            alternative_setups=[baseline]
        )
    
    def get_training_stats(self) -> Dict:
        """Возвращает статистику обучения"""
        return {
            'total_samples': len(self.training_data),
            'is_trained': self.is_trained,
            'model_types': list(self.models.keys()),
            'last_training': getattr(self, 'last_training_time', None)
        }


class TelemetryPredictor:
    """Предиктор событий на основе телеметрии"""
    
    def __init__(self, model_path: str = "models/telemetry_predictor.pkl"):
        self.model_path = Path(model_path)
        self.logger = logging.getLogger(__name__)
        
        # Модели для разных предсказаний
        self.models = {
            'incident_risk': RandomForestRegressor(n_estimators=50, random_state=42),
            'tire_degradation': GradientBoostingRegressor(n_estimators=50, random_state=42),
            'fuel_consumption': RandomForestRegressor(n_estimators=50, random_state=42)
        }
        
        self.scalers = {}
        self.is_trained = False
        self.prediction_history = []
        
        self.load_model()
    
    def load_model(self):
        """Загружает модель предиктора"""
        try:
            if self.model_path.exists():
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                
                self.models = data.get('models', self.models)
                self.scalers = data.get('scalers', {})
                self.is_trained = data.get('is_trained', False)
                
                self.logger.info("Telemetry predictor model loaded")
        except Exception as e:
            self.logger.error(f"Error loading telemetry predictor: {e}")
    
    def save_model(self):
        """Сохраняет модель предиктора"""
        try:
            data = {
                'models': self.models,
                'scalers': self.scalers,
                'is_trained': self.is_trained
            }
            
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump(data, f)
                
        except Exception as e:
            self.logger.error(f"Error saving telemetry predictor: {e}")
    
    def predict_incident_risk(self, telemetry_window: List[Dict]) -> float:
        """Предсказывает риск инцидента на основе последних данных телеметрии"""
        if len(telemetry_window) < 5:
            return 0.0
        
        try:
            # Извлекаем признаки
            features = self._extract_risk_features(telemetry_window)
            
            if self.is_trained and 'risk_features' in self.scalers:
                features_scaled = self.scalers['risk_features'].transform([features])
                risk = self.models['incident_risk'].predict(features_scaled)[0]
                return max(0.0, min(1.0, risk))
            else:
                # Простая эвристика
                return self._simple_risk_calculation(telemetry_window)
                
        except Exception as e:
            self.logger.error(f"Error predicting incident risk: {e}")
            return 0.0
    
    def _extract_risk_features(self, telemetry_window: List[Dict]) -> List[float]:
        """Извлекает признаки для предсказания риска"""
        features = []
        
        # Статистики по скорости
        speeds = [d.get('speed', 0) for d in telemetry_window]
        features.extend([
            np.mean(speeds),
            np.std(speeds),
            max(speeds) - min(speeds)
        ])
        
        # Статистики по рулению
        steering = [abs(d.get('steering', 0)) for d in telemetry_window]
        features.extend([
            np.mean(steering),
            np.std(steering),
            max(steering)
        ])
        
        # Резкость торможения
        braking = [d.get('brake', 0) for d in telemetry_window]
        brake_changes = [abs(braking[i] - braking[i-1]) for i in range(1, len(braking))]
        features.extend([
            np.mean(braking),
            np.mean(brake_changes) if brake_changes else 0
        ])
        
        # Резкость газа
        throttle = [d.get('throttle', 0) for d in telemetry_window]
        throttle_changes = [abs(throttle[i] - throttle[i-1]) for i in range(1, len(throttle))]
        features.extend([
            np.mean(throttle),
            np.mean(throttle_changes) if throttle_changes else 0
        ])
        
        return features
    
    def _simple_risk_calculation(self, telemetry_window: List[Dict]) -> float:
        """Простой расчет риска без ML"""
        risk_factors = []
        
        for data in telemetry_window[-3:]:  # Последние 3 точки
            speed = data.get('speed', 0)
            steering = abs(data.get('steering', 0))
            brake = data.get('brake', 0)
            
            # Высокая скорость + резкое руление
            if speed > 150 and steering > 15:
                risk_factors.append(0.8)
            
            # Экстренное торможение на высокой скорости
            if speed > 120 and brake > 0.9:
                risk_factors.append(0.7)
            
            # Комбинация факторов
            combined_risk = (speed / 300) * (steering / 30) * (brake + 0.1)
            risk_factors.append(min(1.0, combined_risk))
        
        return np.mean(risk_factors) if risk_factors else 0.0
