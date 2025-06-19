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
    from core.constants import AppConstants, UIConstants, DatabaseConstants
    from core.exceptions import LMUAssistantError, ConfigurationError, DatabaseConnectionError
    
    # UI модули
    from ui.garage import GarageTab
    from ui.telemetry_tab import TelemetryTab
    from ui.progress_tab import ProgressTab
    from ui.trainer_tab import TrainerTab
    # УБРАЛИ: from ui.encyclopedia import EncyclopediaTab
    from ui.overlay_control import OverlayControl
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
            
            # Вкладка телеметрии
            self.telemetry_tab = TelemetryTab(self)
            self.tab_widget.addTab(self.telemetry_tab, "📡 Телеметрия")
            
            # Вкладка прогресса
            self.progress_tab = ProgressTab(self)
            self.tab_widget.addTab(self.progress_tab, "📈 Прогресс")
            
            # Вкладка тренера
            self.trainer_tab = TrainerTab(self)
            self.tab_widget.addTab(self.trainer_tab, "🎯 Тренер")
            
            # УБРАЛИ ЭНЦИКЛОПЕДИЮ:
            # self.encyclopedia_tab = EncyclopediaTab(self)
            # self.tab_widget.addTab(self.encyclopedia_tab, "📚 Энциклопедия")
            
            # Вкладка оверлея
            self.overlay_tab = OverlayControl(self)
            self.tab_widget.addTab(self.overlay_tab, "🖥️ Оверлей")
            
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
            
            # Статус телеметрии
            if hasattr(self, 'telemetry_tab') and self.telemetry_tab:
                if hasattr(self.telemetry_tab, 'is_connected') and self.telemetry_tab.is_connected():
                    status_parts.append("📡 Подключено")
                else:
                    status_parts.append("📡 Отключено")
            
            # Статус базы данных
            if self.database:
                status_parts.append("🗄️ БД OK")
            else:
                status_parts.append("🗄️ БД Ошибка")
            
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
                self.logger.error(f"Failed to save window config: {e}")
            
            # Закрываем соединения и освобождаем ресурсы
            if hasattr(self, 'overlay_tab') and self.overlay_tab:
                try:
                    if hasattr(self.overlay_tab, 'cleanup'):
                        self.overlay_tab.cleanup()
                except Exception as e:
                    self.logger.error(f"Error cleaning up overlay: {e}")
            
            if self.database:
                try:
                    self.database.close()
                except Exception as e:
                    self.logger.error(f"Error closing database: {e}")
            
            # Останавливаем таймер
            if hasattr(self, 'update_timer') and self.update_timer and self.update_timer.isActive():
                self.update_timer.stop()
            
            self.logger.info("Application closed successfully")
            event.accept()
            
        except Exception as e:
            self.logger.error(f"Error during application close: {e}")
            event.accept()  # Закрываем в любом случае


def setup_logging(config_manager: ConfigManager) -> bool:
    """Настройка системы логирования"""
    try:
        # Создаем директорию для логов
        log_dir = Path(AppConstants.LOG_DIR)
        log_dir.mkdir(exist_ok=True)
        
        # Получаем уровень логирования из конфигурации
        log_level = config_manager.get_setting('main', 'log_level', 'INFO')
        
        # Настройка форматирования
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Файл-хендлер
        log_file = log_dir / 'lmu_assistant.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # Консоль-хендлер
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Настройка корневого логгера
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        return True
        
    except Exception as e:
        print(f"Failed to setup logging: {e}")
        return False


def main():
    """Главная функция приложения"""
    # Создание приложения QT
    app = QApplication(sys.argv)
    app.setApplicationName(AppConstants.APP_NAME)
    app.setApplicationVersion(AppConstants.VERSION)
    app.setOrganizationName(AppConstants.ORGANIZATION)
    
    try:
        # Инициализация менеджера конфигурации
        config_manager = ConfigManager()
        
        # Настройка логирования
        if not setup_logging(config_manager):
            QMessageBox.critical(None, "Ошибка", "Не удалось настроить систему логирования")
            return 1
        
        # Создание основного окна
        main_window = MainWindow(config_manager)
        main_window.show()
        
        # Запуск приложения
        return app.exec_()
        
    except Exception as e:
        error_msg = f"Critical error starting application: {e}"
        print(error_msg)
        QMessageBox.critical(None, "Критическая ошибка", error_msg)
        return 1


if __name__ == "__main__":
    sys.exit(main())
