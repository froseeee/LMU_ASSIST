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
    from core.constants import AppConstants, UIConstants
    from core.exceptions import LMUAssistantError, ConfigurationError, DatabaseConnectionError
    
    # UI модули
    from ui.garage import GarageTab
    from ui.telemetry_tab import TelemetryTab
    from ui.progress_tab import ProgressTab
    from ui.trainer_tab import TrainerTab
    from ui.encyclopedia import EncyclopediaTab
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
        except Exception as e:
            self.logger.error(f"Unexpected database error: {e}")
            self.database = None
        
        self.setup_ui()
        self.setup_window()
        
        # Таймер для периодических обновлений
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.periodic_update)
        self.update_timer.start(UIConstants.STATUS_BAR_UPDATE_INTERVAL)
        
        self.logger.info("LMU Assistant started successfully")
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Создаем вкладки
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3c3c3c;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #4a4a4a;
                color: #ffffff;
                padding: 12px 20px;
                margin: 2px;
                border-radius: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
            QTabBar::tab:hover {
                background-color: #5a5a5a;
            }
        """)
        
        # Добавляем вкладки
        self.setup_tabs()
        
        layout.addWidget(self.tab_widget)
        
        # Строка состояния
        self.statusBar().showMessage("LMU Assistant готов к работе")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #3c3c3c;
                color: #ffffff;
                border-top: 1px solid #555555;
            }
        """)
    
    def setup_tabs(self):
        """Настройка вкладок"""
        try:
            # Вкладка Setup Expert (Гараж)
            self.garage_tab = GarageTab(self)
            self.tab_widget.addTab(self.garage_tab, "🏎️ Setup Expert")
            
            # Вкладка телеметрии
            self.telemetry_tab = TelemetryTab(self)
            self.tab_widget.addTab(self.telemetry_tab, "📡 Телеметрия")
            
            # Вкладка прогресса
            self.progress_tab = ProgressTab(self)
            self.tab_widget.addTab(self.progress_tab, "📈 Прогресс")
            
            # Вкладка тренера
            self.trainer_tab = TrainerTab(self)
            self.tab_widget.addTab(self.trainer_tab, "🎯 Тренер")
            
            # Вкладка энциклопедии
            self.encyclopedia_tab = EncyclopediaTab(self)
            self.tab_widget.addTab(self.encyclopedia_tab, "📚 Энциклопедия")
            
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
        
        # Проверяем минимальные размеры
        width = max(width, UIConstants.MIN_WINDOW_WIDTH)
        height = max(height, UIConstants.MIN_WINDOW_HEIGHT)
        
        self.resize(width, height)
        
        position = window_config.get('position', [100, 100])
        self.move(position[0], position[1])
        
        if window_config.get('maximized', False):
            self.showMaximized()
        
        # Стиль окна
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {UIConstants.BACKGROUND_COLOR};
                color: {UIConstants.FOREGROUND_COLOR};
            }}
            QWidget {{
                background-color: {UIConstants.BACKGROUND_COLOR};
                color: {UIConstants.FOREGROUND_COLOR};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)
    
    def periodic_update(self):
        """Периодическое обновление"""
        try:
            # Обновляем строку состояния
            current_tab_index = self.tab_widget.currentIndex()
            tab_names = ["Setup Expert", "Телеметрия", "Прогресс", "Тренер", "Энциклопедия", "Оверлей"]
            
            if 0 <= current_tab_index < len(tab_names):
                status_message = f"Активна вкладка: {tab_names[current_tab_index]}"
                
                # Добавляем информацию о базе данных
                if self.database:
                    status_message += " | БД: подключена"
                else:
                    status_message += " | БД: отключена"
                
                self.statusBar().showMessage(status_message)
        
        except Exception as e:
            self.logger.warning(f"Error in periodic update: {e}")
    
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
                    self.overlay_tab.cleanup()
                except Exception as e:
                    self.logger.error(f"Error cleaning up overlay: {e}")
            
            if self.database:
                try:
                    self.database.close()
                except Exception as e:
                    self.logger.error(f"Error closing database: {e}")
            
            # Останавливаем таймер
            if self.update_timer and self.update_timer.isActive():
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
        
        # Корневой логгер
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Очищаем существующие хендлеры
        root_logger.handlers.clear()
        
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        return True
        
    except Exception as e:
        print(f"Failed to setup logging: {e}")
        return False


def check_dependencies() -> bool:
    """Проверка необходимых зависимостей"""
    missing_deps = []
    
    try:
        import PyQt5
    except ImportError:
        missing_deps.append("PyQt5")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import matplotlib
    except ImportError:
        missing_deps.append("matplotlib")
    
    if missing_deps:
        print("Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install missing dependencies using:")
        print("pip install " + " ".join(missing_deps))
        return False
    
    return True


def create_directories() -> bool:
    """Создание необходимых директорий"""
    directories = [
        AppConstants.CONFIG_DIR,
        AppConstants.LOG_DIR,
        AppConstants.ASSETS_DIR,
        AppConstants.DATA_DIR,
        AppConstants.MODELS_DIR
    ]
    
    success = True
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create directory {directory}: {e}")
            success = False
    
    return success


def check_data_files() -> bool:
    """Проверка наличия необходимых файлов данных"""
    data_file = Path(AppConstants.DATA_DIR) / "lmu_data.json"
    
    if not data_file.exists():
        print(f"Warning: Data file not found: {data_file}")
        print("Some features may not work properly without the data file.")
        return False
    
    return True


def main():
    """Основная функция приложения"""
    try:
        # Проверяем зависимости
        if not check_dependencies():
            return 1
        
        # Создаем необходимые директории
        create_directories()
        
        # Настройка высокого DPI
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Создание приложения
        app = QApplication(sys.argv)
        app.setApplicationName(AppConstants.APP_NAME)
        app.setApplicationVersion(AppConstants.VERSION)
        app.setOrganizationName(AppConstants.ORGANIZATION)
        
        # Инициализация конфигурации
        try:
            config_manager = ConfigManager()
        except ConfigurationError as e:
            print(f"Configuration error: {e}")
            QMessageBox.critical(None, "Configuration Error", str(e))
            return 1
        
        # Настройка логирования
        setup_logging(config_manager)
        logger = logging.getLogger(__name__)
        
        logger.info("=" * 50)
        logger.info(f"Starting {AppConstants.APP_NAME} v{AppConstants.VERSION}")
        logger.info("=" * 50)
        
        # Проверяем файлы данных
        check_data_files()
        
        # Создание и отображение главного окна
        try:
            window = MainWindow(config_manager)
            window.show()
            
            logger.info("Main window displayed successfully")
            
        except Exception as e:
            logger.error(f"Failed to create main window: {e}")
            QMessageBox.critical(None, "Startup Error", 
                               f"Failed to create main window:\n{e}")
            return 1
        
        # Запуск цикла событий
        exit_code = app.exec_()
        
        logger.info(f"Application exited with code: {exit_code}")
        return exit_code
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 130
        
    except Exception as e:
        print(f"Critical error during application startup: {e}")
        
        # Логируем если возможно
        try:
            logger = logging.getLogger(__name__)
            logger.critical(f"Critical startup error: {e}", exc_info=True)
        except:
            pass
        
        # Показываем диалог с ошибкой если возможно
        try:
            if 'app' in locals():
                QMessageBox.critical(None, "Критическая ошибка", 
                                   f"Не удалось запустить приложение:\n{e}")
        except:
            pass
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
