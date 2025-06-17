from PyQt5 import QtWidgets, QtCore

class PreferencesDialog(QtWidgets.QDialog):
    """Диалог настроек приложения"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки LMU Assistant")
        self.setModal(True)
        self.resize(500, 400)
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        
        # Создаем вкладки
        tabs = QtWidgets.QTabWidget()
        
        # Вкладка общих настроек
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "Общие")
        
        # Вкладка телеметрии
        telemetry_tab = self.create_telemetry_tab()
        tabs.addTab(telemetry_tab, "Телеметрия")
        
        # Вкладка интерфейса
        ui_tab = self.create_ui_tab()
        tabs.addTab(ui_tab, "Интерфейс")
        
        layout.addWidget(tabs)
        
        # Кнопки
        buttons_layout = QtWidgets.QHBoxLayout()
        
        ok_btn = QtWidgets.QPushButton("OK")
        cancel_btn = QtWidgets.QPushButton("Отмена")
        apply_btn = QtWidgets.QPushButton("Применить")
        
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        apply_btn.clicked.connect(self.apply_settings)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(apply_btn)
        
        layout.addLayout(buttons_layout)
    
    def create_general_tab(self):
        """Создание вкладки общих настроек"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(widget)
        
        # Язык
        self.language_combo = QtWidgets.QComboBox()
        self.language_combo.addItems(["Русский", "English"])
        layout.addRow("Язык:", self.language_combo)
        
        # Автосохранение
        self.auto_save_check = QtWidgets.QCheckBox("Включить автосохранение")
        self.auto_save_check.setChecked(True)
        layout.addRow(self.auto_save_check)
        
        # Путь для сохранения
        save_path_layout = QtWidgets.QHBoxLayout()
        self.save_path_edit = QtWidgets.QLineEdit("./data/")
        browse_btn = QtWidgets.QPushButton("Обзор...")
        save_path_layout.addWidget(self.save_path_edit)
        save_path_layout.addWidget(browse_btn)
        layout.addRow("Путь сохранения:", save_path_layout)
        
        return widget
    
    def create_telemetry_tab(self):
        """Создание вкладки настроек телеметрии"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(widget)
        
        # Порт по умолчанию
        self.default_port_spin = QtWidgets.QSpinBox()
        self.default_port_spin.setRange(1000, 65535)
        self.default_port_spin.setValue(20777)
        layout.addRow("Порт по умолчанию:", self.default_port_spin)
        
        # Частота обновления
        self.update_rate_spin = QtWidgets.QSpinBox()
        self.update_rate_spin.setRange(10, 1000)
        self.update_rate_spin.setValue(100)
        self.update_rate_spin.setSuffix(" мс")
        layout.addRow("Частота обновления:", self.update_rate_spin)
        
        # Размер буфера
        self.buffer_size_spin = QtWidgets.QSpinBox()
        self.buffer_size_spin.setRange(100, 10000)
        self.buffer_size_spin.setValue(1000)
        layout.addRow("Размер буфера:", self.buffer_size_spin)
        
        return widget
    
    def create_ui_tab(self):
        """Создание вкладки настроек интерфейса"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(widget)
        
        # Тема
        self.theme_combo = QtWidgets.QComboBox()
        self.theme_combo.addItems(["Темная", "Светлая", "Системная"])
        layout.addRow("Тема:", self.theme_combo)
        
        # Размер шрифта
        self.font_size_spin = QtWidgets.QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(10)
        layout.addRow("Размер шрифта:", self.font_size_spin)
        
        return widget
    
    def apply_settings(self):
        """Применение настроек"""
        # Здесь должна быть логика применения настроек
        QtWidgets.QMessageBox.information(self, "Настройки", "Настройки применены!")
