import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

class SetupExpert:
    """Экспертная система для оптимизации настроек автомобиля"""
    
    def __init__(self, data_file=None):
        self.logger = logging.getLogger(__name__)
        
        # Загружаем данные о машинах и трассах
        if data_file:
            self.data = self._load_data(data_file)
        else:
            self.data = self._get_default_data()
        
        # Базовые правила настройки для Le Mans Ultimate
        self.setup_rules = {
            "temperature": {
                "hot": {"tire_pressure": +1.5, "wing_adjustment": -1},
                "cold": {"tire_pressure": -1.0, "wing_adjustment": +1},
                "optimal": {"tire_pressure": 0, "wing_adjustment": 0},
                "extreme_hot": {"tire_pressure": +2.5, "wing_adjustment": -2}
            },
            "track_characteristics": {
                "very_fast": {"wing_level": "minimal", "suspension": "stiff", "brake_bias": -1},
                "fast": {"wing_level": "low", "suspension": "medium_stiff", "brake_bias": 0},
                "technical": {"wing_level": "high", "suspension": "soft", "brake_bias": +2},
                "mixed": {"wing_level": "medium", "suspension": "medium", "brake_bias": 0},
                "bumpy": {"suspension": "very_stiff", "brake_bias": +1},
                "elevation": {"suspension": "adaptive", "brake_bias": +1}
            },
            "weather": {
                "hot_dry": {"tire_pressure": +1.0, "wing_angle": -1, "brake_bias": +1},
                "tropical_variable": {"tire_pressure": +0.5, "wing_angle": +1, "brake_bias": 0},
                "changeable": {"tire_pressure": 0, "wing_angle": +1, "brake_bias": 0},
                "desert": {"tire_pressure": +2.0, "wing_angle": -2, "brake_bias": +2}
            },
            "car_category_specific": {
                "hypercar": {
                    "hybrid_optimization": True,
                    "fuel_efficiency_priority": True,
                    "aero_efficiency": "critical"
                },
                "lmp2": {
                    "power_fixed": True,
                    "setup_freedom": "limited",
                    "tire_management": "important"
                },
                "lmgt3": {
                    "balance_priority": True,
                    "durability_focus": True,
                    "bop_considerations": True
                },
                "gte": {
                    "power_curve_optimization": True,
                    "fuel_strategy": "important"
                }
            },
            "endurance_specific": {
                "stint_length": {
                    "short": {"aggressive_setup": True, "tire_pressure": -0.5},
                    "medium": {"balanced_setup": True, "tire_pressure": 0},
                    "long": {"conservative_setup": True, "tire_pressure": +0.5}
                },
                "race_duration": {
                    "6_hour": {"tire_degradation": "medium", "fuel_critical": False},
                    "24_hour": {"tire_degradation": "critical", "fuel_critical": True, "driver_comfort": True}
                }
            }
        }
    
    def _load_data(self, data_file: str) -> Dict[str, Any]:
        """Загрузка данных из файла"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading data file: {e}")
            return self._get_default_data()
    
    def _get_default_data(self) -> Dict[str, Any]:
        """Базовые данные по умолчанию для Le Mans Ultimate"""
        return {
            "cars": {
                "hypercar": {
                    "name": "Hypercar (LMH/LMDh)",
                    "category": "LMH/LMDh", 
                    "power": 680,
                    "weight": 1030,
                    "drivetrain": "AWD",
                    "hybrid_system": True,
                    "setup_ranges": {
                        "front_wing": [1, 15],
                        "rear_wing": [1, 15],
                        "brake_bias": [52, 68],
                        "tire_pressure": {"front": [22.0, 28.0], "rear": [22.0, 28.0]},
                        "hybrid_deployment": [0, 100]
                    }
                },
                "lmp2": {
                    "name": "LMP2 (ORECA 07 Gibson)",
                    "category": "LMP2",
                    "power": 600,
                    "weight": 950,
                    "drivetrain": "RWD",
                    "setup_ranges": {
                        "front_wing": [1, 12],
                        "rear_wing": [1, 12], 
                        "brake_bias": [54, 70],
                        "tire_pressure": {"front": [23.0, 29.0], "rear": [23.0, 29.0]}
                    }
                },
                "lmgt3_mclaren": {
                    "name": "McLaren 720S LMGT3 Evo",
                    "category": "LMGT3",
                    "power": 520,
                    "weight": 1300,
                    "drivetrain": "RWD",
                    "free_car": True,
                    "setup_ranges": {
                        "front_wing": [1, 8],
                        "rear_wing": [1, 8],
                        "brake_bias": [55, 66],
                        "tire_pressure": {"front": [25.0, 31.0], "rear": [25.0, 31.0]}
                    }
                },
                "gte_porsche": {
                    "name": "Porsche 911 RSR-19",
                    "category": "GTE",
                    "power": 520,
                    "weight": 1245,
                    "drivetrain": "RWD",
                    "setup_ranges": {
                        "front_wing": [1, 10],
                        "rear_wing": [1, 10],
                        "brake_bias": [57, 67],
                        "tire_pressure": {"front": [24.0, 30.0], "rear": [24.0, 30.0]}
                    }
                }
            },
            "tracks": {
                "le_mans": {
                    "name": "Circuit de la Sarthe",
                    "length": 13.626,
                    "characteristics": ["very_fast", "long_straights"],
                    "setup_recommendations": {
                        "aero": "minimum_downforce",
                        "suspension": "medium_stiff",
                        "brake_bias": "balanced"
                    }
                },
                "spa": {
                    "name": "Spa-Francorchamps",
                    "length": 7.004,
                    "characteristics": ["fast", "elevation"],
                    "setup_recommendations": {
                        "aero": "medium_downforce",
                        "suspension": "medium_stiff",
                        "brake_bias": "balanced"
                    }
                },
                "monza": {
                    "name": "Monza",
                    "length": 5.793,
                    "characteristics": ["very_fast", "low_downforce"],
                    "setup_recommendations": {
                        "aero": "minimum_downforce",
                        "suspension": "stiff",
                        "brake_bias": "forward_biased"
                    }
                }
            }
        }
    
    def recommend_setup(self, conditions: Dict[str, Any], telemetry: Dict[str, Any], 
                       car_type: str = "hypercar", track_name: str = "le_mans") -> Dict[str, Any]:
        """Генерация рекомендаций по настройке"""
        try:
            adjustments = {}
            explanations = []
            
            # Получаем данные о машине и трассе
            car_data = self.data.get("cars", {}).get(car_type, {})
            track_data = self.data.get("tracks", {}).get(track_name, {})
            
            # Анализ температурных условий
            temp_adjustments = self._analyze_temperature(conditions, explanations)
            adjustments.update(temp_adjustments)
            
            # Анализ характеристик трассы
            track_adjustments = self._analyze_track_specific_lmu(track_data, car_data, explanations)
            adjustments.update(track_adjustments)
            
            # Анализ факторов эндьюранса
            endurance_adjustments = self._analyze_endurance_factors(conditions, explanations)
            adjustments.update(endurance_adjustments)
            
            # Специальный анализ для гиперкаров
            if car_type == "hypercar":
                hypercar_adjustments = self._analyze_hypercar_specific(telemetry, explanations)
                adjustments.update(hypercar_adjustments)
            
            # Анализ погодных условий
            weather_adjustments = self._analyze_weather(conditions, explanations)
            adjustments.update(weather_adjustments)
            
            # Анализ телеметрии и стиля пилотирования
            telemetry_adjustments = self._analyze_telemetry(telemetry, explanations)
            adjustments.update(telemetry_adjustments)
            
            # Проверяем корректность настроек для данной машины
            validated_adjustments = self._validate_adjustments(adjustments, car_data)
            
            return {
                "adjustments": validated_adjustments,
                "explanations": explanations,
                "confidence": self._calculate_confidence(conditions, telemetry),
                "car_type": car_type,
                "track_name": track_name
            }
            
        except Exception as e:
            self.logger.error(f"Error generating setup recommendations: {e}")
            return {"adjustments": {}, "explanations": ["Ошибка при генерации рекомендаций"], "confidence": 0}
    
    def _analyze_temperature(self, conditions: Dict[str, Any], explanations: List[str]) -> Dict[str, Any]:
        """Анализ температурных условий для Le Mans Ultimate"""
        adjustments = {}
        temp = conditions.get("temperature", 25)
        track_name = conditions.get("track", "")
        
        if track_name in ["bahrain", "lusail"] and temp > 45:
            adjustments["tire_pressure_front"] = +2.5
            adjustments["tire_pressure_rear"] = +2.5
            adjustments["front_wing"] = -3
            adjustments["rear_wing"] = -3
            explanations.append(f"Экстремальная жара ({temp}°C) в пустыне: максимальные корректировки")
        elif temp > 35:
            adjustments["tire_pressure_front"] = +1.5
            adjustments["tire_pressure_rear"] = +1.5
            adjustments["front_wing"] = -2
            adjustments["rear_wing"] = -2
            explanations.append(f"Высокая температура ({temp}°C): увеличено давление, снижен прижим")
        elif temp < 15:
            adjustments["tire_pressure_front"] = -1.0
            adjustments["tire_pressure_rear"] = -1.0
            adjustments["front_wing"] = +1
            adjustments["rear_wing"] = +1
            explanations.append(f"Низкая температура ({temp}°C): снижено давление, увеличен прижим")
        else:
            explanations.append(f"Оптимальная температура ({temp}°C): базовые настройки")
        
        return adjustments
    
    def _analyze_track_specific_lmu(self, track_data: Dict[str, Any], car_data: Dict[str, Any], 
                                  explanations: List[str]) -> Dict[str, Any]:
        """Специальный анализ трасс Le Mans Ultimate"""
        adjustments = {}
        
        if not track_data:
            return adjustments
        
        track_name = track_data.get("name", "").lower()
        characteristics = track_data.get("characteristics", [])
        
        if "le_mans" in track_name or "sarthe" in track_name:
            adjustments["front_wing"] = -5
            adjustments["rear_wing"] = -5
            adjustments["differential_coast"] = -15
            explanations.append("Ле-Ман: минимальное сопротивление, эффективность на прямых")
        elif "sebring" in track_name:
            adjustments["front_spring"] = +30
            adjustments["rear_spring"] = +30
            adjustments["brake_bias"] = +2
            explanations.append("Sebring: жесткая подвеска для неровной поверхности")
        elif "portimao" in track_name or "algarve" in track_name:
            adjustments["front_spring"] = +10
            adjustments["rear_spring"] = +10
            explanations.append("Портимао: усиленная подвеска для холмов")
        elif "monza" in track_name:
            adjustments["front_wing"] = -4
            adjustments["rear_wing"] = -4
            explanations.append("Монца: минимальный прижим для максимальной скорости")
        
        return adjustments
    
    def _analyze_endurance_factors(self, conditions: Dict[str, Any], explanations: List[str]) -> Dict[str, Any]:
        """Анализ факторов эндьюранса"""
        adjustments = {}
        
        race_duration = conditions.get("race_duration", "6_hour")
        stint_strategy = conditions.get("stint_strategy", "medium")
        
        if race_duration == "24_hour":
            adjustments["tire_pressure_front"] = +0.5
            adjustments["tire_pressure_rear"] = +0.5
            adjustments["brake_bias"] = +1
            explanations.append("24-часовая гонка: консервативные настройки для надежности")
            
            if stint_strategy == "long":
                adjustments["tire_pressure_front"] += 0.5
                adjustments["tire_pressure_rear"] += 0.5
                explanations.append("Длинные стинты: дополнительное давление для износа шин")
        elif race_duration == "6_hour":
            if stint_strategy == "short":
                adjustments["tire_pressure_front"] = -0.5
                adjustments["tire_pressure_rear"] = -0.5
                explanations.append("6-часовая гонка, короткие стинты: агрессивные настройки")
        
        return adjustments
    
    def _analyze_hypercar_specific(self, telemetry: Dict[str, Any], explanations: List[str]) -> Dict[str, Any]:
        """Анализ специфичных для гиперкаров факторов"""
        adjustments = {}
        
        hybrid_efficiency = telemetry.get("hybrid_efficiency", 0.8)
        fuel_consumption = telemetry.get("fuel_consumption", 1.0)
        
        if hybrid_efficiency < 0.7:
            adjustments["hybrid_deployment"] = -10
            explanations.append("Низкая эффективность гибрида: снижен агрессивный режим")
        
        if fuel_consumption > 1.2:
            adjustments["front_wing"] = -1
            adjustments["rear_wing"] = -1
            explanations.append("Высокий расход топлива: снижен прижим для эффективности")
        
        return adjustments
    
    def _analyze_weather(self, conditions: Dict[str, Any], explanations: List[str]) -> Dict[str, Any]:
        """Анализ погодных условий"""
        adjustments = {}
        weather = conditions.get("weather", "dry")
        
        if weather == "light_rain":
            adjustments["tire_pressure_front"] = +2.0
            adjustments["tire_pressure_rear"] = +2.0
            adjustments["front_wing"] = +3
            adjustments["rear_wing"] = +3
            adjustments["brake_bias"] = -2
            explanations.append("Легкий дождь: увеличено давление и прижим, смещен тормозной баланс")
        elif weather == "heavy_rain":
            adjustments["tire_pressure_front"] = +4.0
            adjustments["tire_pressure_rear"] = +4.0
            adjustments["front_wing"] = +6
            adjustments["rear_wing"] = +6
            adjustments["brake_bias"] = -4
            explanations.append("Сильный дождь: максимальные корректировки для безопасности")
        
        return adjustments
    
    def _analyze_telemetry(self, telemetry: Dict[str, Any], explanations: List[str]) -> Dict[str, Any]:
        """Анализ телеметрии"""
        adjustments = {}
        
        # Анализ торможения
        brake_avg = telemetry.get("brake_avg", 0.5)
        brake_tendency = telemetry.get("brake_tendency", "normal")
        
        if brake_avg > 0.9 or brake_tendency == "aggressive":
            adjustments["brake_bias"] = +2
            adjustments["front_spring"] = +10
            explanations.append("Агрессивное торможение: усилен передний тормозной баланс")
        elif brake_tendency == "late":
            adjustments["brake_bias"] = -2
            explanations.append("Позднее торможение: смещен баланс назад для стабильности")
        
        # Анализ работы с газом
        throttle_exit = telemetry.get("throttle_exit", 0.8)
        if throttle_exit < 0.7:
            adjustments["differential_power"] = +10
            adjustments["rear_spring"] = +5
            explanations.append("Слабая работа с газом: усилен дифференциал на выходе")
        elif throttle_exit > 0.95:
            adjustments["differential_power"] = -5
            explanations.append("Агрессивная работа с газом: смягчен дифференциал")
        
        # Анализ баланса автомобиля
        balance = telemetry.get("balance", "neutral")
        if balance == "oversteer":
            adjustments["tire_pressure_rear"] = +0.5
            adjustments["rear_wing"] = +2
            adjustments["differential_coast"] = -10
            explanations.append("Избыточная поворачиваемость: корректировки для стабильности")
        elif balance == "understeer":
            adjustments["tire_pressure_front"] = +0.5
            adjustments["front_wing"] = -2
            adjustments["differential_power"] = +5
            explanations.append("Недостаточная поворачиваемость: корректировки для отзывчивости")
        
        return adjustments
    
    def _validate_adjustments(self, adjustments: Dict[str, Any], car_data: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация настроек в пределах допустимых значений"""
        if not car_data or "setup_ranges" not in car_data:
            return adjustments
        
        validated = {}
        ranges = car_data["setup_ranges"]
        
        for param, value in adjustments.items():
            if param in ranges:
                param_range = ranges[param]
                if isinstance(param_range, list) and len(param_range) == 2:
                    validated[param] = max(param_range[0], min(param_range[1], value))
                elif isinstance(param_range, dict):
                    validated[param] = value
            else:
                validated[param] = value
        
        return validated
    
    def _calculate_confidence(self, conditions: Dict[str, Any], telemetry: Dict[str, Any]) -> float:
        """Расчет уверенности в рекомендациях"""
        confidence_factors = []
        
        if "temperature" in conditions:
            confidence_factors.append(0.9)
        if "weather" in conditions:
            confidence_factors.append(0.9)
        if "brake_avg" in telemetry:
            confidence_factors.append(0.8)
        if "balance" in telemetry:
            confidence_factors.append(0.85)
        if "steering_smoothness" in telemetry:
            confidence_factors.append(0.7)
        
        if not confidence_factors:
            return 0.5
        
        return sum(confidence_factors) / len(confidence_factors)
    
    def get_available_tracks(self) -> List[str]:
        """Получение списка доступных трасс"""
        return list(self.data.get("tracks", {}).keys())
    
    def get_available_cars(self) -> List[str]:
        """Получение списка доступных автомобилей"""
        return list(self.data.get("cars", {}).keys())
    
    def get_track_recommendations(self, track_name: str) -> Dict[str, Any]:
        """Получение общих рекомендаций для трассы"""
        track_data = self.data.get("tracks", {}).get(track_name, {})
        
        if not track_data:
            return {"error": f"Трасса '{track_name}' не найдена"}
        
        return {
            "name": track_data.get("name", track_name),
            "length": track_data.get("length", 0),
            "characteristics": track_data.get("characteristics", []),
            "setup_recommendations": track_data.get("setup_recommendations", {}),
            "sector_info": track_data.get("sector_info", {}),
            "weather_tendency": track_data.get("weather_tendency", "unknown")
        }
    
    def get_car_specifications(self, car_type: str) -> Dict[str, Any]:
        """Получение характеристик автомобиля"""
        car_data = self.data.get("cars", {}).get(car_type, {})
        
        if not car_data:
            return {"error": f"Автомобиль '{car_type}' не найден"}
        
        return car_data
    
    def explain_adjustments(self, adjustments: Dict[str, Any], explanations: List[str]):
        """Подробное объяснение настроек"""
        detailed_explanations = []
        
        for param, value in adjustments.items():
            explanation = f"[{param}]: {value:+.1f}"
            
            if "wing" in param.lower():
                if value > 0:
                    explanation += " (больше прижима, меньше скорости)"
                else:
                    explanation += " (меньше прижима, больше скорости)"
            elif "brake_bias" in param.lower():
                if value > 0:
                    explanation += " (больше торможения передними колесами)"
                else:
                    explanation += " (больше торможения задними колесами)"
            elif "tire_pressure" in param.lower():
                if value > 0:
                    explanation += " (выше давление, меньше пятно контакта)"
                else:
                    explanation += " (ниже давление, больше пятно контакта)"
            elif "spring" in param.lower():
                if value > 0:
                    explanation += " (жестче подвеска)"
                else:
                    explanation += " (мягче подвеска)"
            
            detailed_explanations.append(explanation)
        
        detailed_explanations.extend(explanations)
        return detailed_explanations
    
    def compare_setups(self, setup1: Dict[str, Any], setup2: Dict[str, Any]) -> Dict[str, Any]:
        """Сравнение двух настроек"""
        comparison = {
            "differences": {},
            "recommendations": []
        }
        
        all_params = set(setup1.keys()) | set(setup2.keys())
        
        for param in all_params:
            val1 = setup1.get(param, 0)
            val2 = setup2.get(param, 0)
            
            if val1 != val2:
                comparison["differences"][param] = {
                    "setup1": val1,
                    "setup2": val2,
                    "difference": val2 - val1
                }
        
        return comparison