from PyQt5 import QtWidgets, QtCore, QtGui
from core.setupexpert import SetupExpert
from core.exceptions import FileError, ValidationError
import json
import re
from pathlib import Path

class ModernCard(QtWidgets.QFrame):
    """Современная карточка с glass эффектом"""
    
    def __init__(self, title="", subtitle="", parent=None):
        super().__init__(parent)
        self.setProperty("class", "glass-card")
        self.setup_ui(title, subtitle)
    
    def setup_ui(self, title, subtitle):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        if title:
            title_label = QtWidgets.QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    color: #F8FAFC;
                    font-size: 20px;
                    font-weight: 600;
                    margin-bottom: 8px;
                }
            """)
            layout.addWidget(title_label)
        
        if subtitle:
            subtitle_label = QtWidgets.QLabel(subtitle)
            subtitle_label.setStyleSheet("""
                QLabel {
                    color: #CBD5E1;
                    font-size: 14px;
                    margin-bottom: 16px;
                }
            """)
            layout.addWidget(subtitle_label)

class ModernButton(QtWidgets.QPushButton):
    """Современная кнопка с анимациями"""
    
    def __init__(self, text="", icon=None, style="primary", parent=None):
        super().__init__(text, parent)
        self.style_type = style
        self.setup_style()
        
        if icon:
            self.setIcon(icon)
            self.setIconSize(QtCore.QSize(20, 20))
    
    def setup_style(self):
        if self.style_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3B82F6, stop:1 #1D4ED8);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 16px 24px;
                    font-weight: 600;
                    font-size: 16px;
                    min-height: 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #2563EB, stop:1 #1E40AF);
                    transform: translateY(-2px);
                    box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4);
                }
                QPushButton:pressed {
                    transform: translateY(0px);
                }
            """)
        elif self.style_type == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(30, 41, 59, 0.8);
                    color: #F8FAFC;
                    border: 1px solid #475569;
                    border-radius: 12px;
                    padding: 16px 24px;
                    font-weight: 500;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background: rgba(51, 65, 85, 0.9);
                    border-color: #64748B;
                    transform: translateY(-1px);
                }
            """)
        elif self.style_type == "ghost":
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #CBD5E1;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 16px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: rgba(51, 65, 85, 0.5);
                    color: #F8FAFC;
                }
            """)

class ModernInput(QtWidgets.QWidget):
    """Современное поле ввода с лейблом"""
    
    def __init__(self, label="", input_type="line", parent=None):
        super().__init__(parent)
        self.setup_ui(label, input_type)
    
    def setup_ui(self, label, input_type):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        if label:
            label_widget = QtWidgets.QLabel(label)
            label_widget.setStyleSheet("""
                QLabel {
                    color: #CBD5E1;
                    font-size: 14px;
                    font-weight: 500;
                }
            """)
            layout.addWidget(label_widget)
        
        if input_type == "combo":
            self.input = QtWidgets.QComboBox()
        elif input_type == "spin":
            self.input = QtWidgets.QSpinBox()
        else:
            self.input = QtWidgets.QLineEdit()
        
        self.input.setStyleSheet("""
            QLineEdit, QComboBox, QSpinBox {
                background: rgba(30, 41, 59, 0.8);
                color: #F8FAFC;
                border: 1px solid #475569;
                border-radius: 12px;
                padding: 14px 16px;
                font-size: 16px;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #3B82F6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #CBD5E1;
                margin-right: 8px;
            }
        """)
        
        layout.addWidget(self.input)

