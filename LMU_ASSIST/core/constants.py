"""
Константы для LMU Assistant
Централизованное хранение всех магических чисел и конфигураций
"""

from enum import Enum


class AppConstants:
    """Основные константы приложения"""
    APP_NAME = "LMU Assistant"
    VERSION = "2.0.1"
    ORGANIZATION = "LMU Assistant"
    
    # Пути
    CONFIG_DIR = "config"
    LOG_DIR = "logs"
    DATA_DIR = "data"
    ASSETS_DIR = "assets"
    MODELS_DIR = "models"
    
    # Файлы конфигурации
    MAIN_CONFIG_FILE = "main.json"
    UI_CONFIG_FILE = "ui.json"
    # УБРАЛИ: TELEMETRY_CONFIG_FILE = "telemetry.json"
    # УБРАЛИ: OVERLAY_CONFIG_FILE = "overlay.json"
    
    # База данных
    DEFAULT_DB_NAME = "lmu_data.db"
    DB_BACKUP_INTERVAL = 3600  # секунд


# УБРАЛИ ВЕСЬ КЛАСС TelemetryConstants
# class TelemetryConstants:
#     """Константы для телеметрии"""
#     ...


class UIConstants:
    """Константы пользовательского интерфейса"""
    # Размеры окна по умолчанию
    DEFAULT_WINDOW_WIDTH = 1280
    DEFAULT_WINDOW_HEIGHT = 800
    MIN_WINDOW_WIDTH = 800
    MIN_WINDOW_HEIGHT = 600
    
    # Шрифты
    DEFAULT_FONT_SIZE = 12
    MIN_FONT_SIZE = 8
    MAX_FONT_SIZE = 24
    
    # Цвета (темная тема)
    BACKGROUND_COLOR = "#2b2b2b"
    FOREGROUND_COLOR = "#ffffff"
    ACCENT_COLOR = "#0078d4"
    SUCCESS_COLOR = "#22c55e"
    WARNING_COLOR = "#f59e0b"
    ERROR_COLOR = "#ef4444"
    
    # УБРАЛИ ОВЕРЛЕЙ:
    # DEFAULT_OVERLAY_OPACITY = 0.9
    # MIN_OVERLAY_OPACITY = 0.3
    # MAX_OVERLAY_OPACITY = 1.0
