#!/usr/bin/env python3
"""
LMU Assistant - Помощник для симрейсинга
Улучшенная версия с обработкой ошибок, конфигурацией и логированием
"""

import sys
import os
import logging
import traceback
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent))

try:
    from ui.encyclopedia import EncyclopediaTab
    from ui.telemetry_tab import TelemetryTab
    from ui.garage import GarageTab
    from ui.trainer_tab import TrainerTab
    from ui.progress_tab import ProgressTab
    from ui.overlay_control import OverlayControl
    from core.database import DatabaseManager
    from core.config_manager import ConfigManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Some modules may be missing or have errors")

class LMUAssistant(QtWidgets.QMainWindow):
    """Главное окно приложения LMU Assistant"""
    
    def __init__(self):
        super().__init__()
        
        # Инициализация менеджеров
        self.config_manager = None
        self.db = None
        self.overlay_control = None
        
        try:
            self.init_logging()
            self.init_config()
            self.init_database()
            self.init_ui()
            self.restore_window_state()
            
            if hasattr(self, 'logger'):
                self.logger.info("LMU Assistant started successfully")
            else:
                print("LMU Assistant started successfully")
            
        except Exception as e:
            self.handle_critical_error("Initialization", e)
    
    def init_logging(self):
        """Инициализация системы логирования"""
        # Создаем директорию для логов
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Настройка логирования
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_dir / "lmu_assistant.log", encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
        # Перехватываем необработанные исключения
        sys.excepthook = self.handle_exception
    
    def init_config(self):
        """Инициализация менеджера конфигурации"""
        try:
            self.config_manager = ConfigManager()
            
            # Применяем настройки логирования из конфигурации
            if hasattr(self, 'logger'):
                log_level = self.config_manager.get_setting('main', 'log_level', 'INFO')
                logging.getLogger().setLevel(getattr(logging, log_level))
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Failed to initialize config manager: {e}")
            else:
                print(f"Failed to initialize config manager: {e}")
            # Продолжаем работу с настройками по умолчанию
            self.config_manager = None
    
    def init_database(self):
        """Инициализация базы данных"""
        try:
            db_name = "lmu_data.db"
            if self.config_manager:
                db_name = self.config_manager.get_setting('main', 'database.name', db_name)
            
            self.db = DatabaseManager(db_name)
            if hasattr(self, 'logger'):
                self.logger.info(f"Database initialized: {db_name}")
            else:
                print(f"Database initialized: {db_name}")
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Failed to initialize database: {e}")
            else:
                print(f"Failed to initialize database: {e}")
            # Создаем mock объект для избежания ошибок
            self.db = None
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        try:
            # Основные настройки окна
            self.setWindowTitle("LMU Assistant v2.0")
            self.setWindowIcon(self.get_app_icon())
            
            # Получаем настройки окна из конфигурации
            if self.config_manager:
                ui_config = self.config_manager.get_ui_config()
                window_config = ui_config.get('window', {})
                
                width = window_config.get('width', 1280)
                height = window_config.get('height', 800)
                position = window_config.get('position', [100, 100])
                
                self.setGeometry(position[0], position[1], width, height)
            else:
                self.setGeometry(100, 100, 1280, 800)
            
            # Создание центрального виджета с вкладками
            self.create_tabs()
            
            # Создание меню и панели инструментов
            self.create_menu_bar()
            self.create_status_bar()
            
            # Настройка стиля
            self.apply_theme()
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Failed to initialize UI: {e}")
            else:
                print(f"Failed to initialize UI: {e}")
            raise
    
    def create_tabs(self):
        """Создание вкладок приложения"""
        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Создаем вкладки с обработкой ошибок
        tab_configs = [
            ("📘 Энциклопедия", EncyclopediaTab, "encyclopedia"),
            ("🛠️ Гараж", GarageTab, "garage"),
            ("📡 Телеметрия", TelemetryTab, "telemetry"),
            ("🧠 Тренер", TrainerTab, "trainer"),
            ("📈 Прогресс", ProgressTab, "progress"),
            ("🔲 Оверлей", OverlayControl, "overlay")
        ]
        
        for tab_name, tab_class, tab_id in tab_configs:
            try:
                if tab_class:  # Проверяем, что класс импортирован
                    tab_widget = tab_class(self)
                    self.tabs.addTab(tab_widget, tab_name)
                    
                    # Сохраняем ссылку на оверлей
                    if tab_id == "overlay":
                        self.overlay_control = tab_widget
                else:
                    # Создаем заглушку если класс не импортирован
                    error_tab = QtWidgets.QLabel(f"Модуль {tab_name} не загружен")
                    self.tabs.addTab(error_tab, f"❌ {tab_name}")
                
            except Exception as e:
                if hasattr(self, 'logger'):
                    self.logger.error(f"Failed to create tab {tab_name}: {e}")
                else:
                    print(f"Failed to create tab {tab_name}: {e}")
                # Создаем заглушку
                error_tab = QtWidgets.QLabel(f"Ошибка загрузки вкладки: {e}")
                self.tabs.addTab(error_tab, f"❌ {tab_name}")
        
        # Восстанавливаем последнюю активную вкладку
        if self.config_manager:
            last_tab = self.config_manager.get_setting('ui', 'tabs.default_tab', 0)
            if 0 <= last_tab < self.tabs.count():
                self.tabs.setCurrentIndex(last_tab)
        
        # Подключаем сигнал изменения вкладки
        self.tabs.currentChanged.connect(self.on_tab_changed)
    
    def create_menu_bar(self):
        """Создание меню приложения"""
        menubar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menubar.addMenu('Файл')
        
        # Экспорт данных
        export_action = QtWidgets.QAction('Экспорт данных...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        # Импорт данных
        import_action = QtWidgets.QAction('Импорт данных...', self)
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        # Выход
        exit_action = QtWidgets.QAction('Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню "Инструменты"
        tools_menu = menubar.addMenu('Инструменты')
        
        # Настройки
        settings_action = QtWidgets.QAction('Настройки...', self)
        settings_action.triggered.connect(self.open_settings)
        tools_menu.addAction(settings_action)
        
        # Оверлей
        overlay_action = QtWidgets.QAction('Переключить оверлей', self)
        overlay_action.setShortcut('F10')
        overlay_action.triggered.connect(self.toggle_overlay)
        tools_menu.addAction(overlay_action)
        
        # Меню "Помощь"
        help_menu = menubar.addMenu('Помощь')
        
        # О программе
        about_action = QtWidgets.QAction('О программе', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Логи
        logs_action = QtWidgets.QAction('Показать логи', self)
        logs_action.triggered.connect(self.show_logs)
        help_menu.addAction(logs_action)
    
    def create_status_bar(self):
        """Создание панели состояния"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Готов к работе")
        
        # Индикатор подключения телеметрии
        self.telemetry_status = QtWidgets.QLabel("Телеметрия: Отключена")
        self.telemetry_status.setStyleSheet("color: red;")
        self.status_bar.addPermanentWidget(self.telemetry_status)
        
        # Индикатор базы данных
        db_status = "Подключена" if self.db else "Ошибка"
        self.db_status = QtWidgets.QLabel(f"БД: {db_status}")
        self.db_status.setStyleSheet("color: green;" if self.db else "color: red;")
        self.status_bar.addPermanentWidget(self.db_status)
    
    def apply_theme(self):
        """Применение темы оформления"""
        if not self.config_manager:
            return
        
        theme = self.config_manager.get_setting('ui', 'theme', 'dark')
        
        if theme == 'dark':
            # Темная тема
            dark_style = """
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #3c3c3c;
            }
            QTabBar::tab {
                background-color: #555555;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 4px 4px 0px 0px;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
            QMenuBar {
                background-color: #555555;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #0078d4;
            }
            QStatusBar {
                background-color: #555555;
                color: #ffffff;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #666666;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            """
            self.setStyleSheet(dark_style)
    
    def get_app_icon(self):
        """Получение иконки приложения"""
        try:
            # Попытка загрузить иконку из файла
            icon_path = Path("assets/icon.png")
            if icon_path.exists():
                return QtGui.QIcon(str(icon_path))
        except:
            pass
        
        # Создаем простую иконку программно
        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtCore.Qt.blue)
        return QtGui.QIcon(pixmap)
    
    def restore_window_state(self):
        """Восстановление состояния окна"""
        if not self.config_manager:
            return
        
        try:
            ui_config = self.config_manager.get_ui_config()
            window_config = ui_config.get('window', {})
            
            if window_config.get('maximized', False):
                self.showMaximized()
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.warning(f"Failed to restore window state: {e}")
    
    def save_window_state(self):
        """Сохранение состояния окна"""
        if not self.config_manager:
            return
        
        try:
            window_updates = {
                'window': {
                    'width': self.width(),
                    'height': self.height(),
                    'position': [self.x(), self.y()],
                    'maximized': self.isMaximized()
                },
                'tabs': {
                    'default_tab': self.tabs.currentIndex()
                }
            }
            
            self.config_manager.update_ui_config(window_updates)
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.warning(f"Failed to save window state: {e}")
    
    def on_tab_changed(self, index):
        """Обработка смены вкладки"""
        try:
            tab_name = self.tabs.tabText(index)
            self.status_bar.showMessage(f"Активна вкладка: {tab_name}")
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.warning(f"Error handling tab change: {e}")
    
    def toggle_overlay(self):
        """Переключение оверлея"""
        try:
            if self.overlay_control and hasattr(self.overlay_control, 'toggle_overlay'):
                self.overlay_control.toggle_overlay()
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Модуль оверлея недоступен")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error toggling overlay: {e}")
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось переключить оверлей: {e}")
    
    def export_data(self):
        """Экспорт данных"""
        try:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Экспорт данных", "", "JSON Files (*.json)")
            
            if file_path and self.db:
                QtWidgets.QMessageBox.information(self, "Экспорт", "Функция экспорта будет реализована в следующей версии")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error exporting data: {e}")
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка экспорта: {e}")
    
    def import_data(self):
        """Импорт данных"""
        try:
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "Импорт данных", "", "JSON Files (*.json)")
            
            if file_path:
                QtWidgets.QMessageBox.information(self, "Импорт", "Функция импорта будет реализована в следующей версии")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error importing data: {e}")
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка импорта: {e}")
    
    def open_settings(self):
        """Открытие настроек"""
        try:
            QtWidgets.QMessageBox.information(self, "Настройки", "Диалог настроек будет реализован в следующей версии")
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error opening settings: {e}")
    
    def show_about(self):
        """Показ информации о программе"""
        about_text = """
        <h2>LMU Assistant v2.0</h2>
        <p>Помощник для Le Mans Ultimate</p>
        <p><b>Возможности:</b></p>
        <ul>
        <li>Анализ телеметрии в реальном времени</li>
        <li>Экспертная система настройки автомобилей</li>
        <li>База данных всех машин и трасс LMU</li>
        <li>Обучающие рекомендации</li>
        <li>Оверлей для игры</li>
        <li>Система конфигурации</li>
        </ul>
        <p>© 2025 LMU Assistant Team</p>
        """
        QtWidgets.QMessageBox.about(self, "О программе", about_text)
    
    def show_logs(self):
        """Показ логов"""
        try:
            log_file = Path("logs/lmu_assistant.log")
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                
                dialog = QtWidgets.QDialog(self)
                dialog.setWindowTitle("Логи приложения")
                dialog.setGeometry(200, 200, 800, 600)
                
                layout = QtWidgets.QVBoxLayout()
                text_edit = QtWidgets.QTextEdit()
                text_edit.setPlainText(log_content)
                text_edit.setReadOnly(True)
                
                layout.addWidget(text_edit)
                
                close_button = QtWidgets.QPushButton("Закрыть")
                close_button.clicked.connect(dialog.close)
                layout.addWidget(close_button)
                
                dialog.setLayout(layout)
                dialog.exec_()
            else:
                QtWidgets.QMessageBox.information(self, "Логи", "Файл логов не найден")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error showing logs: {e}")
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось показать логи: {e}")
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Обработка необработанных исключений"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        if hasattr(self, 'logger'):
            self.logger.critical(f"Uncaught exception: {error_msg}")
        else:
            print(f"Uncaught exception: {error_msg}")
        
        QtWidgets.QMessageBox.critical(
            self, "Критическая ошибка", 
            f"Произошла необработанная ошибка:\n{exc_value}\n\nДетали записаны в лог файл."
        )
    
    def handle_critical_error(self, context, error):
        """Обработка критических ошибок"""
        error_msg = f"Critical error in {context}: {error}"
        print(f"ERROR: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Пытаемся показать диалог ошибки
        try:
            app = QtWidgets.QApplication.instance()
            if app:
                QtWidgets.QMessageBox.critical(
                    None, "Критическая ошибка", 
                    f"Не удалось запустить приложение:\n{error}\n\nПроверьте логи для получения подробной информации."
                )
        except:
            pass
        
        sys.exit(1)
    
    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        try:
            if hasattr(self, 'logger'):
                self.logger.info("Application closing...")
            
            # Сохраняем состояние окна
            self.save_window_state()
            
            # Закрываем оверлей
            if self.overlay_control and hasattr(self.overlay_control, 'cleanup'):
                self.overlay_control.cleanup()
            
            # Закрываем базу данных
            if self.db and hasattr(self.db, 'close'):
                self.db.close()
            
            if hasattr(self, 'logger'):
                self.logger.info("Application closed successfully")
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error during application close: {e}")
            else:
                print(f"Error during application close: {e}")
        
        event.accept()

def main():
    """Основная функция запуска"""
    # Создаем приложение
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("LMU Assistant")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("LMU Assistant Team")
    
    # Применяем стиль
    app.setStyle("Fusion")
    
    # Обработка аргументов командной строки
    if "--debug" in sys.argv:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Создаем и показываем главное окно
        window = LMUAssistant()
        window.show()
        
        # Запускаем событийный цикл
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()