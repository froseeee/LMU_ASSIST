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
    
    # Таймауты обновления
    STATUS_BAR_UPDATE_INTERVAL = 1000  # мс
    CHART_UPDATE_INTERVAL = 100  # мс


class DatabaseConstants:
    """Константы для базы данных"""
    # Основные настройки
    DEFAULT_DB_NAME = "lmu_data.db"
    CONNECTION_TIMEOUT = 30.0
    
    # Размеры
    MAX_QUERY_LENGTH = 10000
    MAX_RESULT_ROWS = 10000
    
    # Backup
    BACKUP_INTERVAL = 3600  # секунд
    MAX_BACKUP_FILES = 5
    
    # Таблицы
    SESSIONS_TABLE = "sessions"
    LAPS_TABLE = "laps" 
    SETUPS_TABLE = "setups"
    TRACKS_TABLE = "tracks"
    CARS_TABLE = "cars"
    # УБРАЛИ: TELEMETRY_TABLE = "telemetry"


# УБРАЛИ ВЕСЬ КЛАСС NetworkConstants
# class NetworkConstants:
#     """Константы для сетевого взаимодействия"""
#     ...


class ValidationConstants:
    """Константы для валидации данных"""
    # Строки
    MAX_STRING_LENGTH = 1000
    MAX_FILENAME_LENGTH = 255
    
    # Числовые значения
    MIN_LAP_TIME = 10.0   # секунд
    MAX_LAP_TIME = 600.0  # секунд
    
    # УБРАЛИ диапазоны телеметрии:
    # MIN_RPM = 0
    # MAX_RPM = 20000
    # MIN_SPEED = 0
    # MAX_SPEED = 500  # км/ч
    # MIN_THROTTLE = 0.0
    # MAX_THROTTLE = 1.0
    # MIN_BRAKE = 0.0
    # MAX_BRAKE = 1.0
    # MIN_STEERING = -45.0  # градусы
    # MAX_STEERING = 45.0   # градусы


class ErrorMessages:
    """Сообщения об ошибках"""
    # УБРАЛИ телеметрию:
    # TELEMETRY_CONNECTION_FAILED = "Не удалось подключиться к телеметрии"
    # TELEMETRY_DATA_INVALID = "Некорректные данные телеметрии"
    # TELEMETRY_TIMEOUT = "Таймаут соединения с телеметрией"
    
    # База данных
    DATABASE_CONNECTION_FAILED = "Не удалось подключиться к базе данных"
    DATABASE_QUERY_FAILED = "Ошибка выполнения запроса к базе данных"
    
    # Файлы
    FILE_NOT_FOUND = "Файл не найден"
    FILE_READ_ERROR = "Ошибка чтения файла"
    FILE_WRITE_ERROR = "Ошибка записи файла"
    FILE_PERMISSION_ERROR = "Недостаточно прав для работы с файлом"
    
    # Конфигурация
    CONFIG_LOAD_ERROR = "Ошибка загрузки конфигурации"
    CONFIG_SAVE_ERROR = "Ошибка сохранения конфигурации"
    CONFIG_VALIDATION_ERROR = "Ошибка валидации конфигурации"
    
    # ML
    ML_INSUFFICIENT_DATA = "Недостаточно данных для обучения"
    ML_TRAINING_FAILED = "Ошибка обучения модели"
    ML_PREDICTION_FAILED = "Ошибка предсказания"
    
    # Общие
    UNEXPECTED_ERROR = "Неожиданная ошибка"
    OPERATION_CANCELLED = "Операция отменена пользователем"
    INSUFFICIENT_PERMISSIONS = "Недостаточно прав доступа"


class LoggingConstants:
    """Константы для логирования"""
    # Форматы
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Размеры
    MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 5
    
    # Уровни по умолчанию
    DEFAULT_LOG_LEVEL = "INFO"
    DEBUG_LOG_LEVEL = "DEBUG"
    PRODUCTION_LOG_LEVEL = "WARNING"


class TrackType(Enum):
    """Типы трасс"""
    VERY_FAST = "very_fast"
    FAST = "fast"
    TECHNICAL = "technical"
    MIXED = "mixed"
    BUMPY = "bumpy"
    ELEVATION = "elevation"


class CarCategory(Enum):
    """Категории автомобилей"""
    HYPERCAR = "Hypercar"
    LMP2 = "LMP2"
    LMGT3 = "LMGT3"
    GTE = "GTE"


class WeatherType(Enum):
    """Типы погоды"""
    DRY = "dry"
    LIGHT_RAIN = "light_rain"
    HEAVY_RAIN = "heavy_rain"
    VARIABLE = "variable"


class SetupParameter(Enum):
    """Параметры настройки автомобиля"""
    FRONT_WING = "front_wing"
    REAR_WING = "rear_wing"
    BRAKE_BIAS = "brake_bias"
    TIRE_PRESSURE_FRONT = "tire_pressure_front"
    TIRE_PRESSURE_REAR = "tire_pressure_rear"
    FRONT_SPRING = "front_spring"
    REAR_SPRING = "rear_spring"
    DIFFERENTIAL_POWER = "differential_power"
    DIFFERENTIAL_COAST = "differential_coast"
