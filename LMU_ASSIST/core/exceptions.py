"""
Система исключений для LMU Assistant
Централизованная иерархия ошибок
"""


class LMUAssistantError(Exception):
    """Базовая ошибка приложения LMU Assistant"""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ConfigurationError(LMUAssistantError):
    """Ошибки конфигурации"""
    pass


class ConfigLoadError(ConfigurationError):
    """Ошибка загрузки конфигурации"""
    pass


class ConfigSaveError(ConfigurationError):
    """Ошибка сохранения конфигурации"""
    pass


class ConfigValidationError(ConfigurationError):
    """Ошибка валидации конфигурации"""
    pass


class DatabaseError(LMUAssistantError):
    """Базовая ошибка базы данных"""
    pass


class DatabaseConnectionError(DatabaseError):
    """Ошибка подключения к базе данных"""
    pass


class DatabaseQueryError(DatabaseError):
    """Ошибка выполнения запроса"""
    pass


class TelemetryError(LMUAssistantError):
    """Базовая ошибка телеметрии"""
    pass


class TelemetryConnectionError(TelemetryError):
    """Ошибка подключения к телеметрии"""
    pass


class TelemetryDataError(TelemetryError):
    """Ошибка данных телеметрии"""
    pass


class TelemetryTimeoutError(TelemetryError):
    """Таймаут телеметрии"""
    pass


class FileError(LMUAssistantError):
    """Базовая ошибка работы с файлами"""
    pass


class FileNotFoundError(FileError):
    """Файл не найден"""
    pass


class FilePermissionError(FileError):
    """Недостаточно прав для работы с файлом"""
    pass


class FileReadError(FileError):
    """Ошибка чтения файла"""
    pass


class FileWriteError(FileError):
    """Ошибка записи файла"""
    pass


class MLError(LMUAssistantError):
    """Базовая ошибка машинного обучения"""
    pass


class MLInsufficientDataError(MLError):
    """Недостаточно данных для обучения"""
    pass


class MLTrainingError(MLError):
    """Ошибка обучения модели"""
    pass


class MLPredictionError(MLError):
    """Ошибка предсказания"""
    pass


class ValidationError(LMUAssistantError):
    """Ошибка валидации данных"""
    pass


class UIError(LMUAssistantError):
    """Ошибка пользовательского интерфейса"""
    pass


class NetworkError(LMUAssistantError):
    """Ошибка сети"""
    pass


class SetupError(LMUAssistantError):
    """Ошибка настройки автомобиля"""
    pass


# Вспомогательные функции для создания исключений
def create_config_error(message: str, config_type: str = None) -> ConfigurationError:
    """Создание ошибки конфигурации с дополнительной информацией"""
    details = {}
    if config_type:
        details['config_type'] = config_type
    
    return ConfigurationError(
        message=message,
        error_code="CONFIG_ERROR",
        details=details
    )


def create_database_error(message: str, query: str = None, table: str = None) -> DatabaseError:
    """Создание ошибки базы данных с дополнительной информацией"""
    details = {}
    if query:
        details['query'] = query
    if table:
        details['table'] = table
    
    return DatabaseError(
        message=message,
        error_code="DB_ERROR",
        details=details
    )


def create_telemetry_error(message: str, port: int = None, timeout: float = None) -> TelemetryError:
    """Создание ошибки телеметрии с дополнительной информацией"""
    details = {}
    if port:
        details['port'] = port
    if timeout:
        details['timeout'] = timeout
    
    return TelemetryError(
        message=message,
        error_code="TELEMETRY_ERROR",
        details=details
    )
