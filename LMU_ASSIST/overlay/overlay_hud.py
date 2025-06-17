from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
from core.telemetry_receiver import TelemetryReceiver
from core.telemetry_buffer import TelemetryBuffer
import logging

class OverlayHUD(QtWidgets.QWidget):
    def __init__(self, config=None):
        super().__init__()
        
        # Конфигурация по умолчанию
        self.config = config or {
            'update_interval': 50,  # мс
            'position': (50, 50),
            'size': (400, 200),
            'opacity': 0.9,
            'show_plot': True,
            'plot_history_length': 100
        }
        
        self.setup_ui()
        self.setup_telemetry()
        self.setup_timer()
        
        self.logger = logging.getLogger(__name__)
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Настройка окна
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | 
            QtCore.Qt.Tool | 
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # Позиция и размер из конфигурации
        pos = self.config['position']
        size = self.config['size']
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        
        # Прозрачность
        self.setWindowOpacity(self.config['opacity'])
        
        # Основной layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Контейнер для данных
        data_container = QtWidgets.QFrame()
        data_container.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 8px;
                border: 2px solid rgba(255, 255, 255, 100);
            }
        """)
        
        data_layout = QtWidgets.QVBoxLayout(data_container)
        
        # Основные данные
        self.gear_label = QtWidgets.QLabel("Gear: N")
        self.gear_label.setStyleSheet("""
            color: #00FF00; 
            font-size: 24px; 
            font-weight: bold;
            margin: 2px;
        """)
        data_layout.addWidget(self.gear_label)
        
        self.rpm_label = QtWidgets.QLabel("RPM: 0")
        self.rpm_label.setStyleSheet("""
            color: #FF4444; 
            font-size: 18px; 
            font-weight: bold;
            margin: 2px;
        """)
        data_layout.addWidget(self.rpm_label)
        
        self.speed_label = QtWidgets.QLabel("Speed: 0 km/h")
        self.speed_label.setStyleSheet("""
            color: #44DDFF; 
            font-size: 18px; 
            font-weight: bold;
            margin: 2px;
        """)
        data_layout.addWidget(self.speed_label)
        
        # Дополнительная информация
        info_layout = QtWidgets.QHBoxLayout()
        
        self.throttle_label = QtWidgets.QLabel("T: 0%")
        self.throttle_label.setStyleSheet("color: #44FF44; font-size: 14px;")
        info_layout.addWidget(self.throttle_label)
        
        self.brake_label = QtWidgets.QLabel("B: 0%")
        self.brake_label.setStyleSheet("color: #FF4444; font-size: 14px;")
        info_layout.addWidget(self.brake_label)
        
        self.lap_time_label = QtWidgets.QLabel("Lap: --:--.---")
        self.lap_time_label.setStyleSheet("color: #FFFF44; font-size: 14px;")
        info_layout.addWidget(self.lap_time_label)
        
        data_layout.addLayout(info_layout)
        main_layout.addWidget(data_container)
        
        # График телеметрии (опционально)
        if self.config['show_plot']:
            self.setup_plot()
            main_layout.addWidget(self.telemetry_plot)
        
        # Статус подключения
        self.status_label = QtWidgets.QLabel("Status: Disconnected")
        self.status_label.setStyleSheet("""
            color: #FF4444; 
            font-size: 12px; 
            background-color: rgba(0, 0, 0, 100);
            padding: 2px 8px;
            border-radius: 4px;
        """)
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
    
    def setup_plot(self):
        """Настройка графика телеметрии"""
        self.telemetry_plot = pg.PlotWidget()
        self.telemetry_plot.setBackground('k')
        self.telemetry_plot.setFixedHeight(120)
        
        # Настройка осей
        self.telemetry_plot.setLabel('left', 'Value')
        self.telemetry_plot.setLabel('bottom', 'Time')
        self.telemetry_plot.showGrid(x=True, y=True, alpha=0.3)
        
        # Кривые для отображения
        self.rpm_curve = self.telemetry_plot.plot(pen=pg.mkPen('#FF4444', width=2), name='RPM')
        self.throttle_curve = self.telemetry_plot.plot(pen=pg.mkPen('#44FF44', width=2), name='Throttle')
        self.brake_curve = self.telemetry_plot.plot(pen=pg.mkPen('#4444FF', width=2), name='Brake')
        
        # Легенда
        self.telemetry_plot.addLegend()
    
    def setup_telemetry(self):
        """Настройка системы телеметрии"""
        try:
            self.receiver = TelemetryReceiver()
            self.buffer = TelemetryBuffer()
            self.receiver.start_listening()
            
            self.last_data_time = 0
            self.connection_timeout = 2.0  # секунды
            
        except Exception as e:
            self.logger.error(f"Failed to setup telemetry: {e}")
            self.receiver = None
            self.buffer = None
    
    def setup_timer(self):
        """Настройка таймера обновления"""
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(self.config['update_interval'])
    
    def update_display(self):
        """Обновление отображения данных"""
        if not self.receiver:
            self.update_status("No receiver")
            return
        
        # Получаем новые данные
        data = self.receiver.get_latest_data()
        
        if data:
            self.last_data_time = data.get('timestamp', 0)
            self.buffer.add_data(data)
            self.update_data_display(data)
            self.update_plot()
            self.update_status("Connected")
        else:
            # Проверяем таймаут соединения
            import time
            if time.time() - self.last_data_time > self.connection_timeout:
                self.update_status("No data")
    
    def update_data_display(self, data):
        """Обновление текстовых данных"""
        try:
            # Основные данные
            gear = data.get('gear', 0)
            gear_text = 'R' if gear == -1 else 'N' if gear == 0 else str(gear)
            self.gear_label.setText(f"Gear: {gear_text}")
            
            rpm = data.get('rpm', 0)
            self.rpm_label.setText(f"RPM: {rpm:.0f}")
            
            speed = data.get('speed', 0)
            self.speed_label.setText(f"Speed: {speed:.0f} km/h")
            
            # Дополнительные данные
            throttle = data.get('throttle', 0) * 100
            self.throttle_label.setText(f"T: {throttle:.0f}%")
            
            brake = data.get('brake', 0) * 100
            self.brake_label.setText(f"B: {brake:.0f}%")
            
            # Время круга
            lap_time = data.get('current_lap_time', 0)
            if lap_time > 0:
                minutes = int(lap_time // 60)
                seconds = lap_time % 60
                self.lap_time_label.setText(f"Lap: {minutes}:{seconds:06.3f}")
            
        except Exception as e:
            self.logger.warning(f"Error updating display: {e}")
    
    def update_plot(self):
        """Обновление графика"""
        if not self.config['show_plot'] or not hasattr(self, 'telemetry_plot'):
            return
        
        try:
            history_length = self.config['plot_history_length']
            
            # Получаем данные для отображения
            rpm_data = self.buffer.get_parameter_history('rpm', history_length)
            throttle_data = self.buffer.get_parameter_history('throttle', history_length)
            brake_data = self.buffer.get_parameter_history('brake', history_length)
            
            if not rpm_data:
                return
            
            # Нормализация данных для лучшего отображения
            x_data = list(range(len(rpm_data)))
            
            # RPM нормализуем к 0-1 (предполагаем макс 8000 RPM)
            rpm_normalized = [rpm / 8000.0 for rpm in rpm_data]
            
            # Обновляем кривые
            self.rpm_curve.setData(x_data, rpm_normalized)
            self.throttle_curve.setData(x_data, throttle_data)
            self.brake_curve.setData(x_data, brake_data)
            
        except Exception as e:
            self.logger.warning(f"Error updating plot: {e}")
    
    def update_status(self, status_text):
        """Обновление статуса подключения"""
        status_colors = {
            "Connected": "#44FF44",
            "No data": "#FFAA44", 
            "No receiver": "#FF4444",
            "Disconnected": "#FF4444"
        }
        
        color = status_colors.get(status_text, "#FF4444")
        self.status_label.setText(f"Status: {status_text}")
        self.status_label.setStyleSheet(f"""
            color: {color}; 
            font-size: 12px; 
            background-color: rgba(0, 0, 0, 100);
            padding: 2px 8px;
            border-radius: 4px;
        """)
    
    def mousePressEvent(self, event):
        """Обработка нажатия мыши для перемещения окна"""
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.globalPos()
    
    def mouseMoveEvent(self, event):
        """Перемещение окна"""
        if hasattr(self, 'drag_start_position'):
            delta = QtCore.QPoint(event.globalPos() - self.drag_start_position)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_start_position = event.globalPos()
    
    def keyPressEvent(self, event):
        """Обработка клавиш"""
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_F1:
            self.toggle_plot()
    
    def toggle_plot(self):
        """Переключение отображения графика"""
        if hasattr(self, 'telemetry_plot'):
            self.telemetry_plot.setVisible(not self.telemetry_plot.isVisible())
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        try:
            if self.update_timer:
                self.update_timer.stop()
            
            if self.receiver:
                self.receiver.stop_listening()
                
        except Exception as e:
            self.logger.error(f"Error during close: {e}")
        
        super().closeEvent(event)

# Пример использования
if __name__ == "__main__":
    import sys
    
    # Конфигурация для тестирования
    test_config = {
        'update_interval': 100,
        'position': (100, 100),
        'size': (450, 250),
        'opacity': 0.95,
        'show_plot': True,
        'plot_history_length': 150
    }
    
    app = QtWidgets.QApplication(sys.argv)
    hud = OverlayHUD(test_config)
    hud.show()
    sys.exit(app.exec_())
