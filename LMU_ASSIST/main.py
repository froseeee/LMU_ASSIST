# core/setupexpert.py - Enhanced version with ML integration
"""
Улучшенная экспертная система для оптимизации настроек автомобиля
Интегрирована с Machine Learning для более точных рекомендаций
"""

import json
import logging
import numpy as np
from typing import Dict, Any, Optional, List
from pathlib import Path

class EnhancedSetupExpert:
    """Экспертная система для оптимизации настроек с ML интеграцией"""
    
    def __init__(self, data_file=None, ml_optimizer=None):
        self.logger = logging.getLogger(__name__)
        self.ml_optimizer = ml_optimizer
        
        # Загружаем обновленные данные
        if data_file:
            self.data = self._load_data(data_file)
        else:
            self.data = self._get_default_data_2025()
        
        # Обновленные правила для 2025
        self.setup_rules = self._get_enhanced_rules_2025()
        
        # Кэш для ускорения повторных запросов
        self.recommendation_cache = {}
    
    def _load_data(self, data_file: str) -> Dict[str, Any]:
        """Загрузка данных из файла"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading data file: {e}")
            return self._get_default_data_2025()
    
    def _get_default_data_2025(self) -> Dict[str, Any]:
        """Обновленные данные по умолчанию для 2025"""
        return {
            "cars": {
                "aston_martin_valkyrie_lmh": {
                    "name": "Aston Martin Valkyrie AMR-LMH",
                    "category": "Hypercar",
                    "power": 1000,
                    "weight": 1030,
                    "drivetrain": "AWD",
                    "hybrid_system": True,
                    "engine": "6.5L V12 N/A",
                    "designer": "Adrian Newey",
                    "free_car": True,
                    "setup_ranges": {
                        "front_wing": [1, 15],
                        "rear_wing": [1, 15],
                        "brake_bias": [52, 68],
                        "tire_pressure": {"front": [22.0, 28.0], "rear": [22.0, 28.0]},
                        "hybrid_deployment": [0, 100]
                    }
                },
                "mercedes_amg_gt3_lmgt3": {
                    "name": "Mercedes-AMG GT3 LMGT3 Evo",
                    "category": "LMGT3",
                    "power": 520,
                    "weight": 1300,
                    "drivetrain": "RWD",
                    "manufacturer": "Mercedes-Benz",
                    "return_to_lemans": "First time since 1999",
                    "free_car": True,
                    "setup_ranges": {
                        "front_wing": [1, 8],
                        "rear_wing": [1, 8],
                        "brake_bias": [55, 66],
                        "tire_pressure": {"front": [25.0, 31.0], "rear": [25.0, 31.0]},
                        "abs_setting": [1, 11],
                        "tc_setting": [1, 11]
                    }
                },
                "ford_mustang_lmgt3": {
                    "name": "Ford Mustang LMGT3",
                    "category": "LMGT3",
                    "power": 520,
                    "weight": 1300,
                    "drivetrain": "RWD",
                    "engine_layout": "front_engine",
                    "beginner_friendly": True,
                    "free_car": True,
                    "setup_ranges": {
                        "front_wing": [1, 8],
                        "rear_wing": [1, 8],
                        "brake_bias": [55, 66],
                        "tire_pressure": {"front": [25.0, 31.0], "rear": [25.0, 31.0]},
                        "abs_setting": [1, 11],
                        "tc_setting": [1, 11]
                    }
                },
                "bmw_m4_lmgt3": {
                    "name": "BMW M4 GT3 LMGT3",
                    "category": "LMGT3",
                    "power": 590,
                    "weight": 1317,
                    "drivetrain": "RWD",
                    "stability": "reliable_and_stable",
                    "beginner_friendly": True,
                    "setup_ranges": {
                        "front_wing": [1, 8],
                        "rear_wing": [1, 8],
                        "brake_bias": [55, 66],
                        "tire_pressure": {"front": [25.0, 31.0], "rear": [25.0, 31.0]},
                        "abs_setting": [1, 11],
                        "tc_setting": [1, 11]
                    }
                },
                "mclaren_720s_lmgt3": {
                    "name": "McLaren 720S LMGT3 Evo",
                    "category": "LMGT3",
                    "power": 520,
                    "weight": 1300,
                    "drivetrain": "RWD",
                    "characteristics": "oversteer_happy",
                    "experience_level": "expert",
                    "free_car": True,
                    "setup_ranges": {
                        "front_wing": [1, 8],
                        "rear_wing": [1, 8],
                        "brake_bias": [55, 66],
                        "tire_pressure": {"front": [25.0, 31.0], "rear": [25.0, 31.0]},
                        "abs_setting": [1, 11],
                        "tc_setting": [1, 11]
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
                "lusail": {
                    "name": "Lusail International Circuit",
                    "length": 5.380,
                    "characteristics": ["modern", "desert", "hot_climate"],
                    "wec_debut": "2024",
                    "setup_recommendations": {
                        "aero": "medium_downforce",
                        "suspension": "medium",
                        "brake_bias": "balanced"
                    }
                },
                "interlagos": {
                    "name": "Autódromo José Carlos Pace",
                    "length": 4.309,
                    "characteristics": ["technical", "elevation", "weather_variable"],
                    "wec_return": "2024",
                    "setup_recommendations": {
                        "aero": "medium_high_downforce",
                        "suspension": "medium",
                        "brake_bias": "balanced"
                    }
                }
            }
        }
    
    def _get_enhanced_rules_2025(self) -> Dict[str, Any]:
        """Обновленные правила настройки для 2025"""
        return {
            "lmgt3_2025_tire_model": {
                "entry_stability": {
                    "improvement": "10_percent_wider_limit",
                    "technique": "throw_car_into_corner_harder",
                    "limit_detection": "earlier_warning_through_ffb"
                },
                "exit_rotation": {
                    "limitation": "reduced_natural_rotation",
                    "compensation": "use_throttle_for_rotation",
                    "skill_requirement": "throttle_control_critical"
                },
                "abs_recommendations": {
                    "optimal_setting": "high_settings_despite_unrealistic",
                    "explanation": "current_model_favors_high_abs",
                    "future_change": "may_change_in_updates"
                },
                "traction_control": {
                    "main_tc": [7, 8],
                    "tc_power": [1, 2],
                    "tc_slip": [1, 2],
                    "reasoning": "safety_net_with_minimal_power_cut"
                },
                "tire_wear": {
                    "sensitivity": "high_to_aggressive_driving",
                    "smooth_driving": "critical_for_stint_length",
                    "wear_progression": "accelerates_during_stint"
                }
            },
            
            "hypercar_2025": {
                "cold_tires": {
                    "behavior": "still_merciless",
                    "tire_warmers": "now_available_option",
                    "recommendation": "use_warmers_in_cold_conditions"
                },
                "traction_control": {
                    "levels": [9, 11],
                    "power_cut": [1, 2],
                    "slip_angle": [9, 11],
                    "note": "different_from_lmgt3_optimal"
                },
                "hybrid_management": {
                    "deployment_strategy": "track_specific",
                    "efficiency_priority": "fuel_plus_battery_balance"
                }
            },
            
            "temperature_2025": {
                "extreme_hot_desert": {
                    "threshold": 45,
                    "tracks": ["bahrain", "lusail"],
                    "tire_pressure": "+2.5",
                    "wing_adjustment": "-3",
                    "brake_cooling": "maximum"
                },
                "hot": {
                    "threshold": 35,
                    "tire_pressure": "+1.5",
                    "wing_adjustment": "-2",
                    "explanation": "temperature_management_priority"
                },
                "cold": {
                    "threshold": 15,
                    "tire_pressure": "-1.0",
                    "wing_adjustment": "+1",
                    "tire_warmers": "recommended"
                }
            },
            
            "track_specific_2025": {
                "le_mans": {
                    "priority": "minimum_drag",
                    "wing_reduction": 5,
                    "differential_coast": -15,
                    "explanation": "efficiency_on_straights_critical"
                },
                "lusail": {
                    "desert_conditions": True,
                    "heat_management": "critical",
                    "tire_pressure": "+1.0",
                    "brake_cooling": "increased"
                },
                "interlagos": {
