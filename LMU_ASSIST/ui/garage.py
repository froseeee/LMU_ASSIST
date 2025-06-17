from PyQt5 import QtWidgets, QtCore
from core.setupexpert import SetupExpert
import json
from pathlib import Path

class GarageTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Инициализация эксперта с данными LMU
        data_file = Path("data/lmu_data.json")
        
        # ВАЖНО: Проверяем, что файл существует и загружается
        if data_file.exists():
            try:
                # Проверим размер файла
                file_size = data_file.stat().st_size
                print(f"Размер файла lmu_data.json: {file_size} байт")
                
                # Попробуем загрузить данные напрямую для проверки
                import json
                with open(data_file, 'r', encoding='utf-8') as f:
                    test_data = json.load(f)
                
                print(f"Найдено автомобилей: {len(test_data.get('cars', {}))}")
                print(f"Найдено трасс: {len(test_data.get('tracks', {}))}")
                print(f"Список автомобилей: {list(test_data.get('cars', {}).keys())}")
                print(f"Список трасс: {list(test_data.get('tracks', {}).keys())}")
                
            except Exception as e:
                print(f"Ошибка проверки файла данных: {e}")
        else:
            print("❌ Файл data/lmu_data.json не найден!")
            print("Создайте файл с полными данными")

        self.expert = SetupExpert(str(data_file) if data_file.exists() else None)
        
        # Проверим, что expert загрузил данные
        available_cars = self.expert.get_available_cars()
        available_tracks = self.expert.get_available_tracks()
        
        print(f"Expert загрузил автомобилей: {len(available_cars)}")
        print(f"Expert загрузил трасс: {len(available_tracks)}")

        self.init_ui()

    def init_ui(self):
        # Заголовок
        title = QtWidgets.QLabel("🛠️ Настройки автомобиля")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        self.layout.addWidget(title)

        # Горизонтальный layout для селекторов
        selectors_layout = QtWidgets.QHBoxLayout()
        
        # Выбор автомобиля
        car_group = QtWidgets.QGroupBox("Автомобиль")
        car_layout = QtWidgets.QVBoxLayout()
        self.car_selector = QtWidgets.QComboBox()
        
        # Получаем список доступных машин
        available_cars = self.expert.get_available_cars()
        print(f"Добавляем в комбобокс автомобилей: {available_cars}")
        self.car_selector.addItems(available_cars)
        self.car_selector.currentTextChanged.connect(self.on_car_changed)
        
        car_layout.addWidget(self.car_selector)
        car_group.setLayout(car_layout)
        
        # Выбор трассы
        track_group = QtWidgets.QGroupBox("Трасса")
        track_layout = QtWidgets.QVBoxLayout()
        self.track_selector = QtWidgets.QComboBox()
        
        # Получаем список доступных трасс
        available_tracks = self.expert.get_available_tracks()
        print(f"Добавляем в комбобокс трасс: {available_tracks}")
        self.track_selector.addItems(available_tracks)
        self.track_selector.currentTextChanged.connect(self.on_track_changed)
        
        track_layout.addWidget(self.track_selector)
        track_group.setLayout(track_layout)
        
        selectors_layout.addWidget(car_group)
        selectors_layout.addWidget(track_group)
        self.layout.addLayout(selectors_layout)

        # Условия гонки
        conditions_group = QtWidgets.QGroupBox("Условия гонки")
        conditions_layout = QtWidgets.QGridLayout()
        
        # Температура
        conditions_layout.addWidget(QtWidgets.QLabel("Температура (°C):"), 0, 0)
        self.temp_spinbox = QtWidgets.QSpinBox()
        self.temp_spinbox.setRange(-10, 60)
        self.temp_spinbox.setValue(25)
        conditions_layout.addWidget(self.temp_spinbox, 0, 1)
        
        # Продолжительность гонки
        conditions_layout.addWidget(QtWidgets.QLabel("Тип гонки:"), 1, 0)
        self.race_type = QtWidgets.QComboBox()
        self.race_type.addItems(["6_hour", "24_hour", "sprint"])
        conditions_layout.addWidget(self.race_type, 1, 1)
        
        # Погода
        conditions_layout.addWidget(QtWidgets.QLabel("Погода:"), 0, 2)
        self.weather_selector = QtWidgets.QComboBox()
        self.weather_selector.addItems(["dry", "light_rain", "heavy_rain"])
        conditions_layout.addWidget(self.weather_selector, 0, 3)
        
        # Стратегия стинтов
        conditions_layout.addWidget(QtWidgets.QLabel("Стинты:"), 1, 2)
        self.stint_strategy = QtWidgets.QComboBox()
        self.stint_strategy.addItems(["short", "medium", "long"])
        conditions_layout.addWidget(self.stint_strategy, 1, 3)
        
        conditions_group.setLayout(conditions_layout)
        self.layout.addWidget(conditions_group)

        # Телеметрия (симуляция)
        telemetry_group = QtWidgets.QGroupBox("Анализ стиля пилотирования")
        telemetry_layout = QtWidgets.QGridLayout()
        
        # Стиль торможения
        telemetry_layout.addWidget(QtWidgets.QLabel("Стиль торможения:"), 0, 0)
        self.brake_style = QtWidgets.QComboBox()
        self.brake_style.addItems(["normal", "aggressive", "late"])
        telemetry_layout.addWidget(self.brake_style, 0, 1)
        
        # Баланс автомобиля
        telemetry_layout.addWidget(QtWidgets.QLabel("Баланс:"), 0, 2)
        self.balance_selector = QtWidgets.QComboBox()
        self.balance_selector.addItems(["neutral", "understeer", "oversteer"])
        telemetry_layout.addWidget(self.balance_selector, 0, 3)
        
        telemetry_group.setLayout(telemetry_layout)
        self.layout.addWidget(telemetry_group)

        # Результаты
        self.result_area = QtWidgets.QTextBrowser()
        self.result_area.setMinimumHeight(250)
        self.layout.addWidget(self.result_area)

        # Кнопки
        buttons_layout = QtWidgets.QHBoxLayout()
        
        self.optimize_button = QtWidgets.QPushButton("🔧 Получить рекомендации")
        self.optimize_button.setMinimumHeight(40)
        self.optimize_button.clicked.connect(self.run_optimization)
        buttons_layout.addWidget(self.optimize_button)
        
        self.clear_button = QtWidgets.QPushButton("🗑️ Очистить")
        self.clear_button.setMinimumHeight(40)
        self.clear_button.clicked.connect(self.clear_results)
        buttons_layout.addWidget(self.clear_button)
        
        self.layout.addLayout(buttons_layout)

        # Загружаем информацию о текущем автомобиле
        self.load_car_info()

    def on_car_changed(self):
        """Обработка смены автомобиля"""
        self.load_car_info()

    def on_track_changed(self):
        """Обработка смены трассы"""
        self.load_track_info()

    def load_car_info(self):
        """Загрузка информации об автомобиле"""
        car_type = self.car_selector.currentText()
        if not car_type:
            return
            
        try:
            car_specs = self.expert.get_car_specifications(car_type)
            if 'error' not in car_specs:
                info_html = f"""
                <h4>Информация об автомобиле:</h4>
                <p><b>Название:</b> {car_specs.get('name', 'N/A')}</p>
                <p><b>Категория:</b> {car_specs.get('category', 'N/A')}</p>
                <p><b>Мощность:</b> {car_specs.get('power', 'N/A')} л.с.</p>
                <p><b>Вес:</b> {car_specs.get('weight', 'N/A')} кг</p>
                <p><b>Привод:</b> {car_specs.get('drivetrain', 'N/A')}</p>
                """
                
                if car_specs.get('hybrid_system'):
                    info_html += "<p><b>Гибридная система:</b> Да</p>"
                
                if car_specs.get('free_car'):
                    info_html += "<p><b>🆓 Бесплатная машина</b></p>"
                
                self.result_area.setHtml(info_html)
            else:
                self.result_area.setHtml(f"<p style='color: red;'>{car_specs['error']}</p>")
        except Exception as e:
            self.result_area.setHtml(f"<p style='color: red;'>Ошибка загрузки информации: {e}</p>")

    def load_track_info(self):
        """Загрузка информации о трассе"""
        track_name = self.track_selector.currentText()
        if not track_name:
            return
            
        try:
            track_info = self.expert.get_track_recommendations(track_name)
            if 'error' not in track_info:
                info_html = f"""
                <h4>Информация о трассе:</h4>
                <p><b>Название:</b> {track_info.get('name', 'N/A')}</p>
                <p><b>Длина:</b> {track_info.get('length', 'N/A')} км</p>
                <p><b>Характер:</b> {', '.join(track_info.get('characteristics', []))}</p>
                <p><b>Погодные условия:</b> {track_info.get('weather_tendency', 'N/A')}</p>
                """
                self.result_area.setHtml(info_html)
            else:
                # Если информация о трассе не найдена, показываем информацию об автомобиле
                self.load_car_info()
        except Exception as e:
            # В случае ошибки показываем информацию об автомобиле
            self.load_car_info()

    def run_optimization(self):
        """Запуск оптимизации настроек"""
        try:
            # Собираем условия
            conditions = {
                "temperature": self.temp_spinbox.value(),
                "race_duration": self.race_type.currentText(),
                "track": self.track_selector.currentText(),
                "weather": self.weather_selector.currentText(),
                "stint_strategy": self.stint_strategy.currentText()
            }
            
            # Создаем телеметрию на основе выбранного стиля
            brake_style = self.brake_style.currentText()
            balance = self.balance_selector.currentText()
            
            telemetry = {
                "brake_avg": 0.95 if brake_style == "aggressive" else (0.75 if brake_style == "late" else 0.85),
                "brake_tendency": brake_style,
                "throttle_exit": 0.88,
                "steering_smoothness": 0.75,
                "balance": balance
            }
            
            # Добавляем специфичные для гиперкаров параметры
            car_type = self.car_selector.currentText()
            if "hypercar" in car_type:
                telemetry.update({
                    "hybrid_efficiency": 0.8,
                    "fuel_consumption": 1.0
                })
            
            # Получаем рекомендации
            track_name = self.track_selector.currentText()
            
            recommendations = self.expert.recommend_setup(
                conditions, telemetry, car_type, track_name
            )
            
            # Отображаем результаты
            self.display_recommendations(recommendations)
            
        except Exception as e:
            self.result_area.setHtml(f"<p style='color: red;'>Ошибка: {e}</p>")

    def display_recommendations(self, recommendations):
        """Отображение рекомендаций"""
        adjustments = recommendations.get("adjustments", {})
        explanations = recommendations.get("explanations", [])
        confidence = recommendations.get("confidence", 0)
        car_type = recommendations.get("car_type", "")
        track_name = recommendations.get("track_name", "")
        
        html = f"""
        <div style="font-family: Arial, sans-serif;">
        <h3>🔧 Рекомендации по настройке</h3>
        <p><b>Автомобиль:</b> {car_type}</p>
        <p><b>Трасса:</b> {track_name}</p>
        <p><b>Уверенность:</b> <span style="color: {'green' if confidence > 0.7 else 'orange' if confidence > 0.5 else 'red'};">{confidence:.1%}</span></p>
        
        <h4>📊 Корректировки настроек:</h4>
        """
        
        if adjustments:
            html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
            html += "<tr style='background-color: #f0f0f0;'><th>Параметр</th><th>Изменение</th><th>Описание</th></tr>"
            
            for param, value in adjustments.items():
                color = "green" if value > 0 else "red" if value < 0 else "gray"
                direction = "↑" if value > 0 else "↓" if value < 0 else "→"
                
                # Описание параметра
                descriptions = {
                    "front_wing": "Передний антикрыло",
                    "rear_wing": "Заднее антикрыло", 
                    "tire_pressure_front": "Давление передних шин",
                    "tire_pressure_rear": "Давление задних шин",
                    "brake_bias": "Баланс тормозов",
                    "front_spring": "Передние пружины",
                    "rear_spring": "Задние пружины",
                    "differential_power": "Дифференциал (тяга)",
                    "differential_coast": "Дифференциал (накат)",
                    "hybrid_deployment": "Режим гибрида"
                }
                
                description = descriptions.get(param, param.replace("_", " ").title())
                
                html += f"""
                <tr>
                    <td><b>{description}</b></td>
                    <td style='color: {color}; text-align: center;'>{direction} {abs(value):.1f}</td>
                    <td style='font-size: 12px;'>{"Увеличить" if value > 0 else "Уменьшить" if value < 0 else "Без изменений"}</td>
                </tr>
                """
            
            html += "</table>"
        else:
            html += "<p><i>Настройки по умолчанию оптимальны для данных условий</i></p>"
        
        html += "<h4>💡 Объяснения:</h4><ul>"
        
        for explanation in explanations:
            html += f"<li>{explanation}</li>"
        
        if not explanations:
            html += "<li>Базовые настройки подходят для выбранных условий</li>"
        
        html += "</ul></div>"
        
        self.result_area.setHtml(html)

    def clear_results(self):
        """Очистка результатов"""
        self.load_car_info()