import json
import os
import logging
import threading
import time
import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from .constants import ErrorMessages  # Убираем AppConstants для избежания circular import


class ConfigError(Exception):
    """Базовая ошибка конфигурации"""
    pass


class ConfigValidationError(ConfigError):
    """Ошибка валидации конфигурации"""
    pass


class ConfigManager:
    """Улучшенный менеджер конфигурации с валидацией и thread-safety"""
    
    def __init__(self, config_dir: str = None):
        self.config_dir = Path(config_dir or "config")  # Используем строку напрямую
        self.config_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        self._lock = threading.RLock()
        
        # Пути к файлам конфигурации (используем строки напрямую)
        self.main_config_path = self.config_dir / "main.json"
        self.telemetry_config_path = self.config_dir / "telemetry.json"
        self.ui_config_path = self.config_dir / "ui.json"
        self.overlay_config_path = self.config_dir / "overlay.json"
        
        # Загружаем конфигурации
        self._load_all_configs()
    
    def _load_all_configs(self):
        """Загрузка всех конфигураций"""
        try:
            self.main_config = self._load_config(
                self.main_config_path, 
                self._get_default_main_config()
            )
            self.telemetry_config = self._load_config(
                self.telemetry_config_path, 
                self._get_default_telemetry_config()
            )
            self.ui_config = self._load_config(
                self.ui_config_path, 
                self._get_default_ui_config()
            )
            self.overlay_config = self._load_config(
                self.overlay_config_path, 
                self._get_default_overlay_config()
            )
            
            self.logger.info("All configurations loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load configurations: {e}")
            raise ConfigError(f"Configuration initialization failed: {e}")
    
    def _get_default_main_config(self) -> Dict[str, Any]:
        """Основная конфигурация по умолчанию"""
        return {
            "app_name": "LMU Assistant",  # Используем строки напрямую
            "version": "2.0.1",
            "language": "ru",
            "log_level": "INFO",
            "auto_save": True,
            "auto_save_interval": 300,
            "database": {
                "name": "lmu_data.db",
                "backup_enabled": True,
                "backup_interval": 3600,
                "cleanup_enabled": True,
                "cleanup_days": 90
            },
            "features": {
                "ml_enabled": True,
                "overlay_enabled": True,
                "telemetry_enabled": True,
                "analytics_enabled": True
            },
            "paths": {
                "data_dir": "data",
                "models_dir": "models",
                "logs_dir": "logs"
            }
        }
    
    def _get_default_telemetry_config(self) -> Dict[str, Any]:
        """Конфигурация телеметрии по умолчанию"""
        return {
            "udp_port": 20777,  # Используем числа напрямую
            "timeout": 1.0,
            "buffer_size": 1000,
            "lap_detection_threshold": 0.95,
            "connection_timeout": 3.0,
            "update_interval": 50,
            "data_validation": {
                "enabled": True,
                "rpm_max": 20000,
                "speed_max": 500,
                "gear_range": [-1, 8]
            },
            "analysis": {
                "smoothness_threshold": 0.75,
                "brake_threshold": 0.85,
                "throttle_threshold": 0.9,
                "consistency_window": 10
            },
            "recording": {
                "enabled": True,
                "auto_save": True,
                "max_file_size": 100 * 1024 * 1024,  # 100MB
                "compression": True
            }
        }
    
    def _get_default_ui_config(self) -> Dict[str, Any]:
        """Конфигурация UI по умолчанию"""
        return {
            "window": {
                "width": 1280,  # Используем числа напрямую
                "height": 800,
                "position": [100, 100],
                "maximized": False,
                "always_on_top": False
            },
            "theme": {
                "name": "dark",
                "accent_color": "#0078d4",
                "font_family": "Segoe UI",
                "font_size": 12
            },
            "show_tooltips": True,
            "auto_refresh": {
                "enabled": True,
                "interval": 1000
            },
            "tabs": {
                "default_tab": 0,
                "remember_last_tab": True,
                "show_icons": True
            },
            "charts": {
                "update_interval": 100,
                "max_data_points": 1000,
                "smooth_updates": True
            },
            "notifications": {
                "enabled": True,
                "position": "bottom_right",
                "duration": 3000
            }
        }
    
    def _get_default_overlay_config(self) -> Dict[str, Any]:
        """Конфигурация оверлея по умолчанию"""
        return {
            "enabled": False,
            "position": [50, 50],
            "size": [400, 200],
            "opacity": 0.9,  # Используем числа напрямую
            "update_interval": 50,
            "always_on_top": True,
            "click_through": False,
            "elements": {
                "gear": {
                    "enabled": True, 
                    "color": "#00FF00", 
                    "size": 24,
                    "position": [10, 10]
                },
                "rpm": {
                    "enabled": True, 
                    "color": "#FF4444", 
                    "size": 18,
                    "position": [10, 50]
                },
                "speed": {
                    "enabled": True, 
                    "color": "#44DDFF", 
                    "size": 18,
                    "position": [150, 50]
                },
                "throttle": {
                    "enabled": True, 
                    "color": "#44FF44", 
                    "size": 14,
                    "position": [10, 90]
                },
                "brake": {
                    "enabled": True, 
                    "color": "#FF4444", 
                    "size": 14,
                    "position": [150, 90]
                },
                "lap_time": {
                    "enabled": True, 
                    "color": "#FFFF44", 
                    "size": 14,
                    "position": [10, 130]
                }
            },
            "plot": {
                "enabled": True,
                "height": 120,
                "history_length": 100,
                "show_legend": True,
                "background_alpha": 0.8
            },
            "hotkeys": {
                "toggle": "F10",
                "toggle_plot": "F11",
                "reset_position": "F12",
                "toggle_elements": "F9"
            },
            "themes": {
                "current": "dark",
                "dark": {
                    "background": "#2b2b2b",
                    "text": "#ffffff",
                    "border": "#555555"
                },
                "light": {
                    "background": "#ffffff",
                    "text": "#000000", 
                    "border": "#cccccc"
                }
            }
        }
    
    def _load_config(self, config_path: Path, default_config: Dict[str, Any]) -> Dict[str, Any]:
        """Загрузка конфигурации из файла с валидацией"""
        with self._lock:
            try:
                if config_path.exists():
                    # Проверяем размер файла
                    file_size = config_path.stat().st_size
                    if file_size > 1024 * 1024:  # 1MB
                        raise ConfigError(f"Config file too large: {file_size} bytes")
                    
                    with open(config_path, 'r', encoding='utf-8') as f:
                        loaded_config = json.load(f)
                    
                    # Валидируем загруженную конфигурацию
                    if not isinstance(loaded_config, dict):
                        raise ConfigValidationError("Config must be a dictionary")
                    
                    # Объединяем с дефолтными значениями
                    config = self._merge_configs(default_config, loaded_config)
                    
                    # Валидируем объединенную конфигурацию
                    self._validate_config(config, config_path.name)
                    
                    # Сохраняем обновленную конфигурацию
                    self._save_config(config_path, config)
                    
                    self.logger.debug(f"Config loaded: {config_path.name}")
                    return config
                else:
                    # Создаем файл с дефолтными значениями
                    self._save_config(config_path, default_config)
                    self.logger.info(f"Created default config: {config_path.name}")
                    return default_config
                    
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON in {config_path}: {e}")
                # Создаем backup поврежденного файла
                backup_path = config_path.with_suffix(f'.backup_{int(time.time())}')
                try:
                    config_path.rename(backup_path)
                    self.logger.info(f"Corrupted config backed up to {backup_path}")
                except Exception:
                    pass
                
                # Возвращаем дефолтную конфигурацию
                self._save_config(config_path, default_config)
                return default_config
                
            except Exception as e:
                self.logger.error(f"Error loading config from {config_path}: {e}")
                return default_config
    
    def _validate_config(self, config: Dict[str, Any], config_name: str):
        """Валидация конфигурации"""
        try:
            if config_name == "main.json":  # Используем строки напрямую
                self._validate_main_config(config)
            elif config_name == "telemetry.json":
                self._validate_telemetry_config(config)
            elif config_name == "ui.json":
                self._validate_ui_config(config)
            elif config_name == "overlay.json":
                self._validate_overlay_config(config)
                
        except Exception as e:
            raise ConfigValidationError(f"Validation failed for {config_name}: {e}")
    
    def _validate_main_config(self, config: Dict[str, Any]):
        """Валидация основной конфигурации"""
        required_fields = ['app_name', 'version', 'language']
        for field in required_fields:
            if field not in config:
                raise ConfigValidationError(f"Missing required field: {field}")
        
        # Валидация значений
        if not isinstance(config.get('auto_save_interval', 0), (int, float)) or config.get('auto_save_interval', 0) < 10:
            raise ConfigValidationError("auto_save_interval must be >= 10 seconds")
        
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if config.get('log_level', '').upper() not in valid_log_levels:
            config['log_level'] = 'INFO'
    
    def _validate_telemetry_config(self, config: Dict[str, Any]):
        """Валидация конфигурации телеметрии"""
        port = config.get('udp_port', 0)
        if not isinstance(port, int) or not (1024 <= port <= 65535):
            raise ConfigValidationError("udp_port must be between 1024 and 65535")
        
        timeout = config.get('timeout', 0)
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ConfigValidationError("timeout must be positive")
    
    def _validate_ui_config(self, config: Dict[str, Any]):
        """Валидация конфигурации UI"""
        window = config.get('window', {})
        width = window.get('width', 0)
        height = window.get('height', 0)
        
        if not isinstance(width, int) or width < 800:  # Используем числа напрямую
            window['width'] = 1280
        
        if not isinstance(height, int) or height < 600:
            window['height'] = 800
    
    def _validate_overlay_config(self, config: Dict[str, Any]):
        """Валидация конфигурации оверлея"""
        opacity = config.get('opacity', 0)
        if not isinstance(opacity, (int, float)) or not (0.1 <= opacity <= 1.0):
            config['opacity'] = 0.9
        
        update_interval = config.get('update_interval', 0)
        if not isinstance(update_interval, int) or not (16 <= update_interval <= 1000):
            config['update_interval'] = 50
    
    def _save_config(self, config_path: Path, config: Dict[str, Any]):
        """Сохранение конфигурации в файл"""
        try:
            # Создаем временный файл для атомарной записи
            temp_path = config_path.with_suffix('.tmp')
            
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False, sort_keys=True)
            
            # Атомарно заменяем старый файл
            temp_path.replace(config_path)
            
        except Exception as e:
            self.logger.error(f"Error saving config to {config_path}: {e}")
            # Удаляем временный файл если он остался
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass
            raise ConfigError(f"Failed to save config: {e}")
    
    def _merge_configs(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Объединение конфигураций с сохранением пользовательских настроек"""
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    # Публичные методы для получения конфигураций
    
    def get_main_config(self) -> Dict[str, Any]:
        """Получение основной конфигурации"""
        with self._lock:
            return self.main_config.copy()
    
    def get_telemetry_config(self) -> Dict[str, Any]:
        """Получение конфигурации телеметрии"""
        with self._lock:
            return self.telemetry_config.copy()
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Получение конфигурации UI"""
        with self._lock:
            return self.ui_config.copy()
    
    def get_overlay_config(self) -> Dict[str, Any]:
        """Получение конфигурации оверлея"""
        with self._lock:
            return self.overlay_config.copy()
    
    # Методы для обновления конфигураций
    
    def update_main_config(self, updates: Dict[str, Any]):
        """Обновление основной конфигурации"""
        with self._lock:
            self.main_config = self._merge_configs(self.main_config, updates)
            self._validate_config(self.main_config, "main.json")
            self._save_config(self.main_config_path, self.main_config)
            self.logger.debug("Main config updated")
    
    def update_telemetry_config(self, updates: Dict[str, Any]):
        """Обновление конфигурации телеметрии"""
        with self._lock:
            self.telemetry_config = self._merge_configs(self.telemetry_config, updates)
            self._validate_config(self.telemetry_config, "telemetry.json")
            self._save_config(self.telemetry_config_path, self.telemetry_config)
            self.logger.debug("Telemetry config updated")
    
    def update_ui_config(self, updates: Dict[str, Any]):
        """Обновление конфигурации UI"""
        with self._lock:
            self.ui_config = self._merge_configs(self.ui_config, updates)
            self._validate_config(self.ui_config, "ui.json")
            self._save_config(self.ui_config_path, self.ui_config)
            self.logger.debug("UI config updated")
    
    def update_overlay_config(self, updates: Dict[str, Any]):
        """Обновление конфигурации оверлея"""
        with self._lock:
            self.overlay_config = self._merge_configs(self.overlay_config, updates)
            self._validate_config(self.overlay_config, "overlay.json")
            self._save_config(self.overlay_config_path, self.overlay_config)
            self.logger.debug("Overlay config updated")
    
    # Универсальные методы для работы с настройками
    
    def get_setting(self, config_type: str, path: str, default=None):
        """Получение конкретной настройки по пути"""
        config_map = {
            'main': self.main_config,
            'telemetry': self.telemetry_config,
            'ui': self.ui_config,
            'overlay': self.overlay_config
        }
        
        config = config_map.get(config_type)
        if not config:
            return default
        
        keys = path.split('.')
        value = config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_setting(self, config_type: str, path: str, value: Any):
        """Установка конкретной настройки по пути"""
        config_map = {
            'main': (self.main_config, self.update_main_config),
            'telemetry': (self.telemetry_config, self.update_telemetry_config),
            'ui': (self.ui_config, self.update_ui_config),
            'overlay': (self.overlay_config, self.update_overlay_config)
        }
        
        if config_type not in config_map:
            raise ValueError(f"Unknown config type: {config_type}")
        
        keys = path.split('.')
        updates = {}
        current = updates
        
        # Строим вложенную структуру обновлений
        for key in keys[:-1]:
            current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        
        # Применяем обновления
        _, update_func = config_map[config_type]
        update_func(updates)
    
    def reset_config(self, config_type: str) -> bool:
        """Сброс конфигурации к значениям по умолчанию"""
        try:
            with self._lock:
                if config_type == 'main':
                    self.main_config = self._get_default_main_config()
                    self._save_config(self.main_config_path, self.main_config)
                elif config_type == 'telemetry':
                    self.telemetry_config = self._get_default_telemetry_config()
                    self._save_config(self.telemetry_config_path, self.telemetry_config)
                elif config_type == 'ui':
                    self.ui_config = self._get_default_ui_config()
                    self._save_config(self.ui_config_path, self.ui_config)
                elif config_type == 'overlay':
                    self.overlay_config = self._get_default_overlay_config()
                    self._save_config(self.overlay_config_path, self.overlay_config)
                else:
                    raise ValueError(f"Unknown config type: {config_type}")
                
                self.logger.info(f"Config {config_type} reset to defaults")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to reset config {config_type}: {e}")
            return False
    
    def export_config(self, export_path: str) -> bool:
        """Экспорт всех конфигураций в один файл"""
        try:
            export_data = {
                'main': self.get_main_config(),
                'telemetry': self.get_telemetry_config(),
                'ui': self.get_ui_config(),
                'overlay': self.get_overlay_config(),
                'export_timestamp': datetime.datetime.now().isoformat(),
                'app_version': "2.0.1"  # Используем строку напрямую
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configurations exported to {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export configs: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Импорт конфигураций из файла"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Проверяем структуру файла
            if not isinstance(import_data, dict):
                raise ConfigError("Invalid import file format")
            
            # Импортируем каждую конфигурацию
            if 'main' in import_data:
                self.update_main_config(import_data['main'])
            if 'telemetry' in import_data:
                self.update_telemetry_config(import_data['telemetry'])
            if 'ui' in import_data:
                self.update_ui_config(import_data['ui'])
            if 'overlay' in import_data:
                self.update_overlay_config(import_data['overlay'])
            
            self.logger.info(f"Configurations imported from {import_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import configs: {e}")
            return False
