from PyQt5 import QtWidgets, QtCore, QtGui
from core.setupexpert import SetupExpert
import json
import re
from pathlib import Path

class GarageTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self.expert = SetupExpert(str(Path("data/lmu_data.json")))
        self.init_ui()

    def init_ui(self):
        # Основной layout с отступами
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

        # Заголовок с современным стилем
        self.create_header(main_layout)
        
        # Главная область с карточками
        self.create_main_content(main_layout)

    def create_header(self, parent_layout):
        """Создание современного заголовка"""
        header_widget = QtWidgets.QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 16px;
                padding: 20px;
            }
        """)
        header_widget.setFixedHeight(120)
        
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        
        # Левая часть с иконкой и текстом
        left_section = QtWidgets.QVBoxLayout()
        
        title = QtWidgets.QLabel("🏎️ Setup Expert")
        title.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin: 0;
        """)
        
        subtitle = QtWidgets.QLabel("Optimize your car setup for peak performance")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
            margin-top: 5px;
        """)
        
        left_section.addWidget(title)
        left_section.addWidget(subtitle)
        left_section.addStretch()
        
        # Правая часть со статистикой
        stats_section = QtWidgets.QHBoxLayout()
        
        total_cars = len(self.expert.get_available_cars())
        total_tracks = len(self.expert.get_available_tracks())
        
        cars_stat = self.create_stat_badge(str(total_cars), "Cars")
        tracks_stat = self.create_stat_badge(str(total_tracks), "Tracks")
        
        stats_section.addWidget(cars_stat)
        stats_section.addWidget(tracks_stat)
        
        header_layout.addLayout(left_section, 3)
        header_layout.addLayout(stats_section, 1)
        
        parent_layout.addWidget(header_widget)

    def create_stat_badge(self, value, label):
        """Создание значка статистики"""
        badge = QtWidgets.QWidget()
        badge.setStyleSheet("""
            background: rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 15px;
        """)
        badge.setFixedSize(80, 60)
        
        layout = QtWidgets.QVBoxLayout(badge)
        layout.setContentsMargins(5, 5, 5, 5)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        
        label_label = QtWidgets.QLabel(label)
        label_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 11px;
        """)
        label_label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(label_label)
        
        return badge

    def create_main_content(self, parent_layout):
        """Создание основного контента"""
        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Левая панель с настройками
        left_panel = self.create_settings_panel()
        content_layout.addWidget(left_panel, 1)
        
        # Центральная панель с результатами
        center_panel = self.create_results_panel()
        content_layout.addWidget(center_panel, 2)
        
        # Правая панель с рекомендациями
        right_panel = self.create_recommendations_panel()
        content_layout.addWidget(right_panel, 1)
        
        parent_layout.addLayout(content_layout)

    def create_settings_panel(self):
        """Создание панели настроек"""
        panel = QtWidgets.QWidget()
        panel.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 16px;
                border: 1px solid #e0e4e7;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Заголовок панели
        panel_title = QtWidgets.QLabel("⚙️ Configuration")
        panel_title.setStyleSheet("""
            color: #1a202c;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        layout.addWidget(panel_title)
        
        # Селекторы
        self.create_modern_selectors(layout)
        
        # Условия гонки
        self.create_race_conditions(layout)
        
        # Кнопка анализа
        self.create_analyze_button(layout)
        
        layout.addStretch()
        return panel

    def create_modern_selectors(self, parent_layout):
        """Создание современных селекторов"""
        # Автомобиль
        car_section = QtWidgets.QVBoxLayout()
        
        car_label = QtWidgets.QLabel("Vehicle")
        car_label.setStyleSheet("""
            color: #4a5568;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        """)
        
        self.car_selector = QtWidgets.QComboBox()
        self.car_selector.setStyleSheet("""
            QComboBox {
                background: #f7fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #2d3748;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #667eea;
                background: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #a0aec0;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 4px;
                selection-background-color: #667eea;
                selection-color: white;
            }
        """)
        
        # Группируем машины по категориям
        car_groups = self.group_cars_by_category()
        for category, cars in car_groups.items():
            if cars:
                self.car_selector.addItem(f"--- {category} ---")
                for car in cars:
                    self.car_selector.addItem(f"  {car}")
        
        self.car_selector.currentTextChanged.connect(self.on_car_changed)
        
        car_section.addWidget(car_label)
        car_section.addWidget(self.car_selector)
        
        # Трасса
        track_section = QtWidgets.QVBoxLayout()
        
        track_label = QtWidgets.QLabel("Track")
        track_label.setStyleSheet(car_label.styleSheet())
        
        self.track_selector = QtWidgets.QComboBox()
        self.track_selector.setStyleSheet(self.car_selector.styleSheet())
        
        available_tracks = self.expert.get_available_tracks()
        for track in available_tracks:
            track_info = self.expert.get_track_recommendations(track)
            display_name = track_info.get('name', track)
            self.track_selector.addItem(display_name, track)
        
        self.track_selector.currentTextChanged.connect(self.on_track_changed)
        
        track_section.addWidget(track_label)
        track_section.addWidget(self.track_selector)
        
        parent_layout.addLayout(car_section)
        parent_layout.addLayout(track_section)

    def group_cars_by_category(self):
        """Группировка автомобилей по категориям"""
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
            
            # Добавляем дополнительную информацию
            display_name = car_name
            
            if "free_car" in car_data and car_data["free_car"]:
                display_name += " 🆓"
            if "status" in car_data and car_data["status"] == "coming_soon":
                display_name += " ⏳"
            
            # Добавляем мощность для различия
            power = car_data.get("power", "")
            if power:
                display_name += f" ({power}hp)"
                
            if category in groups:
                groups[category].append(display_name)
        
        # Сортируем по производителям
        for category in groups:
            groups[category].sort(key=lambda x: x.split()[0])  # Сортируем по первому слову (производитель)
        
        return groups

    def create_race_conditions(self, parent_layout):
        """Создание секции условий гонки"""
        conditions_title = QtWidgets.QLabel("Race Conditions")
        conditions_title.setStyleSheet("""
            color: #1a202c;
            font-size: 16px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 15px;
        """)
        parent_layout.addWidget(conditions_title)
        
        # Сетка для условий
        conditions_grid = QtWidgets.QGridLayout()
        conditions_grid.setSpacing(15)
        
        # Температура
        temp_label = QtWidgets.QLabel("Temperature")
        temp_label.setStyleSheet("color: #4a5568; font-size: 12px; font-weight: 600;")
        
        self.temp_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.temp_slider.setRange(-10, 60)
        self.temp_slider.setValue(25)
        self.temp_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #e2e8f0;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #667eea;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -7px 0;
            }
            QSlider::sub-page:horizontal {
                background: #667eea;
                border-radius: 3px;
            }
        """)
        
        self.temp_value = QtWidgets.QLabel("25°C")
        self.temp_value.setStyleSheet("color: #667eea; font-weight: bold; font-size: 12px;")
        self.temp_value.setAlignment(QtCore.Qt.AlignCenter)
        
        self.temp_slider.valueChanged.connect(
            lambda v: self.temp_value.setText(f"{v}°C")
        )
        
        # Погода
        weather_label = QtWidgets.QLabel("Weather")
        weather_label.setStyleSheet(temp_label.styleSheet())
        
        self.weather_selector = QtWidgets.QComboBox()
        self.weather_selector.setStyleSheet("""
            QComboBox {
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                color: #2d3748;
                min-height: 15px;
            }
        """)
        self.weather_selector.addItems(["☀️ Dry", "🌦️ Light Rain", "🌧️ Heavy Rain"])
        
        # Стратегия
        strategy_label = QtWidgets.QLabel("Strategy")
        strategy_label.setStyleSheet(temp_label.styleSheet())
        
        self.strategy_selector = QtWidgets.QComboBox()
        self.strategy_selector.setStyleSheet(self.weather_selector.styleSheet())
        self.strategy_selector.addItems(["🏃 Sprint", "⏱️ 6 Hour", "🕐 24 Hour"])
        
        # Размещение в сетке
        conditions_grid.addWidget(temp_label, 0, 0)
        conditions_grid.addWidget(self.temp_slider, 0, 1)
        conditions_grid.addWidget(self.temp_value, 0, 2)
        
        conditions_grid.addWidget(weather_label, 1, 0)
        conditions_grid.addWidget(self.weather_selector, 1, 1, 1, 2)
        
        conditions_grid.addWidget(strategy_label, 2, 0)
        conditions_grid.addWidget(self.strategy_selector, 2, 1, 1, 2)
        
        parent_layout.addLayout(conditions_grid)

    def create_analyze_button(self, parent_layout):
        """Создание кнопки анализа"""
        button_container = QtWidgets.QVBoxLayout()
        button_container.setSpacing(10)
        
        self.analyze_btn = QtWidgets.QPushButton("🔬 Analyze Setup")
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 16px 24px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46c1);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4c51bf, stop:1 #553c9a);
            }
        """)
        self.analyze_btn.clicked.connect(self.run_optimization)
        
        # Вторичные кнопки
        secondary_layout = QtWidgets.QHBoxLayout()
        
        self.save_btn = QtWidgets.QPushButton("💾")
        self.share_btn = QtWidgets.QPushButton("📤")
        
        for btn in [self.save_btn, self.share_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: #f7fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 16px;
                    color: #4a5568;
                }
                QPushButton:hover {
                    background: #edf2f7;
                    border-color: #cbd5e0;
                }
            """)
            btn.setFixedSize(50, 50)
        
        secondary_layout.addWidget(self.save_btn)
        secondary_layout.addWidget(self.share_btn)
        secondary_layout.addStretch()
        
        button_container.addWidget(self.analyze_btn)
        button_container.addLayout(secondary_layout)
        
        parent_layout.addLayout(button_container)

    def create_results_panel(self):
        """Создание панели результатов"""
        panel = QtWidgets.QWidget()
        panel.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 16px;
                border: 1px solid #e0e4e7;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Заголовок
        title = QtWidgets.QLabel("📊 Setup Analysis")
        title.setStyleSheet("""
            color: #1a202c;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Область результатов
        self.results_area = QtWidgets.QTextBrowser()
        self.results_area.setStyleSheet("""
            QTextBrowser {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
            }
        """)
        
        # Начальное содержимое
        self.results_area.setHtml("""
            <div style="text-align: center; padding: 40px 20px; color: #718096;">
                <h2 style="color: #2d3748; margin-bottom: 16px;">🏁 Ready to Optimize</h2>
                <p style="font-size: 16px; margin-bottom: 24px;">
                    Select your car and track, adjust the conditions, then click <strong>Analyze Setup</strong> 
                    to get personalized recommendations.
                </p>
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 16px; border-radius: 8px; margin: 20px 0;">
                    <strong>💡 Pro Tip:</strong> Start with base settings and gradually fine-tune based on recommendations.
                </div>
            </div>
        """)
        
        layout.addWidget(self.results_area)
        return panel

    def create_recommendations_panel(self):
        """Создание панели рекомендаций"""
        panel = QtWidgets.QWidget()
        panel.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 16px;
                border: 1px solid #e0e4e7;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Заголовок
        title = QtWidgets.QLabel("💡 Quick Tips")
        title.setStyleSheet("""
            color: #1a202c;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Быстрые советы
        tips = [
            ("🏎️", "Aero Balance", "Higher downforce = more grip but less top speed"),
            ("🛞", "Tire Pressure", "Lower pressure = more grip but faster wear"),
            ("🔧", "Suspension", "Stiffer = better handling on smooth tracks"),
            ("⚖️", "Brake Balance", "Forward bias helps with turn-in"),
            ("⚡", "Differential", "Locked diff = better traction out of corners")
        ]
        
        for icon, title_text, description in tips:
            tip_widget = self.create_tip_card(icon, title_text, description)
            layout.addWidget(tip_widget)
        
        layout.addStretch()
        return panel

    def create_tip_card(self, icon, title, description):
        """Создание карточки совета"""
        card = QtWidgets.QWidget()
        card.setStyleSheet("""
            QWidget {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 8px;
            }
            QWidget:hover {
                background: #edf2f7;
                border-color: #cbd5e0;
            }
        """)
        
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Иконка
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setStyleSheet("""
            font-size: 20px;
            color: #667eea;
            margin-right: 8px;
        """)
        icon_label.setFixedSize(30, 30)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Текст
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(2)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            color: #2d3748;
            font-size: 13px;
            font-weight: bold;
        """)
        
        desc_label = QtWidgets.QLabel(description)
        desc_label.setStyleSheet("""
            color: #718096;
            font-size: 11px;
        """)
        desc_label.setWordWrap(True)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        
        return card

    def on_car_changed(self):
        """Обработка смены автомобиля"""
        self.load_car_info()

    def on_track_changed(self):
        """Обработка смены трассы"""
        self.load_track_info()

    def load_car_info(self):
        """Загрузка информации об автомобиле"""
        car_text = self.car_selector.currentText().strip()
        if car_text.startswith("---") or not car_text:
            return
            
        # Убираем префикс и суффиксы (включая мощность в скобках)
        car_name = car_text.replace("  ", "")
        car_name = re.sub(r'\s*🆓|\s*⏳|\s*\(\d+hp\)', '', car_name)  # Убираем эмодзи и мощность
        
        # Находим машину в данных
        cars_data = self.expert.data.get("cars", {})
        selected_car = None
        
        for car_id, car_data in cars_data.items():
            if car_data.get("name", "") == car_name:
                selected_car = car_data
                break
        
        if selected_car:
            self.display_car_info(selected_car)

    def display_car_info(self, car_data):
        """Отображение информации об автомобиле"""
        html = f"""
        <div style="padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 20px; border-radius: 12px; margin-bottom: 24px;">
                <h2 style="margin: 0 0 8px 0; font-size: 24px;">{car_data.get('name', 'Unknown')}</h2>
                <p style="margin: 0; opacity: 0.9; font-size: 14px;">
                    {car_data.get('manufacturer', 'Unknown')} • {car_data.get('category', 'Unknown')}
                </p>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                <div style="background: #f8fafc; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <h4 style="margin: 0 0 8px 0; color: #2d3748;">⚡ Power</h4>
                    <p style="margin: 0; font-size: 20px; font-weight: bold; color: #667eea;">
                        {car_data.get('power', 'N/A')} HP
                    </p>
                </div>
                <div style="background: #f8fafc; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <h4 style="margin: 0 0 8px 0; color: #2d3748;">⚖️ Weight</h4>
                    <p style="margin: 0; font-size: 20px; font-weight: bold; color: #667eea;">
                        {car_data.get('weight', 'N/A')} kg
                    </p>
                </div>
            </div>
            
            <div style="background: #f8fafc; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 16px;">
                <h4 style="margin: 0 0 12px 0; color: #2d3748;">🔧 Technical Specs</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div>
                        <p style="margin: 0; color: #4a5568;"><strong>Drivetrain:</strong> {car_data.get('drivetrain', 'N/A')}</p>
                    </div>
        """
        
        # Добавляем информацию о двигателе если есть
        if car_data.get('engine'):
            html += f"""
                    <div>
                        <p style="margin: 0; color: #4a5568;"><strong>Engine:</strong> {car_data.get('engine')}</p>
                    </div>
            """
        
        # Добавляем информацию о трансмиссии если есть
        if car_data.get('transmission'):
            html += f"""
                    <div>
                        <p style="margin: 0; color: #4a5568;"><strong>Transmission:</strong> {car_data.get('transmission')}</p>
                    </div>
            """
        
        html += """
                </div>
        """
        
        # Специальные отметки
        if car_data.get('hybrid_system'):
            html += """
                <div style="margin-top: 12px; padding: 12px; background: #e6fffa; border: 1px solid #81e6d9; border-radius: 6px;">
                    <strong style="color: #234e52;">⚡ Hybrid System Available</strong>
                </div>
            """
        
        if car_data.get('free_car'):
            html += """
                <div style="margin-top: 12px; padding: 12px; background: #f0fff4; border: 1px solid #9ae6b4; border-radius: 6px;">
                    <strong style="color: #22543d;">🆓 Free Car</strong>
                </div>
            """
        
        if car_data.get('status') == 'coming_soon':
            html += """
                <div style="margin-top: 12px; padding: 12px; background: #fffbf0; border: 1px solid #fbd38d; border-radius: 6px;">
                    <strong style="color: #744210;">⏳ Coming Soon</strong>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        self.results_area.setHtml(html)

    def load_track_info(self):
        """Загрузка информации о трассе"""
        # Можно добавить аналогичную функцию для трасс
        pass

    def run_optimization(self):
        """Запуск оптимизации настроек"""
        try:
            # Получаем выбранные параметры
            car_text = self.car_selector.currentText().strip()
            if car_text.startswith("---") or not car_text:
                QtWidgets.QMessageBox.warning(self, "Error", "Please select a car!")
                return
            
            track_data = self.track_selector.currentData()
            if not track_data:
                QtWidgets.QMessageBox.warning(self, "Error", "Please select a track!")
                return
            
            # Собираем условия
            conditions = {
                "temperature": self.temp_slider.value(),
                "weather": self.weather_selector.currentText().split()[-1].lower(),  # Извлекаем тип погоды
                "race_duration": self.strategy_selector.currentText().split()[-1].lower().replace("hour", "_hour"),
                "track": track_data
            }
            
            # Создаем базовую телеметрию
            telemetry = {
                "brake_avg": 0.85,
                "throttle_exit": 0.8,
                "steering_smoothness": 0.75,
                "balance": "neutral"
            }
            
            # Получаем ID машины
            car_name = car_text.replace("  ", "")
            car_name = re.sub(r'\s*🆓|\s*⏳|\s*\(\d+hp\)', '', car_name)  # Убираем эмодзи и мощность
            car_id = None
            
            for cid, cdata in self.expert.data.get("cars", {}).items():
                if cdata.get("name", "") == car_name:
                    car_id = cid
                    break
            
            if not car_id:
                QtWidgets.QMessageBox.warning(self, "Error", "Car not found in database!")
                return
            
            # Получаем рекомендации
            recommendations = self.expert.recommend_setup(conditions, telemetry, car_id, track_data)
            
            # Отображаем результаты
            self.display_modern_results(recommendations, car_name, conditions)
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Analysis failed: {e}")

    def display_modern_results(self, recommendations, car_name, conditions):
        """Отображение результатов в современном стиле"""
        adjustments = recommendations.get("adjustments", {})
        explanations = recommendations.get("explanations", [])
        confidence = recommendations.get("confidence", 0)
        
        # Цвет уверенности
        confidence_color = "#22c55e" if confidence > 0.8 else "#f59e0b" if confidence > 0.6 else "#ef4444"
        
        html = f"""
        <div style="padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 24px; border-radius: 12px; margin-bottom: 24px;">
                <h2 style="margin: 0 0 12px 0; font-size: 24px;">🏁 Setup Analysis Complete</h2>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="margin: 0; opacity: 0.9;">Car: <strong>{car_name}</strong></p>
                        <p style="margin: 4px 0 0 0; opacity: 0.9;">Track: <strong>{recommendations.get('track_name', 'N/A')}</strong></p>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px;">
                            <div style="font-size: 24px; font-weight: bold; color: {confidence_color};">
                                {confidence:.0%}
                            </div>
                            <div style="font-size: 12px; opacity: 0.8;">Confidence</div>
                        </div>
                    </div>
                </div>
            </div>
        """
        
        if adjustments:
            html += """
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <h3 style="margin: 0 0 16px 0; color: #1a202c; font-size: 18px;">🔧 Recommended Adjustments</h3>
                <div style="display: grid; gap: 12px;">
            """
            
            for param, value in adjustments.items():
                direction = "↗️" if value > 0 else "↘️" if value < 0 else "➡️"
                color = "#22c55e" if value > 0 else "#ef4444" if value < 0 else "#6b7280"
                
                param_display = param.replace("_", " ").title()
                
                html += f"""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px;
                            display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #2d3748;">{param_display}</strong>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 18px;">{direction}</span>
                        <span style="color: {color}; font-weight: bold; font-size: 16px;">
                            {abs(value):+.1f}
                        </span>
                    </div>
                </div>
                """
            
            html += "</div></div>"
        
        # Объяснения
        if explanations:
            html += """
            <div style="background: #fef7e0; border: 1px solid #f6cc5d; border-radius: 12px; padding: 20px;">
                <h3 style="margin: 0 0 16px 0; color: #92400e; font-size: 18px;">💡 Explanations</h3>
                <ul style="margin: 0; padding-left: 20px; color: #92400e;">
            """
            
            for explanation in explanations:
                html += f"<li style='margin-bottom: 8px;'>{explanation}</li>"
            
            html += "</ul></div>"
        
        html += "</div>"
        
        self.results_area.setHtml(html)
