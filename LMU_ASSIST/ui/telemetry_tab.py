import logging
from PyQt5 import QtWidgets

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

class TelemetryTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
        # Заголовок
        title = QtWidgets.QLabel("📡 Телеметрия")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        self.layout.addWidget(title)
        
        if not TELEMETRY_AVAILABLE:
            error_label = QtWidgets.QLabel("❌ Модули телеметрии не загружены")
            error_label.setStyleSheet("color: red; font-size: 14px;")
            self.layout.addWidget(error_label)
            return
            
        if not PYQTGRAPH_AVAILABLE:
            error_label = QtWidgets.QLabel("❌ PyQtGraph не установлен")
            error_label.setStyleSheet("color: red; font-size: 14px;")
            self.layout.addWidget(error_label)
            return
        
        try:
            self.receiver = TelemetryReceiver()
            self.buffer = TelemetryBuffer()
            
            # Создаем график
            self.graph = pg.PlotWidget()
            self.graph.setLabel('left', 'Значение')
            self.graph.setLabel('bottom', 'Время')
            self.graph.showGrid(x=True, y=True)
            self.layout.addWidget(self.graph)
            
            # Статус
            self.status_label = QtWidgets.QLabel("Статус: Ожидание данных...")
            self.layout.addWidget(self.status_label)
            
            # Кнопка обновления
            self.update_button = QtWidgets.QPushButton("Обновить график")
            self.update_button.clicked.connect(self.update_graph)
            self.layout.addWidget(self.update_button)
            
            # Инструкции
            instructions = QtWidgets.QLabel(
                "Инструкции:\n"
                "• Убедитесь, что игра отправляет UDP данные на порт 20777\n"
                "• График показывает RPM (красный), газ (зеленый), тормоз (синий)\n"
                "• Нажмите 'Обновить график' для обновления данных"
            )
            instructions.setStyleSheet("background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 10px;")
            self.layout.addWidget(instructions)
            
        except Exception as e:
            error_label = QtWidgets.QLabel(f"❌ Ошибка инициализации телеметрии: {e}")
            error_label.setStyleSheet("color: red; font-size: 14px;")
            self.layout.addWidget(error_label)
            
            # Логируем ошибку
            logger = logging.getLogger(__name__)
            logger.error(f"Telemetry tab initialization error: {e}")

    def update_graph(self):
        """Обновление графика"""
        if not hasattr(self, 'receiver') or not self.receiver:
            self.status_label.setText("❌ Приемник телеметрии недоступен")
            return
            
        try:
            # Получаем данные из буфера
            rpm_data = self.buffer.get_parameter_history('rpm', 100)
            throttle_data = self.buffer.get_parameter_history('throttle', 100)
            brake_data = self.buffer.get_parameter_history('brake', 100)
            
            if not rpm_data:
                # Пытаемся получить одно значение
                data = self.receiver.get_latest_data()
                if data:
                    self.buffer.add_data(data)
                    rpm_data = [data.get("rpm", 0)]
                    throttle_data = [data.get("throttle", 0)]
                    brake_data = [data.get("brake", 0)]
                else:
                    self.status_label.setText("⚠️ Нет данных телеметрии")
                    return
            
            # Очищаем график
            self.graph.clear()
            
            # Создаем данные для отображения
            x_data = list(range(len(rpm_data)))
            
            # Нормализуем RPM для лучшего отображения
            rpm_normalized = [rpm / 8000.0 for rpm in rpm_data]
            
            # Строим графики
            self.graph.plot(x_data, rpm_normalized, pen=pg.mkPen('r', width=2), name='RPM')
            self.graph.plot(x_data, throttle_data, pen=pg.mkPen('g', width=2), name='Throttle')
            self.graph.plot(x_data, brake_data, pen=pg.mkPen('b', width=2), name='Brake')
            
            # Обновляем статус
            self.status_label.setText(f"✅ График обновлен: {len(rpm_data)} точек данных")
            
        except Exception as e:
            self.status_label.setText(f"❌ Ошибка обновления: {e}")
            
            # Логируем ошибку
            logger = logging.getLogger(__name__)
            logger.error(f"Graph update error: {e}")