class ModernSlider(QtWidgets.QWidget):
    """Современный слайдер с индикатором"""
    
    valueChanged = QtCore.pyqtSignal(int)
    
    def __init__(self, label="", min_val=0, max_val=100, value=50, suffix="", parent=None):
        super().__init__(parent)
        self.suffix = suffix
        self.setup_ui(label, min_val, max_val, value)
    
    def setup_ui(self, label, min_val, max_val, value):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Заголовок с значением
        header_layout = QtWidgets.QHBoxLayout()
        
        if label:
            label_widget = QtWidgets.QLabel(label)
            label_widget.setStyleSheet("""
                QLabel {
                    color: #CBD5E1;
                    font-size: 14px;
                    font-weight: 500;
                }
            """)
            header_layout.addWidget(label_widget)
        
        header_layout.addStretch()
        
        self.value_label = QtWidgets.QLabel(f"{value}{self.suffix}")
        self.value_label.setStyleSheet("""
            QLabel {
                color: #3B82F6;
                font-size: 16px;
                font-weight: 600;
                background: rgba(59, 130, 246, 0.1);
                border-radius: 6px;
                padding: 4px 12px;
            }
        """)
        header_layout.addWidget(self.value_label)
        
        layout.addLayout(header_layout)
        
        # Слайдер
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(value)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: rgba(51, 65, 85, 0.8);
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3B82F6, stop:1 #1D4ED8);
                width: 24px;
                height: 24px;
                border-radius: 12px;
                margin: -8px 0;
                border: 3px solid white;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563EB, stop:1 #1E40AF);
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3B82F6, stop:1 #1D4ED8);
                border-radius: 4px;
            }
        """)
        
        self.slider.valueChanged.connect(self.on_value_changed)
        layout.addWidget(self.slider)
    
    def on_value_changed(self, value):
        self.value_label.setText(f"{value}{self.suffix}")
        self.valueChanged.emit(value)
    
    def value(self):
        return self.slider.value()
    
    def setValue(self, value):
        self.slider.setValue(value)

class StatsCard(QtWidgets.QFrame):
    """Карточка статистики"""
    
    def __init__(self, title, value, icon="", color="#3B82F6", parent=None):
        super().__init__(parent)
        self.setup_ui(title, value, icon, color)
    
    def setup_ui(self, title, value, icon, color):
        self.setStyleSheet(f"""
            QFrame {{
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 16px;
                padding: 20px;
            }}
            QFrame:hover {{
                border-color: rgba(59, 130, 246, 0.4);
                background: rgba(30, 41, 59, 0.9);
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Заголовок с иконкой
        header_layout = QtWidgets.QHBoxLayout()
        
        if icon:
            icon_label = QtWidgets.QLabel(icon)
            icon_label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-size: 24px;
                    font-weight: bold;
                }}
            """)
            header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Значение
        value_label = QtWidgets.QLabel(str(value))
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 32px;
                font-weight: 700;
                line-height: 1;
            }}
        """)
        layout.addWidget(value_label)
        
        # Заголовок
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #94A3B8;
                font-size: 14px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        layout.addWidget(title_label)

