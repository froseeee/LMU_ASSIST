from PyQt5 import QtWidgets, QtGui, QtCore
import logging
import time
import math

try:
    import pyqtgraph as pg
    PYQTGRAPH_AVAILABLE = True
except ImportError:
    PYQTGRAPH_AVAILABLE = False

try:
    from core.telemetry_receiver import TelemetryReceiver
    from core.telemetry_buffer import TelemetryBuffer
    TELEMETRY_AVAILABLE = True
except ImportError:
    TELEMETRY_AVAILABLE = False

class OverlayHUD(QtWidgets.QWidget):
    """Современный оверлей с улучшенной производительностью и дизайном"""
    
    def __init__(self, config=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Конфигурация по умолчанию
        self.config = config or {
            'update_interval': 50,
            'position': (100, 100),
            'size': (450, 300),
            'opacity': 0.95,
            'show_plot': True,
            'plot_history_length': 100,
            'theme': 'dark',
            'compact_mode': False
        }
        
        # Состояние
        self.is_dragging = False
        self.drag_start_position = None
        self.last_data_time = 0
        self.connection_timeout = 3.0
        
        # Инициализация
        self.setup_window_properties()
        self.setup_telemetry()
        self.setup_ui()
        self.setup_animations()
        self.setup_timer()
        
        self.logger.info("Modern overlay HUD initialized")

    def setup_window_properties(self):
        """Настройка свойств окна"""
        # Флаги окна для современного оверлея
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | 
            QtCore.Qt.Tool | 
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.X11BypassWindowManagerHint  # Для лучшей производительности
        )
        
        # Прозрачность фона
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        
        # Позиция и размер
        pos = self.config['position']
        size = self.config['size']
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        
        # Прозрачность окна
        self.setWindowOpacity(self.config['opacity'])

    def setup_telemetry(self):
        """Настройка системы телеметрии"""
        self.receiver = None
        self.buffer = None
        
        if TELEMETRY_AVAILABLE:
            try:
                self.receiver = TelemetryReceiver()
                self.buffer = TelemetryBuffer()
                self.receiver.start_listening()
                self.logger.info("Telemetry system initialized")
            except Exception as e:
                self.logger.error(f"Failed to setup telemetry: {e}")
        else:
            self.logger.warning("Telemetry modules not available")

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        self.setLayout(main_layout)
        
        # Создаем компоненты
        self.create_main_display(main_layout)
        if self.config['show_plot'] and PYQTGRAPH_AVAILABLE:
            self.create_telemetry_plot(main_layout)
        self.create_status_bar(main_layout)

    def create_main_display(self, parent_layout):
        """Создание основного дисплея"""
        # Контейнер с современным дизайном
        display_container = QtWidgets.QFrame()
        display_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 41, 59, 240),
                    stop:1 rgba(15, 23, 42, 240));
                border: 1px solid rgba(71, 85, 105, 180);
                border-radius: 16px;
                padding: 8px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(display_container)
        layout.setSpacing(8)
        
        # Заголовок
        header = self.create_header()
        layout.addWidget(header)
        
        # Основные данные в сетке
        main_data_grid = self.create_main_data_grid()
        layout.addWidget(main_data_grid)
        
        # Дополнительные данные
        additional_data = self.create_additional_data()
        layout.addWidget(additional_data)
        
        parent_layout.addWidget(display_container)

    def create_header(self):
        """Создание заголовка"""
        header_widget = QtWidgets.QWidget()
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(4, 4, 4, 4)
        
        # Логотип/название
        title = QtWidgets.QLabel("🏁 LMU Telemetry")
        title.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            font-weight: bold;
        """)
        
        # Кнопки управления
        controls_layout = QtWidgets.QHBoxLayout()
        
        self.minimize_btn = self.create_control_button("−")
        self.settings_btn = self.create_control_button("⚙")
        self.close_btn = self.create_control_button("×")
        
        self.minimize_btn.clicked.connect(self.toggle_compact_mode)
        self.settings_btn.clicked.connect(self.show_settings)
        self.close_btn.clicked.connect(self.close)
        
        controls_layout.addWidget(self.minimize_btn)
        controls_layout.addWidget(self.settings_btn)
        controls_layout.addWidget(self.close_btn)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addLayout(controls_layout)
        
        return header_widget

    def create_control_button(self, text):
        """Создание кнопки управления"""
        btn = QtWidgets.QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background: rgba(71, 85, 105, 100);
                border: 1px solid rgba(148, 163, 184, 100);
                border-radius: 4px;
                color: rgba(255, 255, 255, 0.8);
                font-weight: bold;
                font-size: 12px;
                padding: 4px 8px;
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
            }
            QPushButton:hover {
                background: rgba(99, 102, 241, 150);
                border-color: rgba(129, 140, 248, 150);
            }
            QPushButton:pressed {
                background: rgba(79, 70, 229, 180);
            }
        """)
        return btn

    def create_main_data_grid(self):
        """Создание сетки основных данных"""
        grid_widget = QtWidgets.QWidget()
        grid_layout = QtWidgets.QGridLayout(grid_widget)
        grid_layout.setSpacing(12)
        
        # Создаем виджеты данных
        self.gear_widget = self.create_data_widget("GEAR", "N", "#10b981", large=True)
        self.rpm_widget = self.create_data_widget("RPM", "0", "#ef4444")
        self.speed_widget = self.create_data_widget("SPEED", "0", "#06b6d4")
        self.lap_time_widget = self.create_data_widget("LAP TIME", "--:--.---", "#f59e0b")
        
        # Размещаем в сетке
        grid_layout.addWidget(self.gear_widget, 0, 0, 2, 1)  # Gear занимает 2 строки
        grid_layout.addWidget(self.rpm_widget, 0, 1)
        grid_layout.addWidget(self.speed_widget, 0, 2)
        grid_layout.addWidget(self.lap_time_widget, 1, 1, 1, 2)  # Lap time занимает 2 колонки
        
        return grid_widget

    def create_data_widget(self, label, value, color, large=False):
        """Создание виджета данных"""
        widget = QtWidgets.QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background: rgba(30, 41, 59, 120);
                border: 1px solid {color}40;
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)
        
        # Метка
        label_widget = QtWidgets.QLabel(label)
        label_widget.setStyleSheet(f"""
            color: {color};
            font-size: {'11px' if not large else '12px'};
            font-weight: bold;
            text-align: center;
        """)
        label_widget.setAlignment(QtCore.Qt.AlignCenter)
        
        # Значение
        value_widget = QtWidgets.QLabel(value)
        value_widget.setStyleSheet(f"""
            color: white;
            font-size: {'32px' if large else '20px'};
            font-weight: bold;
            text-align: center;
        """)
        value_widget.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        
        # Сохраняем ссылки на виджеты
        widget.label_widget = label_widget
        widget.value_widget = value_widget
        widget.color = color
        
        return widget

    def create_additional_data(self):
        """Создание дополнительных данных"""
        additional_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(additional_widget)
        layout.setSpacing(8)
        
        # Прогресс-бары для педалей
        self.throttle_bar = self.create_progress_bar("THROTTLE", "#10b981")
        self.brake_bar = self.create_progress_bar("BRAKE", "#ef4444")
        
        layout.addWidget(self.throttle_bar)
        layout.addWidget(self.brake_bar)
        
        return additional_widget

    def create_progress_bar(self, label, color):
        """Создание прогресс-бара"""
        container = QtWidgets.QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background: rgba(30, 41, 59, 120);
                border: 1px solid {color}40;
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(4)
        
        # Метка
        label_widget = QtWidgets.QLabel(label)
        label_widget.setStyleSheet(f"""
            color: {color};
            font-size: 10px;
            font-weight: bold;
            text-align: center;
        """)
        label_widget.setAlignment(QtCore.Qt.AlignCenter)
        
        # Прогресс-бар
        progress = QtWidgets.QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(0)
        progress.setTextVisible(False)
        progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid rgba(100, 116, 139, 100);
                border-radius: 3px;
                background: rgba(51, 65, 85, 150);
                height: 12px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {color}80);
                border-radius: 2px;
            }}
        """)
        
        layout.addWidget(label_widget)
        layout.addWidget(progress)
        
        container.progress = progress
        return container

    def create_telemetry_plot(self, parent_layout):
        """Создание графика телеметрии"""
        if not PYQTGRAPH_AVAILABLE:
            return
            
        plot_container = QtWidgets.QFrame()
        plot_container.setStyleSheet("""
            QFrame {
                background: rgba(30, 41, 59, 240);
                border: 1px solid rgba(71, 85, 105, 180);
                border-radius: 12px;
                padding: 8px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(plot_container)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Заголовок графика
        plot_title = QtWidgets.QLabel("📈 Real-time Telemetry")
        plot_title.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 4px;
        """)
        layout.addWidget(plot_title)
        
        # График
        self.telemetry_plot = pg.PlotWidget()
        self.telemetry_plot.setBackground('transparent')
        self.telemetry_plot.setFixedHeight(100)
        
        # Настройка стиля графика
        self.telemetry_plot.getAxis('left').setPen(pg.mkPen(color='#64748b', width=1))
        self.telemetry_plot.getAxis('bottom').setPen(pg.mkPen(color='#64748b', width=1))
        self.telemetry_plot.getAxis('left').setTextPen(pg.mkPen(color='#94a3b8'))
        self.telemetry_plot.getAxis('bottom').setTextPen(pg.mkPen(color='#94a3b8'))
        
        self.telemetry_plot.showGrid(x=True, y=True, alpha=0.2)
        self.telemetry_plot.setLabel('left', 'Value', color='#94a3b8', size='10pt')
        self.telemetry_plot.setLabel('bottom', 'Time', color='#94a3b8', size='10pt')
        
        # Кривые для данных
        self.rpm_curve = self.telemetry_plot.plot(
            pen=pg.mkPen('#ef4444', width=2), 
            name='RPM'
        )
        self.throttle_curve = self.telemetry_plot.plot(
            pen=pg.mkPen('#10b981', width=2), 
            name='Throttle'
        )
        self.brake_curve = self.telemetry_plot.plot(
            pen=pg.mkPen('#3b82f6', width=2), 
            name='Brake'
        )
        
        layout.addWidget(self.telemetry_plot)
        parent_layout.addWidget(plot_container)

    def create_status_bar(self, parent_layout):
        """Создание строки состояния"""
        status_container = QtWidgets.QFrame()
        status_container.setStyleSheet("""
            QFrame {
                background: rgba(15, 23, 42, 200);
                border: 1px solid rgba(71, 85, 105, 100);
                border-radius: 8px;
                padding: 4px 8px;
            }
        """)
        
        layout = QtWidgets.QHBoxLayout(status_container)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Индикатор подключения
        self.connection_indicator = QtWidgets.QLabel("●")
        self.connection_indicator.setStyleSheet("""
            color: #ef4444;
            font-size: 12px;
        """)
        
        # Статус текст
        self.status_label = QtWidgets.QLabel("Waiting for telemetry...")
        self.status_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            font-size: 11px;
        """)
        
        # FPS счетчик
        self.fps_label = QtWidgets.QLabel("FPS: --")
        self.fps_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.5);
            font-size: 10px;
        """)
        
        layout.addWidget(self.connection_indicator)
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.fps_label)
        
        parent_layout.addWidget(status_container)

    def setup_animations(self):
        """Настройка анимаций"""
        # Анимация появления
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(self.config['opacity'])
        
        # Анимация исчезновения
        self.fade_out_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(200)
        self.fade_out_animation.setStartValue(self.config['opacity'])
        self.fade_out_animation.setEndValue(0.0)

    def setup_timer(self):
        """Настройка таймера обновления"""
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(self.config['update_interval'])
        
        # FPS счетчик
        self.frame_count = 0
        self.last_fps_time = time.time()

    def update_display(self):
        """Обновление отображения данных"""
        self.frame_count += 1
        current_time = time.time()
        
        # Обновляем FPS каждую секунду
        if current_time - self.last_fps_time >= 1.0:
            fps = self.frame_count / (current_time - self.last_fps_time)
            self.fps_label.setText(f"FPS: {fps:.0f}")
            self.frame_count = 0
            self.last_fps_time = current_time
        
        if not self.receiver:
            self.update_connection_status("No receiver", False)
            return
        
        # Получаем новые данные
        data = self.receiver.get_latest_data()
        
        if data:
            self.last_data_time = current_time
            self.buffer.add_data(data)
            self.update_data_display(data)
            self.update_telemetry_plot()
            self.update_connection_status("Connected", True)
        else:
            # Проверяем таймаут соединения
            if current_time - self.last_data_time > self.connection_timeout:
                self.update_connection_status("No data", False)

    def update_data_display(self, data):
        """Обновление текстовых данных"""
        try:
            # Передача
            gear = data.get('gear', 0)
            gear_text = 'R' if gear == -1 else 'N' if gear == 0 else str(gear)
            self.gear_widget.value_widget.setText(gear_text)
            
            # RPM с анимацией цвета
            rpm = data.get('rpm', 0)
            self.rpm_widget.value_widget.setText(f"{rpm:.0f}")
            self.animate_rpm_color(rpm)
            
            # Скорость
            speed = data.get('speed', 0)
            self.speed_widget.value_widget.setText(f"{speed:.0f}")
            
            # Время круга
            lap_time = data.get('current_lap_time', 0)
            if lap_time > 0:
                minutes = int(lap_time // 60)
                seconds = lap_time % 60
                self.lap_time_widget.value_widget.setText(f"{minutes}:{seconds:06.3f}")
            
            # Педали
            throttle = data.get('throttle', 0) * 100
            brake = data.get('brake', 0) * 100
            
            self.throttle_bar.progress.setValue(int(throttle))
            self.brake_bar.progress.setValue(int(brake))
            
        except Exception as e:
            self.logger.warning(f"Error updating display: {e}")

    def animate_rpm_color(self, rpm):
        """Анимация цвета RPM в зависимости от значения"""
        if rpm < 4000:
            color = "#06b6d4"  # Синий
        elif rpm < 6000:
            color = "#f59e0b"  # Желтый
        elif rpm < 7500:
            color = "#f97316"  # Оранжевый
        else:
            color = "#ef4444"  # Красный
        
        # Обновляем цвет границы
        self.rpm_widget.setStyleSheet(f"""
            QFrame {{
                background: rgba(30, 41, 59, 120);
                border: 2px solid {color}80;
                border-radius: 8px;
                padding: 8px;
            }}
        """)

    def update_telemetry_plot(self):
        """Обновление графика телеметрии"""
        if not hasattr(self, 'telemetry_plot') or not PYQTGRAPH_AVAILABLE:
            return
        
        try:
            history_length = self.config['plot_history_length']
            
            # Получаем данные
            rpm_data = self.buffer.get_parameter_history('rpm', history_length)
            throttle_data = self.buffer.get_parameter_history('throttle', history_length)
            brake_data = self.buffer.get_parameter_history('brake', history_length)
            
            if not rpm_data:
                return
            
            # X данные
            x_data = list(range(len(rpm_data)))
            
            # Нормализация RPM (предполагаем макс 8000)
            rpm_normalized = [rpm / 8000.0 for rpm in rpm_data]
            
            # Обновляем кривые
            self.rpm_curve.setData(x_data, rpm_normalized)
            self.throttle_curve.setData(x_data, throttle_data)
            self.brake_curve.setData(x_data, brake_data)
            
        except Exception as e:
            self.logger.warning(f"Error updating plot: {e}")

    def update_connection_status(self, status_text, connected):
        """Обновление статуса подключения"""
        color = "#10b981" if connected else "#ef4444"
        
        self.connection_indicator.setStyleSheet(f"""
            color: {color};
            font-size: 12px;
        """)
        
        self.status_label.setText(status_text)

    def toggle_compact_mode(self):
        """Переключение компактного режима"""
        self.config['compact_mode'] = not self.config['compact_mode']
        
        if self.config['compact_mode']:
            # Скрываем дополнительные элементы
            if hasattr(self, 'telemetry_plot'):
                self.telemetry_plot.parent().setVisible(False)
            self.resize(300, 150)
        else:
            # Показываем все элементы
            if hasattr(self, 'telemetry_plot'):
                self.telemetry_plot.parent().setVisible(True)
            self.resize(self.config['size'][0], self.config['size'][1])

    def show_settings(self):
        """Показ настроек оверлея"""
        settings_dialog = OverlaySettingsDialog(self.config, self)
        if settings_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.config = settings_dialog.get_config()
            self.apply_config_changes()

    def apply_config_changes(self):
        """Применение изменений конфигурации"""
        # Обновляем прозрачность
        self.setWindowOpacity(self.config['opacity'])
        
        # Обновляем интервал обновления
        self.update_timer.setInterval(self.config['update_interval'])
        
        # Обновляем размер
        if not self.config['compact_mode']:
            self.resize(self.config['size'][0], self.config['size'][1])

    def mousePressEvent(self, event):
        """Обработка нажатия мыши"""
        if event.button() == QtCore.Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_position = event.globalPos()

    def mouseMoveEvent(self, event):
        """Перемещение окна"""
        if self.is_dragging and self.drag_start_position:
            delta = event.globalPos() - self.drag_start_position
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_start_position = event.globalPos()

    def mouseReleaseEvent(self, event):
        """Отпускание мыши"""
        if event.button() == QtCore.Qt.LeftButton:
            self.is_dragging = False
            self.drag_start_position = None

    def keyPressEvent(self, event):
        """Обработка клавиш"""
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_F1:
            self.toggle_compact_mode()
        elif event.key() == QtCore.Qt.Key_F2:
            self.show_settings()

    def showEvent(self, event):
        """Событие показа окна"""
        super().showEvent(event)
        self.fade_in_animation.start()

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        try:
            if self.update_timer:
                self.update_timer.stop()
            
            if self.receiver:
                self.receiver.stop_listening()
                
            self.logger.info("Modern overlay HUD closed")
            
        except Exception as e:
            self.logger.error(f"Error during close: {e}")
        
        super().closeEvent(event)


class OverlaySettingsDialog(QtWidgets.QDialog):
    """Диалог настроек оверлея"""
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config.copy()
        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса диалога"""
        self.setWindowTitle("Overlay Settings")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        
        # Настройки
        form_layout = QtWidgets.QFormLayout()
        
        # Прозрачность
        self.opacity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.opacity_slider.setRange(30, 100)
        self.opacity_slider.setValue(int(self.config['opacity'] * 100))
        form_layout.addRow("Opacity:", self.opacity_slider)
        
        # Интервал обновления
        self.update_interval_spin = QtWidgets.QSpinBox()
        self.update_interval_spin.setRange(16, 500)
        self.update_interval_spin.setValue(self.config['update_interval'])
        self.update_interval_spin.setSuffix(" ms")
        form_layout.addRow("Update Interval:", self.update_interval_spin)
        
        # Показывать график
        self.show_plot_check = QtWidgets.QCheckBox()
        self.show_plot_check.setChecked(self.config['show_plot'])
        form_layout.addRow("Show Plot:", self.show_plot_check)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_config(self):
        """Получение обновленной конфигурации"""
        self.config['opacity'] = self.opacity_slider.value() / 100.0
        self.config['update_interval'] = self.update_interval_spin.value()
        self.config['show_plot'] = self.show_plot_check.isChecked()
        return self.config
