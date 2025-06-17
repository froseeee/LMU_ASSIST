import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """Менеджер конфигурации приложения"""
    
    def __init__(self, config_dir="config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        
        # Пути к файлам конфигурации
        self.main_config_path = self.config_dir / "main.json"
        self.telemetry_config_path = self.config_dir / "telemetry.json"
        self.ui_config_path = self.config_dir / "ui.json"
        self.overlay_config_path = self.config_dir / "overlay.json"
        
        # Загружаем конфигурации
        self.main_config = self._load_config(self.main_config_path, self._get_default_main_config())
        self.telemetry_config = self._load_config(self.telemetry_config_path, self._get_default_telemetry_config())
        self.ui_config = self._load_config(self.ui_config_path, self._get_default_ui_config())
        self.overlay_config = self._load_config(self.overlay_config_path, self._get_default_overlay_config())
    
    def _get_default_main_config(self):
        """Основная конфигурация по умолчанию"""
        return {
            "app_name": "LMU Assistant",
            "version": "1.0.0",
            "language": "ru",
            "log_level": "INFO",
            "auto_save": True,
            "auto_save_interval": 300,
            "database": {
                "name": "lmu_data.db",
                "backup_enabled": True,
                "backup_interval": 3600
            }
        }
    
    def _get_default_telemetry_config(self):
        """Конфигурация телеметрии по умолчанию"""
        return {
            "udp_port": 20777,
            "timeout": 1.0,
            "buffer_size": 1000,
            "lap_detection_threshold": 0.95,
            "data_validation": {
                "rpm_max": 20000,
                "speed_max": 500,
                "gear_range": [-1, 8]
            },
            "analysis": {
                "smoothness_threshold": 0.75,
                "brake_threshold": 0.85,
                "throttle_threshold": 0.9
            }
        }
    
    def _get_default_ui_config(self):
        """Конфигурация UI по умолчанию"""
        return {
            "window": {
                "width": 1280,
                "height": 800,
                "position": [100, 100],
                "maximized": False
            },
            "theme": "dark",
            "font_size": 12,
            "show_tooltips": True,
            "auto_refresh": {
                "enabled": True,
                "interval": 1000
            },
            "tabs": {
                "default_tab": 0,
                "remember_last_tab": True
            }
        }
    
    def _get_default_overlay_config(self):
        """Конфигурация оверлея по умолчанию"""
        return {
            "enabled": False,
            "position": [50, 50],
            "size": [400, 200],
            "opacity": 0.9,
            "update_interval": 50,
            "elements": {
                "gear": {"enabled": True, "color": "#00FF00", "size": 24},
                "rpm": {"enabled": True, "color": "#FF4444", "size": 18},
                "speed": {"enabled": True, "color": "#44DDFF", "size": 18},
                "throttle": {"enabled": True, "color": "#44FF44", "size": 14},
                "brake": {"enabled": True, "color": "#FF4444", "size": 14},
                "lap_time": {"enabled": True, "color": "#FFFF44", "size": 14}
            },
            "plot": {
                "enabled": True,
                "height": 120,
                "history_length": 100,
                "show_legend": True
            },
            "hotkeys": {
                "toggle": "F10",
                "toggle_plot": "F11",
                "reset_position": "F12"
            }
        }
    
    def _load_config(self, config_path, default_config):
        """Загрузка конфигурации из файла"""
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                config = self._merge_configs(default_config, loaded_config)
                self._save_config(config_path, config)
                
                return config
            else:
                self._save_config(config_path, default_config)
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading config from {config_path}: {e}")
            return default_config
    
    def _save_config(self, config_path, config):
        """Сохранение конфигурации в файл"""
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            self.logger.error(f"Error saving config to {config_path}: {e}")
    
    def _merge_configs(self, default, loaded):
        """Объединение конфигураций с сохранением пользовательских настроек"""
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_main_config(self):
        """Получение основной конфигурации"""
        return self.main_config.copy()
    
    def get_telemetry_config(self):
        """Получение конфигурации телеметрии"""
        return self.telemetry_config.copy()
    
    def get_ui_config(self):
        """Получение конфигурации UI"""
        return self.ui_config.copy()
    
    def get_overlay_config(self):
        """Получение конфигурации оверлея"""
        return self.overlay_config.copy()
    
    def update_main_config(self, updates):
        """Обновление основной конфигурации"""
        self.main_config = self._merge_configs(self.main_config, updates)
        self._save_config(self.main_config_path, self.main_config)
    
    def update_telemetry_config(self, updates):
        """Обновление конфигурации телеметрии"""
        self.telemetry_config = self._merge_configs(self.telemetry_config, updates)
        self._save_config(self.telemetry_config_path, self.telemetry_config)
    
    def update_ui_config(self, updates):
        """Обновление конфигурации UI"""
        self.ui_config = self._merge_configs(self.ui_config, updates)
        self._save_config(self.ui_config_path, self.ui_config)
    
    def update_overlay_config(self, updates):
        """Обновление конфигурации оверлея"""
        self.overlay_config = self._merge_configs(self.overlay_config, updates)
        self._save_config(self.overlay_config_path, self.overlay_config)
    
    def get_setting(self, config_type, path, default=None):
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
    
    def set_setting(self, config_type, path, value):
        """Установка конкретной настройки по пути"""
        config_map = {
            'main': (self.main_config, self.update_main_config),
            'telemetry': (self.telemetry_config, self.update_telemetry_config),
            'ui': (self.ui_config, self.update_ui_config),
            'overlay': (self.overlay_config, self.update_overlay_config)
        }
        
        if config_type not in config_map:
            raise ValueError(f"Unknown config type: {config_type}")
        
        config, update_func = config_map[config_type]
        keys = path.split('.')
        
        updates = {}
        current = updates
        
        for key in keys[:-1]:
            current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        update_func(updates)