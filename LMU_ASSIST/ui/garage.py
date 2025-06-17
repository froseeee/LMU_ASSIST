from PyQt5 import QtWidgets, QtCore, QtGui
from core.setupexpert import SetupExpert
from core.exceptions import FileError, ValidationError
import json
import re
from pathlib import Path

class GarageTab(QtWidgets.QWidget):
    """Упрощенная вкладка Setup Expert с базовым дизайном"""
    
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
        # Основной layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

        # Заголовок
        self.create_header(main_layout)
        
        # Основной контент
        self.create_content(main_layout)

    def create_header(self, parent_layout):
        """Создание заголовка"""
        header_frame = QtWidgets.QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #0078d4;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 10px;
            }
        """)
        header_frame.setFixedHeight(120)
        
        header_layout = QtWidgets.QHBoxLayout(header_frame)
        
        # Левая часть
        left_section = QtWidgets.QVBoxLayout()
        
        title = QtWidgets.QLabel("🏎️ Setup Expert")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin: 0;
            }
        """)
        
        subtitle = QtWidgets.QLabel("AI-powered car setup optimization")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                margin-top: 5px;
            }
        """)
        
        left_section.addWidget(title)
        left_section.addWidget(subtitle)
        left_section.addStretch()
        
        # Правая часть со статистикой
        stats_layout = QtWidgets.QHBoxLayout()
        
        total_cars = len(self.expert.get_available_cars())
        total_tracks = len(self.expert.get_available_tracks())
        
        cars_stat = self.create_stat_badge(str(total_cars), "Cars")
        tracks_stat = self.create_stat_badge(str(total_tracks), "Tracks")
        
        stats_layout.addWidget(cars_stat)
        stats_layout.addWidget(tracks_stat)
        
        header_layout.addLayout(left_section, 2)
        header_layout.addLayout(stats_layout, 1)
        
        parent_layout.addWidget(header_frame)

    def create_stat_badge(self, value, label):
        """Создание значка статистики"""
        badge = QtWidgets.QFrame()
        badge.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        badge.setFixedSize(80, 60)
        
        layout = QtWidgets.QVBoxLayout(badge)
        layout.setContentsMargins(5, 5, 5, 5)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        
        label_label = QtWidgets.QLabel(label)
        label_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 10px;
            }
        """)
        label_label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(label_label)
        
        return badge

    def create_content(self, parent_layout):
        """Создание основного контента"""
        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Левая панель с настройками
        left_panel = self.create_configuration_panel()
        content_layout.addWidget(left_panel, 1)
        
        # Правая панель с результатами
        right_panel = self.create_results_panel()
        content_layout.addWidget(right_panel, 2)
        
        parent_layout.addLayout(content_layout)

    def create_configuration_panel(self):
        """Создание панели конфигурации"""
        panel = QtWidgets.QGroupBox("⚙️ Configuration")
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin: 5px;
                padding-top: 15px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0078d4;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Селекторы
        self.create_selectors(layout)
        
        # Условия гонки
        self.create_race_conditions(layout)
        
        # Кнопки
        self.create_action_buttons(layout)
        
        return panel

    def create_selectors(self, parent_layout):
        """Создание селекторов"""
        # Автомобиль
        car_layout = QtWidgets.QVBoxLayout()
        car_label = QtWidgets.QLabel("🏎️ Vehicle:")
        car_label.setStyleSheet("font-weight: bold; color: #333;")
        
        self.car_combo = QtWidgets.QComboBox()
        self.car_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox:focus {
                border-color: #0078d4;
            }
        """)
        
        # Добавляем автомобили
        available_cars = self.expert.get_available_cars()
        for car in available_cars:
            self.car_combo.addItem(car)
        
        car_layout.addWidget(car_label)
        car_layout.addWidget(self.car_combo)
        parent_layout.addLayout(car_layout)
        
        # Трасса
        track_layout = QtWidgets.QVBoxLayout()
        track_label = QtWidgets.QLabel("🏁 Track:")
        track_label.setStyleSheet("font-weight: bold; color: #333;")
        
        self.track_combo = QtWidgets.QComboBox()
        self.track_combo.setStyleSheet(self.car_combo.styleSheet())
        
        # Добавляем трассы
        available_tracks = self.expert.get_available_tracks()
        for track in available_tracks:
            try:
                track_info = self.expert.get_track_recommendations(track)
                display_name = track_info.get('name', track)
                self.track_combo.addItem(display_name, track)
            except Exception:
                self.track_combo.addItem(track, track)
        
        track_layout.addWidget(track_label)
        track_layout.addWidget(self.track_combo)
        parent_layout.addLayout(track_layout)

    def create_race_conditions(self, parent_layout):
        """Создание секции условий гонки"""
        conditions_label = QtWidgets.QLabel("🌤️ Race Conditions")
        conditions_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin: 10px 0;
            }
        """)
        parent_layout.addWidget(conditions_label)
        
        # Температура
        temp_layout = QtWidgets.QVBoxLayout()
        temp_label = QtWidgets.QLabel("Temperature:")
        temp_label.setStyleSheet("font-weight: bold; color: #666;")
        
        self.temp_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.temp_slider.setRange(-10, 60)
        self.temp_slider.setValue(25)
        self.temp_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #0078d4;
            }
        """)
        
        self.temp_value = QtWidgets.QLabel("25°C")
        self.temp_value.setStyleSheet("color: #0078d4; font-weight: bold;")
        self.temp_slider.valueChanged.connect(
            lambda v: self.temp_value.setText(f"{v}°C")
        )
        
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_value)
        parent_layout.addLayout(temp_layout)
        
        # Погода
        weather_layout = QtWidgets.QVBoxLayout()
        weather_label = QtWidgets.QLabel("Weather:")
        weather_label.setStyleSheet("font-weight: bold; color: #666;")
        
        self.weather_combo = QtWidgets.QComboBox()
        self.weather_combo.setStyleSheet(self.car_combo.styleSheet())
        self.weather_combo.addItems(["☀️ Dry", "🌦️ Light Rain", "🌧️ Heavy Rain"])
        
        weather_layout.addWidget(weather_label)
        weather_layout.addWidget(self.weather_combo)
        parent_layout.addLayout(weather_layout)

    def create_action_buttons(self, parent_layout):
        """Создание кнопок действий"""
        parent_layout.addSpacing(20)
        
        # Основная кнопка анализа
        self.analyze_btn = QtWidgets.QPushButton("🔬 Analyze Setup")
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        self.analyze_btn.clicked.connect(self.run_optimization)
        parent_layout.addWidget(self.analyze_btn)
        
        # Вторичные кнопки
        secondary_layout = QtWidgets.QHBoxLayout()
        
        self.save_btn = QtWidgets.QPushButton("💾 Save")
        self.export_btn = QtWidgets.QPushButton("📤 Export")
        
        secondary_style = """
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """
        
        self.save_btn.setStyleSheet(secondary_style)
        self.export_btn.setStyleSheet(secondary_style)
        
        secondary_layout.addWidget(self.save_btn)
        secondary_layout.addWidget(self.export_btn)
        
        parent_layout.addLayout(secondary_layout)

    def create_results_panel(self):
        """Создание панели результатов"""
        panel = QtWidgets.QGroupBox("📊 Analysis Results")
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin: 5px;
                padding-top: 15px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0078d4;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(panel)
        
        # Область результатов
        self.results_text = QtWidgets.QTextBrowser()
        self.results_text.setStyleSheet("""
            QTextBrowser {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 15px;
                background-color: white;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        
        # Начальное состояние
        self.show_welcome_state()
        
        layout.addWidget(self.results_text)
        
        return panel

    def show_welcome_state(self):
        """Показать начальное состояние"""
        welcome_html = """
        <div style="text-align: center; padding: 40px;">
            <h2 style="color: #0078d4; margin-bottom: 20px;">🚀 Ready to Optimize</h2>
            <p style="font-size: 16px; color: #666; margin-bottom: 30px;">
                Select your car and track, adjust race conditions, 
                then click "Analyze Setup" to get AI-powered recommendations.
            </p>
            
            <div style="display: flex; justify-content: space-around; margin-top: 30px;">
                <div style="text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 10px;">🧠</div>
                    <div style="font-weight: bold; color: #333;">AI Analysis</div>
                    <div style="color: #666; font-size: 12px;">Machine learning powered</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 10px;">⚡</div>
                    <div style="font-weight: bold; color: #333;">Real-time</div>
                    <div style="color: #666; font-size: 12px;">Instant optimization</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 10px;">🎯</div>
                    <div style="font-weight: bold; color: #333;">Precision</div>
                    <div style="color: #666; font-size: 12px;">Track-specific</div>
                </div>
            </div>
        </div>
        """
        
        self.results_text.setHtml(welcome_html)

    def run_optimization(self):
        """Запуск оптимизации настроек"""
        try:
            # Показываем индикатор загрузки
            self.show_loading_state()
            
            # Получаем выбранные параметры
            car_text = self.car_combo.currentText()
            track_data = self.track_combo.currentData()
            
            if not car_text or not track_data:
                QtWidgets.QMessageBox.warning(self, "Error", "Please select car and track!")
                self.show_welcome_state()
                return
            
            # Симулируем анализ с задержкой
            QtCore.QTimer.singleShot(2000, self.complete_analysis)
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Analysis failed: {e}")
            self.show_welcome_state()

    def show_loading_state(self):
        """Показать состояние загрузки"""
        loading_html = """
        <div style="text-align: center; padding: 60px;">
            <h2 style="color: #0078d4; margin-bottom: 20px;">🔄 Analyzing Setup...</h2>
            <p style="font-size: 16px; color: #666;">
                AI is processing track data and car characteristics
            </p>
            <div style="margin-top: 30px; color: #0078d4;">
                <div style="font-size: 24px;">⚙️ Processing...</div>
            </div>
        </div>
        """
        
        self.results_text.setHtml(loading_html)

    def complete_analysis(self):
        """Завершение анализа"""
        # Получаем данные
        car = self.car_combo.currentText()
        track = self.track_combo.currentData() or "test_track"
        temperature = self.temp_slider.value()
        weather = self.weather_combo.currentText()
        
        # Формируем условия
        conditions = {
            "temperature": temperature,
            "weather": weather.split(" ")[-1].lower() if weather else "dry",
            "track": track
        }
        
        # Простые данные телеметрии для демо
        telemetry = {
            "brake_avg": 0.7,
            "throttle_exit": 0.8,
            "balance": "neutral"
        }
        
        try:
            # Получаем рекомендации
            recommendations = self.expert.recommend_setup(
                conditions, telemetry, car, track
            )
            
            self.show_analysis_results(recommendations)
            
        except Exception as e:
            error_html = f"""
            <div style="text-align: center; padding: 40px;">
                <h2 style="color: #dc3545;">❌ Analysis Error</h2>
                <p style="color: #666;">An error occurred during analysis:</p>
                <p style="color: #dc3545; font-family: monospace;">{str(e)}</p>
                <p style="color: #666; margin-top: 20px;">
                    Please check your car and track selection.
                </p>
            </div>
            """
            self.results_text.setHtml(error_html)

    def show_analysis_results(self, recommendations):
        """Показать результаты анализа"""
        adjustments = recommendations.get("adjustments", {})
        explanations = recommendations.get("explanations", ["No specific recommendations"])
        confidence = recommendations.get("confidence", 0.5)
        
        # Формируем HTML результатов
        results_html = f"""
        <div style="padding: 20px;">
            <h2 style="color: #28a745; margin-bottom: 20px;">✅ Analysis Complete</h2>
            
            <div style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 4px; padding: 15px; margin-bottom: 20px;">
                <strong>Confidence: {confidence*100:.0f}%</strong>
            </div>
            
            <h3 style="color: #0078d4;">🔧 Recommended Adjustments:</h3>
        """
        
        if adjustments:
            results_html += "<ul style='margin-left: 20px;'>"
            for param, value in adjustments.items():
                direction = "↗️" if value > 0 else "↘️" if value < 0 else "➡️"
                color = "#28a745" if value > 0 else "#dc3545" if value < 0 else "#6c757d"
                results_html += f"""
                <li style="margin-bottom: 8px;">
                    <strong>{param.replace('_', ' ').title()}:</strong> 
                    <span style="color: {color}; font-weight: bold;">{direction} {value:+.1f}</span>
                </li>
                """
            results_html += "</ul>"
        else:
            results_html += "<p style='color: #666; font-style: italic;'>No adjustments needed - current setup is optimal!</p>"
        
        results_html += "<h3 style='color: #0078d4; margin-top: 25px;'>💡 Explanations:</h3>"
        results_html += "<ul style='margin-left: 20px;'>"
        
        for explanation in explanations:
            results_html += f"<li style='margin-bottom: 5px; color: #333;'>{explanation}</li>"
        
        results_html += "</ul></div>"
        
        self.results_text.setHtml(results_html)
