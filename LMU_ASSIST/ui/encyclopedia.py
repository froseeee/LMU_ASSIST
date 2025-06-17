import json
import os
from PyQt5 import QtWidgets, QtCore, QtGui

class EncyclopediaTab(QtWidgets.QWidget):
    """Улучшенная вкладка энциклопедии"""
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.cars_data = self.load_cars_data()
        self.tracks_data = self.load_tracks_data()
        self.setup_ui()
        
    def load_cars_data(self):
        """Загрузка данных об автомобилях"""
        try:
            with open('data/cars.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"lmu_cars": {}}
    
    def load_tracks_data(self):
        """Загрузка данных о трассах"""
        try:
            with open('data/tracks.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"tracks": {}}
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        
        # Левая панель с категориями
        left_panel = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        
        # Заголовок
        title_label = QtWidgets.QLabel("📘 Энциклопедия LMU")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; margin: 10px;")
        left_layout.addWidget(title_label)
        
        # Список категорий
        self.category_list = QtWidgets.QListWidget()
        self.category_list.setMaximumWidth(200)
        self.category_list.setStyleSheet("""
            QListWidget {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #555555;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
            QListWidget::item:hover {
                background-color: #5a5a5a;
            }
        """)
        
        # Добавляем категории
        categories = [
            "🏎️ Автомобили",
            "🏁 Трассы", 
            "⚙️ Настройки",
            "🏆 Стратегии",
            "📚 Руководства"
        ]
        
        for category in categories:
            self.category_list.addItem(category)
            
        self.category_list.currentItemChanged.connect(self.on_category_changed)
        left_layout.addWidget(self.category_list)
        
        left_layout.addStretch()
        layout.addWidget(left_panel)
        
        # Правая панель с контентом
        self.content_area = QtWidgets.QStackedWidget()
        self.content_area.setStyleSheet("""
            QStackedWidget {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
            }
        """)
        
        # Создаем страницы для каждой категории
        self.create_cars_page()
        self.create_tracks_page()
        self.create_setups_page()
        self.create_strategies_page()
        self.create_guides_page()
        
        layout.addWidget(self.content_area, 3)
        
        # Выбираем первую категорию по умолчанию
        self.category_list.setCurrentRow(0)
    
    def create_cars_page(self):
        """Создание страницы автомобилей"""
        cars_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(cars_widget)
        
        # Заголовок
        header = QtWidgets.QLabel("🏎️ Автомобили Le Mans Ultimate")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)
        
        # Создаем вкладки для категорий автомобилей
        cars_tabs = QtWidgets.QTabWidget()
        cars_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #3c3c3c;
            }
            QTabBar::tab {
                background-color: #4a4a4a;
                color: #ffffff;
                padding: 6px 12px;
                margin: 1px;
                border-radius: 3px;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
        """)
        
        # Добавляем категории автомобилей
        for category, cars in self.cars_data.get("lmu_cars", {}).items():
            category_widget = self.create_cars_category_widget(cars)
            cars_tabs.addTab(category_widget, category)
            
        layout.addWidget(cars_tabs)
        self.content_area.addWidget(cars_widget)
    
    def create_cars_category_widget(self, cars_dict):
        """Создание виджета для категории автомобилей"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        # Скроллируемая область
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        
        for car_name, car_data in cars_dict.items():
            car_card = self.create_car_card(car_name, car_data)
            content_layout.addWidget(car_card)
            
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return widget
    
    def create_car_card(self, car_name, car_data):
        """Создание карточки автомобиля"""
        card = QtWidgets.QGroupBox(car_name)
        card.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin: 5px;
                padding-top: 10px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0078d4;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        
        # Основная информация
        info_layout = QtWidgets.QGridLayout()
        
        info_items = [
            ("Категория:", car_data.get("category", "N/A")),
            ("Привод:", car_data.get("drivetrain", "N/A")),
            ("Мощность:", car_data.get("power", "N/A")),
            ("Вес:", car_data.get("weight", "N/A")),
            ("Топливный бак:", car_data.get("fuel_capacity", "N/A"))
        ]
        
        for i, (label, value) in enumerate(info_items):
            label_widget = QtWidgets.QLabel(label)
            label_widget.setStyleSheet("font-weight: bold; color: #cccccc;")
            value_widget = QtWidgets.QLabel(value)
            value_widget.setStyleSheet("color: #ffffff;")
            
            info_layout.addWidget(label_widget, i, 0)
            info_layout.addWidget(value_widget, i, 1)
            
        layout.addLayout(info_layout)
        
        # Характеристики
        if "characteristics" in car_data:
            char_label = QtWidgets.QLabel("Характеристики:")
            char_label.setStyleSheet("font-weight: bold; color: #0078d4; margin-top: 10px;")
            layout.addWidget(char_label)
            
            char_layout = QtWidgets.QGridLayout()
            characteristics = car_data["characteristics"]
            
            for i, (key, value) in enumerate(characteristics.items()):
                key_widget = QtWidgets.QLabel(f"{key.replace('_', ' ').title()}:")
                key_widget.setStyleSheet("color: #cccccc;")
                value_widget = QtWidgets.QLabel(value)
                value_widget.setStyleSheet("color: #ffffff;")
                
                char_layout.addWidget(key_widget, i, 0)
                char_layout.addWidget(value_widget, i, 1)
                
            layout.addLayout(char_layout)
        
        return card
    
    def create_tracks_page(self):
        """Создание страницы трасс"""
        tracks_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tracks_widget)
        
        # Заголовок
        header = QtWidgets.QLabel("🏁 Трассы")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)
        
        # Список трасс
        tracks_list = QtWidgets.QListWidget()
        tracks_list.setStyleSheet("""
            QListWidget {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #555555;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
        """)
        
        for track_name in self.tracks_data.get("tracks", {}).keys():
            tracks_list.addItem(f"🏁 {track_name}")
            
        tracks_list.currentItemChanged.connect(self.on_track_selected)
        
        # Разделяем на список и детали
        tracks_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        tracks_splitter.addWidget(tracks_list)
        
        # Область деталей трассы
        self.track_details = QtWidgets.QTextBrowser()
        self.track_details.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
                padding: 10px;
            }
        """)
        
        tracks_splitter.addWidget(self.track_details)
        tracks_splitter.setSizes([300, 700])
        
        layout.addWidget(tracks_splitter)
        self.content_area.addWidget(tracks_widget)
    
    def create_setups_page(self):
        """Создание страницы настроек"""
        setups_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(setups_widget)
        
        header = QtWidgets.QLabel("⚙️ Руководство по настройкам")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)
        
        content = QtWidgets.QTextBrowser()
        content.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
                padding: 15px;
            }
        """)
        
        setup_guide = """
        <h2 style="color: #0078d4;">🔧 Основы настройки автомобиля</h2>
        
        <h3 style="color: #ffa500;">Аэродинамика</h3>
        <ul>
            <li><b>Переднее крыло:</b> Влияет на поворачиваемость и прижимную силу спереди</li>
            <li><b>Заднее крыло:</b> Обеспечивает стабильность и прижимную силу сзади</li>
            <li><b>Правило:</b> Больше крыла = больше прижимная сила, но меньше максимальная скорость</li>
        </ul>
        
        <h3 style="color: #ffa500;">Подвеска</h3>
        <ul>
            <li><b>Пружины:</b> Жесткие для гладких трасс, мягкие для неровных</li>
            <li><b>Амортизаторы:</b> Контролируют перенос веса</li>
            <li><b>Стабилизаторы:</b> Влияют на баланс в поворотах</li>
        </ul>
        
        <h3 style="color: #ffa500;">Тормоза</h3>
        <ul>
            <li><b>Баланс тормозов:</b> 50-70% (передние/задние)</li>
            <li><b>Давление:</b> Максимальная сила торможения</li>
            <li><b>Воздуховоды:</b> Охлаждение тормозных дисков</li>
        </ul>
        
        <h3 style="color: #ffa500;">Шины</h3>
        <ul>
            <li><b>Давление:</b> Влияет на износ и сцепление</li>
            <li><b>Развал:</b> Оптимизация контактного пятна</li>
            <li><b>Схождение:</b> Стабильность на прямых</li>
        </ul>
        
        <h3 style="color: #ffa500;">Дифференциал</h3>
        <ul>
            <li><b>Предварительная нагрузка:</b> Базовое блокирование</li>
            <li><b>На тяге:</b> Блокирование при ускорении</li>
            <li><b>На торможении:</b> Блокирование при замедлении</li>
        </ul>
        """
        
        content.setHtml(setup_guide)
        layout.addWidget(content)
        self.content_area.addWidget(setups_widget)
    
    def create_strategies_page(self):
        """Создание страницы стратегий"""
        strategies_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(strategies_widget)
        
        header = QtWidgets.QLabel("🏆 Гоночные стратегии")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)
        
        content = QtWidgets.QTextBrowser()
        content.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
                padding: 15px;
            }
        """)
        
        strategies_guide = """
        <h2 style="color: #0078d4;">🎯 Стратегии гонок на выносливость</h2>
        
        <h3 style="color: #ffa500;">Управление топливом</h3>
        <ul>
            <li><b>Экономия топлива:</b> Уменьшение оборотов на 500-1000 rpm на прямых</li>
            <li><b>Планирование пит-стопов:</b> Рассчитывай заправки заранее</li>
            <li><b>Смеси:</b> Богатая для гонки, бедная для экономии</li>
        </ul>
        
        <h3 style="color: #ffa500;">Управление шинами</h3>
        <ul>
            <li><b>Прогрев:</b> Плавное увеличение темпа в первых кругах</li>
            <li><b>Температура:</b> Оптимальная 80-110°C</li>
            <li><b>Износ:</b> Избегай блокировок и пробуксовок</li>
        </ul>
        
        <h3 style="color: #ffa500;">Техника пит-стопов</h3>
        <ul>
            <li><b>Въезд:</b> Точно попадай в бокс</li>
            <li><b>Остановка:</b> Четко на отметке</li>
            <li><b>Выезд:</b> Не превышай лимит скорости в пит-лейне</li>
        </ul>
        
        <h3 style="color: #ffa500;">Тактика обгонов</h3>
        <ul>
            <li><b>Подготовка:</b> Следуй близко для слипстрима</li>
            <li><b>Выполнение:</b> Начинай маневр рано</li>
            <li><b>Защита:</b> Одно движение для защиты позиции</li>
        </ul>
        
        <h3 style="color: #ffa500;">Погодные условия</h3>
        <ul>
            <li><b>Дождь:</b> Плавные движения, избегай луж</li>
            <li><b>Переход:</b> Вовремя меняй резину</li>
            <li><b>Видимость:</b> Увеличивай дистанцию</li>
        </ul>
        """
        
        content.setHtml(strategies_guide)
        layout.addWidget(content)
        self.content_area.addWidget(strategies_widget)
    
    def create_guides_page(self):
        """Создание страницы руководств"""
        guides_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(guides_widget)
        
        header = QtWidgets.QLabel("📚 Обучающие материалы")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)
        
        content = QtWidgets.QTextBrowser()
        content.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
                padding: 15px;
            }
        """)
        
        guides_content = """
        <h2 style="color: #0078d4;">🎓 Руководства для начинающих</h2>
        
        <h3 style="color: #ffa500;">Основы управления</h3>
        <ul>
            <li><b>Положение рук:</b> 9:15 или 10:10 на руле</li>
            <li><b>Торможение:</b> Плавное нажатие и отпускание</li>
            <li><b>Ускорение:</b> Прогрессивное открытие газа</li>
            <li><b>Траектория:</b> Поздний вход, ранний выход</li>
        </ul>
        
        <h3 style="color: #ffa500;">Техника прохождения поворотов</h3>
        <ul>
            <li><b>Торможение:</b> До поворота по прямой</li>
            <li><b>Вход:</b> Плавно довернуть к апексу</li>
            <li><b>Апекс:</b> Самая близкая точка к внутреннему краю</li>
            <li><b>Выход:</b> Раннее ускорение с распусканием траектории</li>
        </ul>
        
        <h3 style="color: #ffa500;">Анализ телеметрии</h3>
        <ul>
            <li><b>Время кругов:</b> Сравнивай с эталоном</li>
            <li><b>Секторы:</b> Найди слабые места</li>
            <li><b>Скорости:</b> Анализируй скорость в поворотах</li>
            <li><b>G-силы:</b> Оценивай плавность вождения</li>
        </ul>
        
        <h3 style="color: #ffa500;">Ментальная подготовка</h3>
        <ul>
            <li><b>Концентрация:</b> Сосредоточься на процессе</li>
            <li><b>Терпение:</b> Прогресс приходит со временем</li>
            <li><b>Анализ:</b> Изучай свои ошибки</li>
            <li><b>Практика:</b> Регулярные тренировки</li>
        </ul>
        
        <h3 style="color: #ffa500;">Полезные ресурсы</h3>
        <ul>
            <li><b>Видео:</b> Записи быстрых кругов</li>
            <li><b>Гайды:</b> Специфичные для трасс руководства</li>
            <li><b>Сообщество:</b> Форумы и Discord серверы</li>
            <li><b>Тренеры:</b> Персональное обучение</li>
        </ul>
        """
        
        content.setHtml(guides_content)
        layout.addWidget(content)
        self.content_area.addWidget(guides_widget)
    
    def on_category_changed(self, current, previous):
        """Обработка смены категории"""
        if current:
            row = self.category_list.row(current)
            self.content_area.setCurrentIndex(row)
    
    def on_track_selected(self, current, previous):
        """Обработка выбора трассы"""
        if current:
            track_name = current.text().replace("🏁 ", "")
            track_data = self.tracks_data.get("tracks", {}).get(track_name, {})
            
            if track_data:
                self.display_track_details(track_name, track_data)
    
    def display_track_details(self, track_name, track_data):
        """Отображение деталей трассы"""
        html_content = f"""
        <h2 style="color: #0078d4;">🏁 {track_name}</h2>
        <h3 style="color: #ffa500;">{track_data.get('full_name', '')}</h3>
        
        <h4>Основная информация:</h4>
        <ul>
            <li><b>Страна:</b> {track_data.get('country', 'N/A')}</li>
            <li><b>Длина:</b> {track_data.get('length', 'N/A')} км</li>
            <li><b>Повороты:</b> {track_data.get('corners', 'N/A')}</li>
            <li><b>Рекорд круга:</b> {track_data.get('lap_record', 'N/A')}</li>
        </ul>
        
        <h4>Характеристики:</h4>
        <ul>
        """
        
        characteristics = track_data.get('characteristics', {})
        for key, value in characteristics.items():
            html_content += f"<li><b>{key.replace('_', ' ').title()}:</b> {value}</li>"
        
        html_content += "</ul>"
        
        # Добавляем информацию о секторах
        if 'sectors' in track_data:
            html_content += "<h4>Сектора:</h4>"
            for i, sector in enumerate(track_data['sectors'], 1):
                html_content += f"""
                <h5 style="color: #ffa500;">Сектор {i}: {sector.get('name', '')}</h5>
                <p>{sector.get('description', '')}</p>
                <p><b>Ключевые повороты:</b> {', '.join(sector.get('key_corners', []))}</p>
                <p><b>Фокус настройки:</b> {sector.get('setup_focus', '')}</p>
                """
        
        # Добавляем рекомендации по настройке
        if 'setup_recommendations' in track_data:
            html_content += "<h4>Рекомендации по настройке:</h4>"
            setup_recs = track_data['setup_recommendations']
            
            for category, settings in setup_recs.items():
                html_content += f"<h5 style='color: #ffa500;'>{category.title()}:</h5><ul>"
                for setting, value in settings.items():
                    if setting != 'reason':
                        html_content += f"<li><b>{setting.replace('_', ' ').title()}:</b> {value}</li>"
                if 'reason' in settings:
                    html_content += f"<li><i>Причина: {settings['reason']}</i></li>"
                html_content += "</ul>"
        
        # Добавляем советы по вождению
        if 'driving_tips' in track_data:
            html_content += "<h4>Советы по вождению:</h4><ul>"
            for tip in track_data['driving_tips']:
                html_content += f"<li>{tip}</li>"
            html_content += "</ul>"
        
        self.track_details.setHtml(html_content)
