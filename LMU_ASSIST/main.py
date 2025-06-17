#!/usr/bin/env python3
"""
LMU Assistant v3.0 - Modern Racing Assistant
Полностью переработанная версия с современным дизайном и улучшенной производительностью
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
    from ui.trainer_tab import TrainerTab
    from ui.progress_tab import ProgressTab
    from overlay.overlay_hud import OverlayHUD
    from ui.garage import GarageTab
    from core.database import DatabaseManager
    from core.config_manager import ConfigManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Some modules may be missing or have errors")

class LMUAssistant(QtWidgets.QMainWindow):
    """Современная версия LMU Assistant с обновленным дизайном"""
    
    def __init__(self):
        super().__init__()
        
        # Состояние приложения
        self.config_manager = None
        self.db = None
        self.overlay_hud = None
        self.is_dark_theme = True
        
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
            self.init_logging()
            self.init_config()
            self.init_database()
            self.init_ui()
            self.setup_style()
            self.restore_window_state()
            
            self.logger.info("Modern LMU Assistant v3.0 started successfully")
            
        except Exception as e:
            self.handle_critical_error("Initialization", e)
    
    def init_logging(self):
        """Инициализация системы логирования"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "lmu_assistant.log", encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        sys.excepthook = self.handle_exception
    
    def init_config(self):
        """Инициализация менеджера конфигурации"""
        try:
            self.config_manager = ConfigManager()
            
            log_level = self.config_manager.get_setting('main', 'log_level', 'INFO')
            logging.getLogger().setLevel(getattr(logging, log_level))
            
        except Exception as e:
            self.logger.error(f"Failed to initialize config manager: {e}")
            self.config_manager = None
    
    def init_database(self):
        """Инициализация базы данных"""
        try:
            db_name = "lmu_data.db"
            if self.config_manager:
                db_name = self.config_manager.get_setting('main', 'database.name', db_name)
            
            self.db = DatabaseManager(db_name)
            self.logger.info(f"Database initialized: {db_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            self.db = None
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Основные настройки окна
        self.setWindowTitle("LMU Assistant v3.0 - Modern Racing Assistant")
        self.setWindowIcon(self.get_app_icon())
        
        # Размер и позиция
        if self.config_manager:
            ui_config = self.config_manager.get_ui_config()
            window_config = ui_config.get('window', {})
            
            width = window_config.get('width', 1400)
            height = window_config.get('height', 900)
            position = window_config.get('position', [100, 100])
            
            self.setGeometry(position[0], position[1], width, height)
            self.setMinimumSize(1200, 700)
        else:
            self.setGeometry(100, 100, 1400, 900)
            self.setMinimumSize(1200, 700)
        
        # Создание основного интерфейса
        self.create_central_widget()
        self.create_menu_bar()
        self.create_status_bar()
        self.create_toolbar()
    
    def create_central_widget(self):
        """Создание центрального виджета"""
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Создаем современные вкладки
        self.create_modern_tabs(layout)
    
    def create_modern_tabs(self, parent_layout):
        """Создание современных вкладок"""
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(False)
        
        # Конфигурация вкладок
        tab_configs = [
            ("🏎️ Setup Expert", GarageTab, "garage"),
            ("📡 Telemetry", TelemetryTab, "telemetry"),
            ("🧠 AI Trainer", TrainerTab, "trainer"),
            ("📈 Progress", ProgressTab, "progress"),
            ("📘 Knowledge Base", EncyclopediaTab, "encyclopedia"),
            ("🎮 Overlay", self.create_overlay_tab, "overlay")
        ]
        
        for tab_name, tab_class, tab_id in tab_configs:
            try:
                if callable(tab_class):
                    if tab_id == "overlay":
                        tab_widget = tab_class()
                    else:
                        tab_widget = tab_class(self)
                else:
                    tab_widget = tab_class(self)
                
                self.tabs.addTab(tab_widget, tab_name)
                
                # Сохраняем ссылку на оверлей
                if tab_id == "overlay":
                    self.overlay_control = tab_widget
                
            except Exception as e:
                self.logger.error(f"Failed to create tab {tab_name}: {e}")
                error_tab = QtWidgets.QLabel(f"❌ Error loading {tab_name}: {e}")
                error_tab.setAlignment(QtCore.Qt.AlignCenter)
                self.tabs.addTab(error_tab, f"❌ {tab_name}")
        
        # Восстанавливаем последнюю активную вкладку
        if self.config_manager:
            last_tab = self.config_manager.get_setting('ui', 'tabs.default_tab', 0)
            if 0 <= last_tab < self.tabs.count():
                self.tabs.setCurrentIndex(last_tab)
        
        self.tabs.currentChanged.connect(self.on_tab_changed)
        parent_layout.addWidget(self.tabs)
    
    def create_overlay_tab(self):
        """Создание вкладки управления оверлеем"""
        overlay_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(overlay_widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Заголовок
        header = self.create_section_header("🎮 Overlay Control", 
                                           "Manage your in-game telemetry overlay")
        layout.addWidget(header)
        
        # Главная карточка
        main_card = QtWidgets.QFrame()
        main_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e0e4e7;
                padding: 24px;
            }
        """)
        
        card_layout = QtWidgets.QVBoxLayout(main_card)
        
        # Статус оверлея
        self.overlay_status = QtWidgets.QLabel("🔴 Overlay: Disabled")
        self.overlay_status.setStyleSheet("""
            color: #ef4444;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 16px;
        """)
        card_layout.addWidget(self.overlay_status)
        
        # Кнопки управления
        buttons_layout = QtWidgets.QHBoxLayout()
        
        self.toggle_overlay_btn = QtWidgets.QPushButton("🚀 Enable Overlay")
        self.toggle_overlay_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46c1);
            }
        """)
        self.toggle_overlay_btn.clicked.connect(self.toggle_overlay)
        
        self.settings_overlay_btn = QtWidgets.QPushButton("⚙️ Settings")
        self.settings_overlay_btn.setStyleSheet("""
            QPushButton {
                background: #f7fafc;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: bold;
                color: #4a5568;
            }
            QPushButton:hover {
                background: #edf2f7;
                border-color: #cbd5e0;
            }
        """)
        
        buttons_layout.addWidget(self.toggle_overlay_btn)
        buttons_layout.addWidget(self.settings_overlay_btn)
        buttons_layout.addStretch()
        
        card_layout.addLayout(buttons_layout)
        
        # Информационная панель
        info_card = self.create_info_card()
        
        layout.addWidget(main_card)
        layout.addWidget(info_card)
        layout.addStretch()
        
        return overlay_widget
    
    def create_section_header(self, title, subtitle):
        """Создание заголовка секции"""
        header_widget = QtWidgets.QWidget()
        header_layout = QtWidgets.QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            color: #1a202c;
            font-size: 28px;
            font-weight: bold;
        """)
        
        subtitle_label = QtWidgets.QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            color: #718096;
            font-size: 16px;
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        return header_widget
    
    def create_info_card(self):
        """Создание информационной карточки"""
        info_card = QtWidgets.QFrame()
        info_card.setStyleSheet("""
            QFrame {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(info_card)
        
        info_title = QtWidgets.QLabel("💡 How to use")
        info_title.setStyleSheet("""
            color: #2d3748;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 12px;
        """)
        
        info_text = QtWidgets.QLabel("""
        <b>Hotkeys:</b><br>
        • <b>F10</b> - Toggle overlay on/off<br>
        • <b>F11</b> - Show/hide telemetry graph<br>
        • <b>F12</b> - Reset overlay position<br><br>
        
        <b>Features:</b><br>
        • Real-time telemetry display<br>
        • Customizable position and opacity<br>
        • Live telemetry graphs<br>
        • Connection status indicator<br>
        • Drag to move, right-click for settings
        """)
        info_text.setStyleSheet("""
            color: #4a5568;
            line-height: 1.5;
        """)
        
        layout.addWidget(info_title)
        layout.addWidget(info_text)
        
        return info_card
    
    def create_menu_bar(self):
        """Создание меню приложения"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background: #1a202c;
                color: white;
                border: none;
                padding: 4px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #4a5568;
            }
            QMenu {
                background: #2d3748;
                color: white;
                border: 1px solid #4a5568;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background: #667eea;
            }
        """)
        
        # Меню "File"
        file_menu = menubar.addMenu('File')
        
        export_action = QtWidgets.QAction('📤 Export Data...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        import_action = QtWidgets.QAction('📥 Import Data...', self)
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QtWidgets.QAction('🚪 Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню "Tools"
        tools_menu = menubar.addMenu('Tools')
        
        overlay_action = QtWidgets.QAction('🎮 Toggle Overlay', self)
        overlay_action.setShortcut('F10')
        overlay_action.triggered.connect(self.toggle_overlay)
        tools_menu.addAction(overlay_action)
        
        settings_action = QtWidgets.QAction('⚙️ Settings...', self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        # Меню "View"
        view_menu = menubar.addMenu('View')
        
        theme_action = QtWidgets.QAction('🎨 Toggle Theme', self)
        theme_action.setShortcut('Ctrl+T')
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        # Меню "Help"
        help_menu = menubar.addMenu('Help')
        
        about_action = QtWidgets.QAction('ℹ️ About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        docs_action = QtWidgets.QAction('📚 Documentation', self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)
    
    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = self.addToolBar('Main')
        toolbar.setStyleSheet("""
            QToolBar {
                background: #f8fafc;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                padding: 8px;
            }
            QToolButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 12px;
                margin: 2px;
                color: #4a5568;
                font-weight: bold;
            }
            QToolButton:hover {
                background: #edf2f7;
                color: #2d3748;
            }
            QToolButton:pressed {
                background: #e2e8f0;
            }
        """)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        
        # Действия панели инструментов
        overlay_action = QtWidgets.QAction('🎮 Overlay', self)
        overlay_action.triggered.connect(self.toggle_overlay)
        toolbar.addAction(overlay_action)
        
        toolbar.addSeparator()
        
        refresh_action = QtWidgets.QAction('🔄 Refresh', self)
        refresh_action.triggered.connect(self.refresh_data)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        settings_action = QtWidgets.QAction('⚙️ Settings', self)
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
    
    def create_status_bar(self):
        """Создание панели состояния"""
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: #1a202c;
                color: white;
                border: none;
                padding: 4px 8px;
            }
            QLabel {
                color: white;
                padding: 4px 8px;
            }
        """)
        
        # Основное сообщение
        self.status_bar.showMessage("Ready - LMU Assistant v3.0")
        
        # Постоянные виджеты
        self.telemetry_status = QtWidgets.QLabel("📡 Telemetry: Disconnected")
        self.telemetry_status.setStyleSheet("color: #ef4444;")
        self.status_bar.addPermanentWidget(self.telemetry_status)
        
        self.overlay_status_label = QtWidgets.QLabel("🎮 Overlay: Off")
        self.overlay_status_label.setStyleSheet("color: #fbbf24;")
        self.status_bar.addPermanentWidget(self.overlay_status_label)
        
        db_status = "Connected" if self.db else "Error"
        self.db_status = QtWidgets.QLabel(f"💾 DB: {db_status}")
        self.db_status.setStyleSheet("color: #10b981;" if self.db else "color: #ef4444;")
        self.status_bar.addPermanentWidget(self.db_status)
    
    def setup_style(self):
        """Настройка стилей приложения"""
        if self.is_dark_theme:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
    
    def apply_dark_theme(self):
        """Применение темной темы"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a202c;
                color: #e2e8f0;
            }
            QTabWidget::pane {
                border: 1px solid #4a5568;
                background-color: #2d3748;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #4a5568;
                color: #e2e8f0;
                padding: 12px 24px;
                margin: 2px;
                border-radius: 8px 8px 0px 0px;
                border: 1px solid #4a5568;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border-color: #667eea;
            }
            QTabBar::tab:hover:!selected {
                background-color: #5a67d8;
            }
            QWidget {
                background-color: #2d3748;
                color: #e2e8f0;
            }
        """)
    
    def apply_light_theme(self):
        """Применение светлой темы"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
                color: #1a202c;
            }
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                background-color: white;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #f1f5f9;
                color: #4a5568;
                padding: 12px 24px;
                margin: 2px;
                border-radius: 8px 8px 0px 0px;
                border: 1px solid #e2e8f0;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border-color: #667eea;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e2e8f0;
            }
            QWidget {
                background-color: white;
                color: #1a202c;
            }
        """)
    
    def get_app_icon(self):
        """Получение иконки приложения"""
        # Создаем простую иконку программно
        pixmap = QtGui.QPixmap(64, 64)
        pixmap.fill(QtCore.Qt.transparent)
        
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Градиентный фон
        gradient = QtGui.QLinearGradient(0, 0, 64, 64)
        gradient.setColorAt(0, QtGui.QColor("#667eea"))
        gradient.setColorAt(1, QtGui.QColor("#764ba2"))
        
        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(4, 4, 56, 56, 12, 12)
        
        # Текст
        painter.setPen(QtGui.QColor("white"))
        painter.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "LMU")
        
        painter.end()
        
        return QtGui.QIcon(pixmap)
    
    def toggle_overlay(self):
        """Переключение оверлея"""
        try:
            if self.overlay_hud is None:
                # Получаем конфигурацию
                config = None
                if self.config_manager:
                    config = self.config_manager.get_overlay_config()
                
                self.overlay_hud = OverlayHUD(config)
                self.overlay_hud.show()
                
                # Обновляем статус
                if hasattr(self, 'overlay_status'):
                    self.overlay_status.setText("🟢 Overlay: Enabled")
                    self.overlay_status.setStyleSheet("color: #10b981; font-size: 18px; font-weight: bold;")
                if hasattr(self, 'toggle_overlay_btn'):
                    self.toggle_overlay_btn.setText("🛑 Disable Overlay")
                self.overlay_status_label.setText("🎮 Overlay: On")
                self.overlay_status_label.setStyleSheet("color: #10b981;")
                
            else:
                self.overlay_hud.close()
                self.overlay_hud = None
                
                # Обновляем статус
                if hasattr(self, 'overlay_status'):
                    self.overlay_status.setText("🔴 Overlay: Disabled")
                    self.overlay_status.setStyleSheet("color: #ef4444; font-size: 18px; font-weight: bold;")
                if hasattr(self, 'toggle_overlay_btn'):
                    self.toggle_overlay_btn.setText("🚀 Enable Overlay")
                self.overlay_status_label.setText("🎮 Overlay: Off")
                self.overlay_status_label.setStyleSheet("color: #fbbf24;")
                
        except Exception as e:
            self.logger.error(f"Error toggling overlay: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to toggle overlay: {e}")
    
    def toggle_theme(self):
        """Переключение темы"""
        self.is_dark_theme = not self.is_dark_theme
        self.setup_style()
        
        # Сохраняем настройку темы
        if self.config_manager:
            theme = "dark" if self.is_dark_theme else "light"
            self.config_manager.update_ui_config({"theme": theme})
    
    def refresh_data(self):
        """Обновление данных"""
        self.status_bar.showMessage("Refreshing data...", 2000)
        # Здесь можно добавить логику обновления данных
    
    def show_settings(self):
        """Показ настроек"""
        QtWidgets.QMessageBox.information(self, "Settings", 
                                         "Advanced settings dialog will be implemented in next update!")
    
    def show_about(self):
        """Показ информации о программе"""
        about_text = """
        <div style="text-align: center;">
            <h2 style="color: #667eea;">🏁 LMU Assistant v3.0</h2>
            <p style="font-size: 16px; margin: 16px 0;">
                <b>Modern Racing Assistant for Le Mans Ultimate</b>
            </p>
            
            <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 16px 0;">
                <h3 style="color: #2d3748;">🚀 New Features</h3>
                <ul style="text-align: left; color: #4a5568;">
                    <li>Modern glass-morphism design</li>
                    <li>Real-time telemetry overlay</li>
                    <li>AI-powered setup optimization</li>
                    <li>Complete car and track database</li>
                    <li>Performance analysis tools</li>
                    <li>Interactive training system</li>
                </ul>
            </div>
            
            <p style="color: #718096;">
                © 2025 LMU Assistant Team<br>
                Built with ❤️ for the sim racing community
            </p>
        </div>
        """
        
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("About LMU Assistant")
        msg_box.setTextFormat(QtCore.Qt.RichText)
        msg_box.setText(about_text)
        msg_box.exec_()
    
    def show_documentation(self):
        """Показ документации"""
        QtWidgets.QMessageBox.information(self, "Documentation", 
                                         "Online documentation will be available soon at docs.lmuassistant.com")
    
    def export_data(self):
        """Экспорт данных"""
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Data", "", "JSON Files (*.json)")
        
        if file_path:
            QtWidgets.QMessageBox.information(self, "Export", 
                                            "Export functionality will be implemented in next update!")
    
    def import_data(self):
        """Импорт данных"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Import Data", "", "JSON Files (*.json)")
        
        if file_path:
            QtWidgets.QMessageBox.information(self, "Import", 
                                            "Import functionality will be implemented in next update!")
    
    def on_tab_changed(self, index):
        """Обработка смены вкладки"""
        tab_name = self.tabs.tabText(index)
        self.status_bar.showMessage(f"Active: {tab_name}")
    
    def restore_window_state(self):
        """Восстановление состояния окна"""
        if not self.config_manager:
            return
        
        try:
            ui_config = self.config_manager.get_ui_config()
            window_config = ui_config.get('window', {})
            
            if window_config.get('maximized', False):
                self.showMaximized()
            
            # Восстанавливаем тему
            theme = ui_config.get('theme', 'dark')
            self.is_dark_theme = (theme == 'dark')
                
        except Exception as e:
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
                },
                'theme': 'dark' if self.is_dark_theme else 'light'
            }
            
            self.config_manager.update_ui_config(window_updates)
            
        except Exception as e:
            self.logger.warning(f"Failed to save window state: {e}")
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Обработка необработанных исключений"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.logger.critical(f"Uncaught exception: {error_msg}")
        
        QtWidgets.QMessageBox.critical(
            self, "Critical Error", 
            f"An unexpected error occurred:\n{exc_value}\n\nCheck logs for details."
        )
    
    def handle_critical_error(self, context, error):
        """Обработка критических ошибок"""
        error_msg = f"Critical error in {context}: {error}"
        print(f"ERROR: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        
        try:
            QtWidgets.QMessageBox.critical(
                None, "Critical Error", 
                f"Failed to start application:\n{error}\n\nCheck logs for details."
            )
        except:
            pass
        
        sys.exit(1)
    
    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        try:
            self.logger.info("Application closing...")
            
            # Сохраняем состояние
            self.save_window_state()
            
            # Закрываем оверлей
            if self.overlay_hud:
                self.overlay_hud.close()
            
            # Закрываем базу данных
            if self.db and hasattr(self.db, 'close'):
                self.db.close()
            
            self.logger.info("Application closed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during close: {e}")
        
        event.accept()


def main():
    """Главная функция запуска"""
    # Создаем приложение
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("LMU Assistant")
    app.setApplicationVersion("3.0.0")
    app.setOrganizationName("LMU Assistant Team")
    
    # Устанавливаем стиль
    app.setStyle("Fusion")
    
    # Применяем глобальные стили
    app.setStyleSheet("""
        QApplication {
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }
        QScrollBar:vertical {
            background: #f1f5f9;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background: #cbd5e0;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background: #a0aec0;
        }
    """)
    
    # Обработка аргументов
    if "--debug" in sys.argv:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