class GarageTab(QtWidgets.QWidget):
    """Современная вкладка Setup Expert с минималистичным дизайном"""
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        
        try:
            self.expert = SetupExpert(str(Path("data/lmu_data.json")))
        except FileError as e:
            self.expert = SetupExpert()  # Используем дефолтные данные
            QtWidgets.QMessageBox.warning(self, "Warning", f"Could not load data file: {e}")
        
        self.init_ui()

    def init_ui(self):
        # Основной layout с современными отступами
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(32)
        self.setLayout(main_layout)

        # Заголовок с градиентом
        self.create_modern_header(main_layout)
        
        # Основной контент
        self.create_modern_content(main_layout)

    def create_modern_header(self, parent_layout):
        """Создание современного заголовка"""
        header_frame = QtWidgets.QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 0.8),
                    stop:0.5 rgba(139, 92, 246, 0.8),
                    stop:1 rgba(236, 72, 153, 0.8));
                border-radius: 24px;
                padding: 32px;
                margin-bottom: 16px;
            }
        """)
        header_frame.setFixedHeight(200)
        
        header_layout = QtWidgets.QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Левая часть
        left_section = QtWidgets.QVBoxLayout()
        
        title = QtWidgets.QLabel("🏎️ Setup Expert")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: 700;
                margin: 0;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
        """)
        
        subtitle = QtWidgets.QLabel("AI-powered car setup optimization for peak performance")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: 400;
                margin-top: 8px;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            }
        """)
        
        left_section.addWidget(title)
        left_section.addWidget(subtitle)
        left_section.addStretch()
        
        # Правая часть со статистикой
        stats_layout = QtWidgets.QHBoxLayout()
        stats_layout.setSpacing(24)
        
        total_cars = len(self.expert.get_available_cars())
        total_tracks = len(self.expert.get_available_tracks())
        
        cars_stat = self.create_modern_stat_badge(str(total_cars), "Cars", "🏎️")
        tracks_stat = self.create_modern_stat_badge(str(total_tracks), "Tracks", "🏁")
        confidence_stat = self.create_modern_stat_badge("95%", "Accuracy", "🎯")
        
        stats_layout.addWidget(cars_stat)
        stats_layout.addWidget(tracks_stat)
        stats_layout.addWidget(confidence_stat)
        
        header_layout.addLayout(left_section, 2)
        header_layout.addLayout(stats_layout, 1)
        
        parent_layout.addWidget(header_frame)

    def create_modern_stat_badge(self, value, label, icon):
        """Создание современного значка статистики"""
        badge = QtWidgets.QFrame()
        badge.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 16px;
                backdrop-filter: blur(10px);
            }
        """)
        badge.setFixedSize(120, 100)
        
        layout = QtWidgets.QVBoxLayout(badge)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: 700;
            }
        """)
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        
        label_label = QtWidgets.QLabel(label)
        label_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        label_label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(label_label)
        
        return badge

    def create_modern_content(self, parent_layout):
        """Создание современного контента"""
        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setSpacing(32)
        
        # Левая панель с настройками
        left_panel = self.create_configuration_panel()
        content_layout.addWidget(left_panel, 1)
        
        # Центральная панель с результатами
        center_panel = self.create_results_panel()
        content_layout.addWidget(center_panel, 2)
        
        # Правая панель с AI рекомендациями
        right_panel = self.create_ai_panel()
        content_layout.addWidget(right_panel, 1)
        
        parent_layout.addLayout(content_layout)

    def create_configuration_panel(self):
        """Создание панели конфигурации"""
        panel = ModernCard("⚙️ Configuration", "Set up your car and track parameters")
        
        # Селекторы
        self.create_modern_selectors(panel.layout())
        
        # Условия гонки
        self.create_race_conditions(panel.layout())
        
        # Кнопки
        self.create_action_buttons(panel.layout())
        
        return panel

    def create_modern_selectors(self, parent_layout):
        """Создание современных селекторов"""
        # Автомобиль
        self.car_input = ModernInput("🏎️ Vehicle", "combo")
        
        # Группируем машины по категориям
        car_groups = self.group_cars_by_category()
        for category, cars in car_groups.items():
            if cars:
                self.car_input.input.addItem(f"─── {category} ───")
                self.car_input.input.model().item(self.car_input.input.count()-1).setEnabled(False)
                for car in cars:
                    self.car_input.input.addItem(f"  {car}")
        
        self.car_input.input.currentTextChanged.connect(self.on_car_changed)
        parent_layout.addWidget(self.car_input)
        
        # Трасса
        self.track_input = ModernInput("🏁 Track", "combo")
        
        available_tracks = self.expert.get_available_tracks()
        for track in available_tracks:
            try:
                track_info = self.expert.get_track_recommendations(track)
                display_name = track_info.get('name', track)
                self.track_input.input.addItem(display_name, track)
            except Exception as e:
                self.track_input.input.addItem(track, track)
        
        self.track_input.input.currentTextChanged.connect(self.on_track_changed)
        parent_layout.addWidget(self.track_input)

    def create_race_conditions(self, parent_layout):
        """Создание секции условий гонки"""
        conditions_title = QtWidgets.QLabel("🌤️ Race Conditions")
        conditions_title.setStyleSheet("""
            QLabel {
                color: #F8FAFC;
                font-size: 18px;
                font-weight: 600;
                margin: 24px 0 16px 0;
            }
        """)
        parent_layout.addWidget(conditions_title)
        
        # Температура
        self.temp_slider = ModernSlider("Temperature", -10, 60, 25, "°C")
        parent_layout.addWidget(self.temp_slider)
        
        # Погода
        self.weather_input = ModernInput("Weather", "combo")
        self.weather_input.input.addItems(["☀️ Dry", "🌦️ Light Rain", "🌧️ Heavy Rain", "🌪️ Variable"])
        parent_layout.addWidget(self.weather_input)
        
        # Стратегия
        self.strategy_input = ModernInput("Race Strategy", "combo")
        self.strategy_input.input.addItems(["🏃 Sprint (30min)", "⏱️ Medium (6h)", "🕐 Endurance (24h)"])
        parent_layout.addWidget(self.strategy_input)

    def create_action_buttons(self, parent_layout):
        """Создание кнопок действий"""
        parent_layout.addSpacing(24)
        
        # Основная кнопка анализа
        self.analyze_btn = ModernButton("🔬 Analyze Setup", style="primary")
        self.analyze_btn.clicked.connect(self.run_optimization)
        parent_layout.addWidget(self.analyze_btn)
        
        # Вторичные кнопки
        secondary_layout = QtWidgets.QHBoxLayout()
        secondary_layout.setSpacing(12)
        
        self.save_btn = ModernButton("💾 Save", style="secondary")
        self.share_btn = ModernButton("📤 Export", style="secondary")
        self.reset_btn = ModernButton("🔄 Reset", style="ghost")
        
        secondary_layout.addWidget(self.save_btn)
        secondary_layout.addWidget(self.share_btn)
        secondary_layout.addWidget(self.reset_btn)
        
        parent_layout.addLayout(secondary_layout)

    def create_results_panel(self):
        """Создание панели результатов"""
        panel = ModernCard("📊 Analysis Results", "AI-powered setup recommendations")
        
        # Область результатов с прокруткой
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(51, 65, 85, 0.5);
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(59, 130, 246, 0.8);
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3B82F6;
            }
        """)
        
        self.results_widget = QtWidgets.QWidget()
        self.results_layout = QtWidgets.QVBoxLayout(self.results_widget)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(16)
        
        # Начальное состояние
        self.show_welcome_state()
        
        scroll_area.setWidget(self.results_widget)
        panel.layout().addWidget(scroll_area)
        
        return panel

    def show_welcome_state(self):
        """Показать начальное состояние"""
        # Очистить предыдущие результаты
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().setParent(None)
        
        welcome_frame = QtWidgets.QFrame()
        welcome_frame.setStyleSheet("""
            QFrame {
                background: rgba(59, 130, 246, 0.05);
                border: 2px dashed rgba(59, 130, 246, 0.2);
                border-radius: 16px;
                padding: 48px 24px;
            }
        """)
        
        welcome_layout = QtWidgets.QVBoxLayout(welcome_frame)
        welcome_layout.setSpacing(16)
        
        # Иконка
        icon_label = QtWidgets.QLabel("🚀")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 64px;
                color: #3B82F6;
            }
        """)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        welcome_layout.addWidget(icon_label)
        
        # Заголовок
        title_label = QtWidgets.QLabel("Ready to Optimize")
        title_label.setStyleSheet("""
            QLabel {
                color: #F8FAFC;
                font-size: 24px;
                font-weight: 700;
                text-align: center;
            }
        """)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        welcome_layout.addWidget(title_label)
        
        # Описание
        desc_label = QtWidgets.QLabel("""
        Select your car and track, adjust the race conditions, 
        then click Analyze Setup to get AI-powered recommendations 
        for optimal performance.
        """)
        desc_label.setStyleSheet("""
            QLabel {
                color: #CBD5E1;
                font-size: 16px;
                text-align: center;
                line-height: 1.5;
            }
        """)
        desc_label.setAlignment(QtCore.Qt.AlignCenter)
        desc_label.setWordWrap(True)
        welcome_layout.addWidget(desc_label)
        
        # Фичи
        features_layout = QtWidgets.QHBoxLayout()
        features_layout.setSpacing(24)
        
        features = [
            ("🧠", "AI Analysis", "Machine learning powered recommendations"),
            ("⚡", "Real-time", "Instant setup optimization"),
            ("🎯", "Precision", "Track-specific adjustments")
        ]
        
        for icon, title, desc in features:
            feature_card = self.create_feature_card(icon, title, desc)
            features_layout.addWidget(feature_card)
        
        welcome_layout.addLayout(features_layout)
        
        self.results_layout.addWidget(welcome_frame)

    def create_feature_card(self, icon, title, description):
        """Создание карточки фичи"""
        card = QtWidgets.QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(30, 41, 59, 0.6);
                border: 1px solid rgba(59, 130, 246, 0.1);
                border-radius: 12px;
                padding: 16px;
            }
            QFrame:hover {
                background: rgba(30, 41, 59, 0.8);
                border-color: rgba(59, 130, 246, 0.3);
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(8)
        
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #F8FAFC;
                font-size: 14px;
                font-weight: 600;
                text-align: center;
            }
        """)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)
        
        desc_label = QtWidgets.QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: #94A3B8;
                font-size: 12px;
                text-align: center;
            }
        """)
        desc_label.setAlignment(QtCore.Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return card

    def create_ai_panel(self):
        """Создание AI панели"""
        panel = ModernCard("🤖 AI Assistant", "Smart recommendations and tips")
        
        # AI чат интерфейс
        self.ai_messages = QtWidgets.QScrollArea()
        self.ai_messages.setWidgetResizable(True)
        self.ai_messages.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ai_messages.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)
        
        self.ai_content = QtWidgets.QWidget()
        self.ai_layout = QtWidgets.QVBoxLayout(self.ai_content)
        self.ai_layout.setContentsMargins(0, 0, 0, 0)
        self.ai_layout.setSpacing(12)
        
        # Начальные советы
        self.show_initial_tips()
        
        self.ai_messages.setWidget(self.ai_content)
        panel.layout().addWidget(self.ai_messages)
        
        return panel

    def show_initial_tips(self):
        """Показать начальные советы"""
        tips = [
            ("🏎️", "Car Balance", "Start with base setup and adjust aerodynamics for track characteristics"),
            ("🌡️", "Temperature", "Hot weather requires higher tire pressure and less downforce"),
            ("🏁", "Track Type", "Fast tracks need minimal drag, technical tracks need more downforce"),
            ("⏱️", "Strategy", "Endurance races prioritize tire wear over raw speed"),
            ("🎯", "Fine-tuning", "Make small adjustments and test systematically")
        ]
        
        for icon, title, tip in tips:
            tip_card = self.create_tip_message(icon, title, tip)
            self.ai_layout.addWidget(tip_card)
        
        self.ai_layout.addStretch()

    def create_tip_message(self, icon, title, message):
        """Создание сообщения-совета"""
        card = QtWidgets.QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(30, 41, 59, 0.4);
                border-left: 3px solid #3B82F6;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 8px;
            }
        """)
        
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Иконка
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #3B82F6;
            }
        """)
        icon_label.setFixedSize(32, 32)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Текст
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(2)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #F8FAFC;
                font-size: 13px;
                font-weight: 600;
            }
        """)
        
        message_label = QtWidgets.QLabel(message)
        message_label.setStyleSheet("""
            QLabel {
                color: #CBD5E1;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        message_label.setWordWrap(True)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(message_label)
        
        layout.addLayout(text_layout)
        
        return card

    def group_cars_by_category(self):
        """Группировка автомобилей по категориям"""
        try:
            cars_data = self.expert.data.get("cars", {})
            groups = {
                "Hypercar": [],
                "LMP2": [],
                "LMGT3": [],
                "GTE": []
            }
            
            for car_id, car_data in cars_data.items():
                category = car_data.get("category", "Unknown")
                car_name = car_data.get("name", car_id)
                manufacturer = car_data.get("manufacturer", "")
                
                display_name = car_name
                
                if car_data.get("free_car"):
                    display_name += " 🆓"
                if car_data.get("status") == "coming_soon":
                    display_name += " ⏳"
                
                power = car_data.get("power")
                if power:
                    display_name += f" ({power}hp)"
                    
                if category in groups:
                    groups[category].append(display_name)
            
            for category in groups:
                groups[category].sort(key=lambda x: x.split()[0])
            
            return groups
        except Exception as e:
            return {"LMGT3": ["McLaren 720S LMGT3 Evo 🆓"]}

    def on_car_changed(self):
        """Обработка смены автомобиля"""
        try:
            self.load_car_info()
            self.update_ai_suggestions("car_changed")
        except Exception as e:
            print(f"Error in car change: {e}")

    def on_track_changed(self):
        """Обработка смены трассы"""
        try:
            self.load_track_info()
            self.update_ai_suggestions("track_changed")
        except Exception as e:
            print(f"Error in track change: {e}")

    def load_car_info(self):
        """Загрузка информации об автомобиле"""
        # Реализация загрузки информации об автомобиле
        pass

    def load_track_info(self):
        """Загрузка информации о трассе"""
        # Реализация загрузки информации о трассе
        pass

    def update_ai_suggestions(self, context):
        """Обновление AI предложений"""
        # Добавляем новое сообщение от AI
        if context == "car_changed":
            message = "Great choice! I've analyzed the car characteristics and updated my recommendations."
        elif context == "track_changed":
            message = "Track data loaded. I'll factor in the track layout and characteristics for optimal setup."
        else:
            message = "Analysis complete! Check the results panel for detailed recommendations."
        
        ai_message = self.create_ai_message(message)
        self.ai_layout.insertWidget(self.ai_layout.count() - 1, ai_message)
        
        # Прокручиваем вниз
        QtCore.QTimer.singleShot(100, lambda: self.ai_messages.verticalScrollBar().setValue(
            self.ai_messages.verticalScrollBar().maximum()
        ))

    def create_ai_message(self, message):
        """Создание AI сообщения"""
        card = QtWidgets.QFrame()
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(59, 130, 246, 0.1),
                    stop:1 rgba(139, 92, 246, 0.1));
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 12px;
            }
        """)
        
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # AI аватар
        avatar = QtWidgets.QLabel("🤖")
        avatar.setStyleSheet("""
            QLabel {
                font-size: 24px;
                background: rgba(59, 130, 246, 0.2);
                border-radius: 20px;
                padding: 8px;
            }
        """)
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(avatar)
        
        # Сообщение
        message_label = QtWidgets.QLabel(message)
        message_label.setStyleSheet("""
            QLabel {
                color: #F8FAFC;
                font-size: 14px;
                line-height: 1.5;
                background: transparent;
            }
        """)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        return card

    def run_optimization(self):
        """Запуск оптимизации настроек"""
        try:
            # Показываем индикатор загрузки
            self.show_loading_state()
            
            # Получаем выбранные параметры
            car_text = self.car_input.input.currentText().strip()
            if car_text.startswith("───") or not car_text:
                QtWidgets.QMessageBox.warning(self, "Error", "Please select a car!")
                return
            
            track_data = self.track_input.input.currentData()
            if not track_data:
                QtWidgets.QMessageBox.warning(self, "Error", "Please select a track!")
                return
            
            # Симулируем анализ с задержкой
            QtCore.QTimer.singleShot(2000, self.complete_analysis)
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Analysis failed: {e}")

    def show_loading_state(self):
        """Показать состояние загрузки"""
        # Очистить результаты
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().setParent(None)
        
        loading_frame = QtWidgets.QFrame()
        loading_frame.setStyleSheet("""
            QFrame {
                background: rgba(59, 130, 246, 0.05);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 16px;
                padding: 48px 24px;
            }
        """)
        
        loading_layout = QtWidgets.QVBoxLayout(loading_frame)
        loading_layout.setSpacing(16)
        
        # Анимированная иконка (симулируем)
        icon_label = QtWidgets.QLabel("🔄")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 48px;
                color: #3B82F6;
            }
        """)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        loading_layout.addWidget(icon_label)
        
        # Текст
        loading_label = QtWidgets.QLabel("Analyzing setup...")
        loading_label.setStyleSheet("""
            QLabel {
                color: #F8FAFC;
                font-size: 18px;
                font-weight: 600;
                text-align: center;
            }
        """)
        loading_label.setAlignment(QtCore.Qt.AlignCenter)
        loading_layout.addWidget(loading_label)
        
        status_label = QtWidgets.QLabel("AI is processing track data and car characteristics")
        status_label.setStyleSheet("""
            QLabel {
                color: #CBD5E1;
                font-size: 14px;
                text-align: center;
            }
        """)
        status_label.setAlignment(QtCore.Qt.AlignCenter)
        loading_layout.addWidget(status_label)
        
        self.results_layout.addWidget(loading_frame)

    def complete_analysis(self):
        """Завершение анализа"""
        # Здесь будет реальная логика анализа
        self.show_analysis_results()
        self.update_ai_suggestions("analysis_complete")

    def show_analysis_results(self):
        """Показать результаты анализа"""
        # Очистить результаты
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().setParent(None)
        
        # Заголовок результатов
        results_header = QtWidgets.QLabel("✅ Analysis Complete")
        results_header.setStyleSheet("""
            QLabel {
                color: #10B981;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 16px;
            }
        """)
        self.results_layout.addWidget(results_header)
        
        # Метрики производительности
        metrics_frame = QtWidgets.QFrame()
        metrics_frame.setStyleSheet("""
            QFrame {
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 12px;
                padding: 16px;
            }
        """)
        
        metrics_layout = QtWidgets.QHBoxLayout(metrics_frame)
        metrics_layout.setSpacing(16)
        
        metrics = [
            ("Expected Improvement", "1.2s", "#10B981"),
            ("Confidence", "94%", "#3B82F6"),
            ("Optimal for", "Hot & Dry", "#F59E0B")
        ]
        
        for title, value, color in metrics:
            metric_card = self.create_metric_card(title, value, color)
            metrics_layout.addWidget(metric_card)
        
        self.results_layout.addWidget(metrics_frame)
        
        # Рекомендации по настройкам
        adjustments = {
            "Front Wing": -2,
            "Rear Wing": -3,
            "Tire Pressure": +1.5,
            "Brake Bias": +2
        }
        
        for param, adjustment in adjustments.items():
            adjustment_card = self.create_adjustment_card(param, adjustment)
            self.results_layout.addWidget(adjustment_card)

    def create_metric_card(self, title, value, color):
        """Создание карточки метрики"""
        card = QtWidgets.QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(30, 41, 59, 0.6);
                border: 1px solid {color}40;
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(4)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 20px;
                font-weight: 700;
                text-align: center;
            }}
        """)
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #94A3B8;
                font-size: 12px;
                text-align: center;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        return card

    def create_adjustment_card(self, parameter, adjustment):
        """Создание карточки настройки"""
        card = QtWidgets.QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(30, 41, 59, 0.6);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 8px;
            }
        """)
        
        layout = QtWidgets.QHBoxLayout(card)
        layout.setSpacing(16)
        
        # Параметр
        param_label = QtWidgets.QLabel(parameter)
        param_label.setStyleSheet("""
            QLabel {
                color: #F8FAFC;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        layout.addWidget(param_label)
        
        layout.addStretch()
        
        # Стрелка направления
        direction = "↗️" if adjustment > 0 else "↘️" if adjustment < 0 else "➡️"
        arrow_label = QtWidgets.QLabel(direction)
        arrow_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(arrow_label)
        
        # Значение
        color = "#10B981" if adjustment > 0 else "#EF4444" if adjustment < 0 else "#6B7280"
        value_label = QtWidgets.QLabel(f"{adjustment:+.1f}")
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 18px;
                font-weight: 700;
                background: rgba(59, 130, 246, 0.1);
                border-radius: 8px;
                padding: 8px 16px;
            }}
        """)
        layout.addWidget(value_label)
        
        return card
