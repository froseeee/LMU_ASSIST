from PyQt5 import QtWidgets, QtCore
from overlay.overlay_hud import OverlayHUD

class OverlayControl(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self.hud = None
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Заголовок
        title = QtWidgets.QLabel("Управление оверлеем")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Кнопка переключения
        self.toggle_button = QtWidgets.QPushButton("Оверлей: Включить")
        self.toggle_button.setMinimumHeight(40)
        layout.addWidget(self.toggle_button)
        self.toggle_button.clicked.connect(self.toggle_overlay)

        # Информация о состоянии
        self.status_label = QtWidgets.QLabel("Состояние: Выключен")
        layout.addWidget(self.status_label)

        # Настройки оверлея
        settings_group = QtWidgets.QGroupBox("Настройки")
        settings_layout = QtWidgets.QFormLayout()
        
        self.opacity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.opacity_slider.setRange(30, 100)
        self.opacity_slider.setValue(90)
        self.opacity_slider.valueChanged.connect(self.update_opacity)
        settings_layout.addRow("Прозрачность:", self.opacity_slider)
        
        # Переключатель графика
        self.plot_checkbox = QtWidgets.QCheckBox("Показывать график")
        self.plot_checkbox.setChecked(True)
        settings_layout.addRow("График:", self.plot_checkbox)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Инструкции
        instructions = QtWidgets.QLabel(
            "Инструкции:\n"
            "• F10 - Переключить оверлей\n"
            "• F11 - Показать/скрыть график\n"
            "• ЛКМ - Перемещение окна\n"
            "• ESC - Закрыть оверлей"
        )
        instructions.setStyleSheet("background: #f0f0f0; padding: 10px; border-radius: 5px;")
        layout.addWidget(instructions)

        layout.addStretch()
        self.setLayout(layout)

    def toggle_overlay(self):
        try:
            if self.hud is None:
                # Получаем конфигурацию из родительского окна
                config = None
                if self.parent_window and hasattr(self.parent_window, 'config_manager'):
                    config = self.parent_window.config_manager.get_overlay_config()
                    # Применяем настройки из UI
                    config['opacity'] = self.opacity_slider.value() / 100.0
                    config['show_plot'] = self.plot_checkbox.isChecked()
                
                self.hud = OverlayHUD(config)
                self.hud.show()
                self.toggle_button.setText("Оверлей: Выключить")
                self.status_label.setText("Состояние: Включен")
            else:
                self.hud.close()
                self.hud = None
                self.toggle_button.setText("Оверлей: Включить")
                self.status_label.setText("Состояние: Выключен")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось переключить оверлей: {e}")

    def update_opacity(self, value):
        """Обновление прозрачности оверлея"""
        if self.hud:
            self.hud.setWindowOpacity(value / 100.0)

    def cleanup(self):
        """Очистка ресурсов при закрытии"""
        if self.hud:
            self.hud.close()
            self.hud = None
