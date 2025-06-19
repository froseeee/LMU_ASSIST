#!/usr/bin/env python3
"""
LMU Assistant - Le Mans Ultimate Setup and Telemetry Tool
Main entry point for the application
"""

import sys
import os
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

# Импорты модулей приложения
try:
    from core.config_manager import ConfigManager
    from core.database import DatabaseManager
    from core.event_system import EventSystem
    from core.constants import AppConstants, UIConstants, DatabaseConstants, LoggingConstants
    from core.exceptions import LMUAssistantError, ConfigurationError, DatabaseConnectionError
    
    # UI модули
    from ui.garage import GarageTab
    from ui.progress_tab import ProgressTab
    from ui.trainer_tab import TrainerTab
    from ui.preferences_dialog import PreferencesDialog
    
except ImportError as e:
    print(f"Critical import error: {e}")
    print("Please ensure all required modules are installed and accessible")
    sys.exit(1)


class MainWindow(QMainWindow):
    """Главное окно приложения LMU Assistant"""
    
    def __init__(self, config_manager=None):
        super().__init__()
        
        # Инициализация логгера ПЕРВЫМ
        self.logger = logging.getLogger(__name__)
        
        # Инициализация компонентов
        self.config_manager = config_manager or ConfigManager()
        self.event_system = EventSystem()
        
        # Инициализация базы данных с обработкой ошибок
        try:
            self.database = DatabaseManager()
            self.logger.info(f"Database initialized: {DatabaseConstants.DEFAULT_DB_NAME}")
        except DatabaseConnectionError as e:
            self.logger.error(f"Database initialization failed: {e}")
            self.database = None
            # Показываем предупреждение пользователю
            QMessageBox.warning(None, "Database Error", 
                              f"Failed to initialize database: {e}\n\nSome features may not work properly.")
        
        # Инициализация UI
        self.setup_ui()
        self.setup_window()
        self.setup_update_timer()
        
        self.logger.info(f"{AppConstants.APP_NAME} v{AppConstants.VERSION} started")
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        try:
            # Центральный виджет
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Layout
            layout = QVBoxLayout(central_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # Tab Widget
            self.tab_widget = QTabWidget()
            layout.addWidget(self.tab_widget)
            
            # Создаем вкладки
            self.setup_tabs()
            
        except Exception as e:
            self.logger.error(f"Error setting up UI: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать интерфейс: {e}")
    
    def setup_tabs(self):
        """Создание вкладок приложения"""
        try:
            # Вкладка гаража (Setup Expert)
            self.garage_tab = GarageTab(self)
            self.tab_widget.addTab(self.garage_tab, "🔧 Гараж")
            
            # Вкладка прогресса
            self.progress_tab = ProgressTab(self)
            self.tab_widget.addTab(self.progress_tab, "📈 Прогресс")
            
            # Вкладка тренера
            self.trainer_tab = TrainerTab(self)
            self.tab_widget.addTab(self.trainer_tab, "🎯 Тренер")
            
            # Устанавливаем вкладку по умолчанию
            default_tab = self.config_manager.get_setting('ui', 'tabs.default_tab', 0)
            if 0 <= default_tab < self.tab_widget.count():
                self.tab_widget.setCurrentIndex(default_tab)
            
        except Exception as e:
            self.logger.error(f"Error setting up tabs: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать вкладки: {e}")
    
    def setup_window(self):
        """Настройка окна"""
        # Заголовок и иконка
        self.setWindowTitle(f"{AppConstants.APP_NAME} v{AppConstants.VERSION}")
        
        # Попытка установить иконку
        try:
            icon_path = Path(AppConstants.ASSETS_DIR) / "icon.ico"
            if icon_path.exists():
                self.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            self.logger.debug(f"Could not set window icon: {e}")
        
        # Размер и позиция окна
        ui_config = self.config_manager.get_ui_config()
        window_config = ui_config.get('window', {})
        
        width = window_config.get('width', UIConstants.DEFAULT_WINDOW_WIDTH)
        height = window_config.get('height', UIConstants.DEFAULT_WINDOW_HEIGHT)
        
        # Валидация размеров
        width = max(width, UIConstants.MIN_WINDOW_WIDTH)
        height = max(height, UIConstants.MIN_WINDOW_HEIGHT)
        
        self.resize(width, height)
        
        # Позиция окна
        if 'position' in window_config:
            pos = window_config['position']
            if isinstance(pos, list) and len(pos) == 2:
                self.move(pos[0], pos[1])
        
        # Максимизировано ли окно
        if window_config.get('maximized', False):
            self.showMaximized()
    
    def setup_update_timer(self):
        """Настройка таймера обновлений"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(UIConstants.STATUS_BAR_UPDATE_INTERVAL)
    
    def update_status(self):
        """Обновление статусной информации"""
        try:
            # Базовая статусная информация
            status_parts = []
            
            # Статус базы данных
            if self.database:
                status_parts.append("🗄️ БД OK")
            else:
                status_parts.append("🗄️ БД Ошибка")
            
            # Статус приложения
            status_parts.append(f"🏁 LMU Assistant v{AppConstants.VERSION}")
            
            # Обновляем статусную строку
            status_text = " | ".join(status_parts)
            self.statusBar().showMessage(status_text)
            
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")
    
    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        try:
            self.logger.info("Application closing...")
            
            # Сохраняем конфигурацию окна
            window_config = {
                'width': self.width(),
                'height': self.height(),
                'position': [self.x(), self.y()],
                'maximized': self.isMaximized()
            }
            
            try:
                self.config_manager.update_ui_config({'window': window_config})
            except Exception as e:
                self.logger.error(f"Error saving window config: {e}")
            
            # Закрываем базу данных
            if self.database:
                self.database.close()
            
            # Останавливаем обновления
            self.update_timer.stop()
            
            self.logger.info("Application closed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during application shutdown: {e}")
        
        event.accept()


def setup_logging():
    """Настройка системы логирования"""
    try:
        # Создаем директорию для логов
        log_dir = Path(AppConstants.LOG_DIR)
        log_dir.mkdir(exist_ok=True)
        
        # Настраиваем логгер
        logging.basicConfig(
            level=getattr(logging, LoggingConstants.DEFAULT_LOG_LEVEL),
            format=LoggingConstants.LOG_FORMAT,
            datefmt=LoggingConstants.LOG_DATE_FORMAT,
            handlers=[
                logging.FileHandler(log_dir / "lmu_assistant.log", encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
    except Exception as e:
        print(f"Failed to setup logging: {e}")


def main():
    """Главная функция приложения"""
    try:
        # Настройка логирования
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Создание приложения
        app = QApplication(sys.argv)
        app.setApplicationName(AppConstants.APP_NAME)
        app.setApplicationVersion(AppConstants.VERSION)
        app.setOrganizationName(AppConstants.ORGANIZATION)
        
        # Проверка зависимостей
        logger.info(f"Starting {AppConstants.APP_NAME} v{AppConstants.VERSION}")
        
        # Создание главного окна
        try:
            window = MainWindow()
            window.show()
        except Exception as e:
            logger.error(f"Failed to create main window: {e}")
            QMessageBox.critical(None, "Критическая ошибка", 
                               f"Не удалось создать главное окно:\n{e}")
            return 1
        
        # Запуск приложения
        return app.exec_()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
