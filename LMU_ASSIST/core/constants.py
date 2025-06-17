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
    TELEMETRY_CONFIG_FILE = "telemetry.json"
    UI_CONFIG_FILE = "ui.json"
    OVERLAY_CONFIG_FILE = "overlay.json"
    
    # База данных
    DEFAULT_DB_NAME = "lmu_data.db"
    DB_BACKUP_INTERVAL = 3600  # секунд


class TelemetryConstants:
    """Константы для телеметрии"""
    DEFAULT_PORT = 20777
    DEFAULT_TIMEOUT = 1.0
    CONNECTION_TIMEOUT = 3.0
    
    # Размеры буферов
    DEFAULT_BUFFER_SIZE = 1000
    MAX_BUFFER_SIZE = 10000
    
    # Валидация данных
    MAX_RPM = 20000
    MAX_SPEED_KMH = 500
    GEAR_RANGE = (-1, 8)  # R, N, 1-8
    
    # Интервалы обновления
    MIN_UPDATE_INTERVAL = 16  # мс (60 FPS)
    MAX_UPDATE_INTERVAL = 1000  # мс
    DEFAULT_UPDATE_INTERVAL = 50  # мс (20 FPS)
    
    # Детекция кругов
    LAP_COMPLETION_THRESHOLD = 0.95
    MIN_LAP_DATA_POINTS = 10


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
    
    # Оверлей
    DEFAULT_OVERLAY_OPACITY = 0.9
    MIN_OVERLAY_OPACITY = 0.3
    MAX_OVERLAY_OPACITY = 1.0
    
    # Таймауты обновления
    STATUS_BAR_UPDATE_INTERVAL = 1000  # мс
    CHART_UPDATE_INTERVAL = 100  # мс


class MLConstants:
    """Константы для машинного обучения"""
    # Обучение
    MIN_TRAINING_SAMPLES = 10
    RETRAIN_INTERVAL = 50  # новых образцов
    CROSS_VALIDATION_FOLDS = 3
    
    # Модели
    RANDOM_FOREST_ESTIMATORS = 100
    GRADIENT_BOOSTING_ESTIMATORS = 100
    MLP_HIDDEN_LAYERS = (100, 50)
    
    # Уверенность и пороги
    MIN_CONFIDENCE = 0.1
    MAX_CONFIDENCE = 0.95
    CONFIDENCE_THRESHOLD = 0.8
    
    # Оптимизация настроек
    MAX_SETUP_CANDIDATES = 50
    SETUP_VARIATION_PROBABILITY = 0.3
    
    # Предсказания
    INCIDENT_RISK_WINDOW = 5  # количество точек данных
    TELEMETRY_HISTORY_LENGTH = 100


class DatabaseConstants:
    """Константы базы данных"""
    DEFAULT_DB_NAME = "lmu_data.db"  # Добавляем недостающую константу
    
    # Лимиты
    MAX_SESSIONS_DISPLAY = 50
    MAX_LAPS_DISPLAY = 100
    MAX_COMPLETED_LAPS_STORE = 50
    
    # Таймауты
    DB_CONNECTION_TIMEOUT = 30.0  # секунд
    DB_QUERY_TIMEOUT = 10.0  # секунд
    
    # Очистка
    AUTO_CLEANUP_DAYS = 90  # дней для хранения старых данных


class SetupConstants:
    """Константы для настройки автомобилей"""
    # Базовые диапазоны настроек
    WING_RANGE = (1, 15)
    BRAKE_BIAS_RANGE = (50, 70)
    TIRE_PRESSURE_RANGE = (20, 30)
    SPRING_RANGE = (10, 100)
    DIFFERENTIAL_RANGE = (10, 90)
    
    # Температурные пороги
    COLD_TEMPERATURE = 15  # °C
    OPTIMAL_TEMPERATURE = 25  # °C
    HOT_TEMPERATURE = 35  # °C
    EXTREME_HOT_TEMPERATURE = 45  # °C
    
    # Корректировки
    MAX_WING_ADJUSTMENT = 5
    MAX_PRESSURE_ADJUSTMENT = 2.5
    MAX_BIAS_ADJUSTMENT = 5
    
    # Оценка уверенности
    BASE_CONFIDENCE = 0.5
    MAX_CONFIDENCE_FACTORS = 5


class AnalysisConstants:
    """Константы для анализа и тренировки"""
    # Пороги качества вождения
    BRAKING_EFFICIENCY_THRESHOLD = 0.85
    THROTTLE_SMOOTHNESS_THRESHOLD = 0.8
    STEERING_SMOOTHNESS_THRESHOLD = 0.75
    CONSISTENCY_THRESHOLD = 0.95
    
    # Анализ секторов
    SECTOR_DEVIATION_THRESHOLD = 2.0  # секунды
    MIN_SECTORS_FOR_ANALYSIS = 3
    
    # Тренировки
    DEFAULT_SESSION_TIME = "45-60 минут"
    MAX_TRAINING_AREAS = 3
    MIN_EXERCISE_TIME = 15  # минут
    MAX_EXERCISE_TIME = 30  # минут
    
    # Скользящие окна для анализа
    CONSISTENCY_WINDOW_SIZE = 10  # кругов
    TELEMETRY_ANALYSIS_WINDOW = 100  # точек данных


class NetworkConstants:
    """Константы для сетевого взаимодействия"""
    # UDP настройки
    UDP_BUFFER_SIZE = 1024
    MAX_UDP_RETRIES = 3
    
    # Сеть
    LOCALHOST = "0.0.0.0"
    DEFAULT_BIND_ADDRESS = "0.0.0.0"
    
    # Таймауты
    SOCKET_TIMEOUT = 1.0
    CONNECTION_RETRY_DELAY = 0.1
    MAX_CONSECUTIVE_ERRORS = 10


class FileConstants:
    """Константы для работы с файлами"""
    # Расширения файлов
    JSON_EXTENSION = ".json"
    CSV_EXTENSION = ".csv"
    LOG_EXTENSION = ".log"
    
    # Размеры файлов
    MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_CONFIG_FILE_SIZE = 1024 * 1024   # 1 MB
    
    # Кодировки
    DEFAULT_ENCODING = "utf-8"
    
    # Backup
    MAX_BACKUP_FILES = 5
    BACKUP_SUFFIX = ".backup"


class ValidationConstants:
    """Константы для валидации данных"""
    # Строки
    MAX_STRING_LENGTH = 1000
    MAX_FILENAME_LENGTH = 255
    
    # Числовые значения
    MIN_LAP_TIME = 10.0   # секунд (минимальное разумное время круга)
    MAX_LAP_TIME = 600.0  # секунд (максимальное разумное время круга)
    
    # Диапазоны телеметрии
    MIN_RPM = 0
    MAX_RPM = 20000
    MIN_SPEED = 0
    MAX_SPEED = 500  # км/ч
    MIN_THROTTLE = 0.0
    MAX_THROTTLE = 1.0
    MIN_BRAKE = 0.0
    MAX_BRAKE = 1.0
    MIN_STEERING = -45.0  # градусы
    MAX_STEERING = 45.0   # градусы


class ErrorMessages:
    """Сообщения об ошибках"""
    # Телеметрия
    TELEMETRY_CONNECTION_FAILED = "Не удалось подключиться к телеметрии"
    TELEMETRY_DATA_INVALID = "Некорректные данные телеметрии"
    TELEMETRY_TIMEOUT = "Таймаут соединения с телеметрией"
    
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
