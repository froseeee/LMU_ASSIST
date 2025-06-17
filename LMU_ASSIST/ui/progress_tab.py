import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np

class ProgressTab(QtWidgets.QWidget):
    """Вкладка прогресса с визуализацией статистики"""
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()
        self.load_progress_data()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        
        # Заголовок
        header = QtWidgets.QLabel("📈 Анализ прогресса")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; margin: 10px;")
        layout.addWidget(header)
        
        # Панель фильтров
        filters_panel = self.create_filters_panel()
        layout.addWidget(filters_panel)
        
        # Основная область с графиками
        main_area = self.create_main_area()
        layout.addWidget(main_area, 1)
        
        # Панель статистики
        stats_panel = self.create_stats_panel()
        layout.addWidget(stats_panel)
    
    def create_filters_panel(self):
        """Создание панели фильтров"""
        panel = QtWidgets.QGroupBox("🔍 Фильтры")
        panel.setMaximumHeight(80)
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin: 5px;
                padding-top: 15px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0078d4;
            }
        """)
        
        layout = QtWidgets.QHBoxLayout(panel)
        
        # Выбор трассы
        layout.addWidget(QtWidgets.QLabel("Трасса:"))
        self.track_filter = QtWidgets.QComboBox()
        self.track_filter.addItems(["Все трассы", "Le Mans", "Silverstone", "Spa", "Monza"])
        self.track_filter.setStyleSheet("""
            QComboBox {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
        """)
        layout.addWidget(self.track_filter)
        
        # Выбор автомобиля
        layout.addWidget(QtWidgets.QLabel("Автомобиль:"))
        self.car_filter = QtWidgets.QComboBox()
        self.car_filter.addItems(["Все автомобили", "Toyota GR010", "Ferrari 499P", "Porsche 963"])
        self.car_filter.setStyleSheet(self.track_filter.styleSheet())
        layout.addWidget(self.car_filter)
        
        # Период
        layout.addWidget(QtWidgets.QLabel("Период:"))
        self.period_filter = QtWidgets.QComboBox()
        self.period_filter.addItems(["Последние 7 дней", "Последний месяц", "Последние 3 месяца", "Все время"])
        self.period_filter.setStyleSheet(self.track_filter.styleSheet())
        layout.addWidget(self.period_filter)
        
        # Кнопка обновления
        self.update_btn = QtWidgets.QPushButton("🔄 Обновить")
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: #ffffff;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        self.update_btn.clicked.connect(self.update_charts)
        layout.addWidget(self.update_btn)
        
        layout.addStretch()
        
        return panel
    
    def create_main_area(self):
        """Создание основной области с графиками"""
        # Используем горизонтальный сплиттер
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        
        # Левая часть - график времен кругов
        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        
        lap_times_label = QtWidgets.QLabel("⏱️ Динамика времен кругов")
        lap_times_label.setStyleSheet("font-weight: bold; color: #ffa500; margin: 5px;")
        left_layout.addWidget(lap_times_label)
        
        # Создаем график времен кругов
        self.lap_times_figure = Figure(figsize=(8, 6), facecolor='#2b2b2b')
        self.lap_times_canvas = FigureCanvas(self.lap_times_figure)
        self.lap_times_canvas.setStyleSheet("background-color: #2b2b2b;")
        left_layout.addWidget(self.lap_times_canvas)
        
        main_splitter.addWidget(left_widget)
        
        # Правая часть - вертикальный сплиттер с дополнительными графиками
        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        
        # График консистентности
        consistency_widget = QtWidgets.QWidget()
        consistency_layout = QtWidgets.QVBoxLayout(consistency_widget)
        
        consistency_label = QtWidgets.QLabel("📊 Консистентность")
        consistency_label.setStyleSheet("font-weight: bold; color: #ffa500; margin: 5px;")
        consistency_layout.addWidget(consistency_label)
        
        self.consistency_figure = Figure(figsize=(6, 3), facecolor='#2b2b2b')
        self.consistency_canvas = FigureCanvas(self.consistency_figure)
        self.consistency_canvas.setStyleSheet("background-color: #2b2b2b;")
        consistency_layout.addWidget(self.consistency_canvas)
        
        right_splitter.addWidget(consistency_widget)
        
        # График улучшений по секторам
        sectors_widget = QtWidgets.QWidget()
        sectors_layout = QtWidgets.QVBoxLayout(sectors_widget)
        
        sectors_label = QtWidgets.QLabel("🎯 Анализ по секторам")
        sectors_label.setStyleSheet("font-weight: bold; color: #ffa500; margin: 5px;")
        sectors_layout.addWidget(sectors_label)
        
        self.sectors_figure = Figure(figsize=(6, 3), facecolor='#2b2b2b')
        self.sectors_canvas = FigureCanvas(self.sectors_figure)
        self.sectors_canvas.setStyleSheet("background-color: #2b2b2b;")
        sectors_layout.addWidget(self.sectors_canvas)
        
        right_splitter.addWidget(sectors_widget)
        
        main_splitter.addWidget(right_splitter)
        main_splitter.setSizes([500, 400])
        
        return main_splitter
    
    def create_stats_panel(self):
        """Создание панели статистики"""
        panel = QtWidgets.QGroupBox("📋 Статистика")
        panel.setMaximumHeight(120)
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin: 5px;
                padding-top: 15px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0078d4;
            }
        """)
        
        layout = QtWidgets.QGridLayout(panel)
        
        # Создаем карточки статистики
        self.stats_cards = {}
        
        stats_data = [
            ('total_laps', 'Всего кругов', '0', '#4ecdc4'),
            ('best_lap', 'Лучший круг', '0:00.000', '#ff6b6b'),
            ('avg_lap', 'Средний круг', '0:00.000', '#ffa500'),
            ('improvement', 'Улучшение', '0.000 сек', '#4ecdc4'),
            ('consistency', 'Стабильность', '0%', '#a8e6cf'),
            ('sessions', 'Сессий', '0', '#c7ceea')
        ]
        
        for i, (key, title, value, color) in enumerate(stats_data):
            card = self.create_stat_card(title, value, color)
            self.stats_cards[key] = card
            
            row = i // 3
            col = i % 3
            layout.addWidget(card, row, col)
        
        return panel
    
    def create_stat_card(self, title, value, color):
        """Создание карточки статистики"""
        card = QtWidgets.QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #3c3c3c;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(10, 5, 10, 5)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 16px;")
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(value_label)
        
        # Сохраняем ссылку на лейбл значения для обновления
        card.value_label = value_label
        
        return card
    
    def load_progress_data(self):
        """Загрузка данных прогресса"""
        # Генерируем тестовые данные
        self.generate_sample_data()
        self.update_charts()
    
    def generate_sample_data(self):
        """Генерация тестовых данных"""
        import random
        from datetime import datetime, timedelta
        
        # Генерируем данные времен кругов за последние 30 дней
        self.lap_times_data = []
        base_time = 90.0  # Базовое время круга
        
        for i in range(150):  # 150 кругов
            # Постепенное улучшение с некоторой вариацией
            improvement = i * 0.01  # Улучшение на 0.01 сек за круг
            variation = random.uniform(-0.5, 0.5)  # Случайная вариация
            lap_time = base_time - improvement + variation
            
            date = datetime.now() - timedelta(days=30) + timedelta(days=i*0.2)
            
            self.lap_times_data.append({
                'date': date,
                'lap_time': lap_time,
                'track': random.choice(['Le Mans', 'Silverstone', 'Spa']),
                'car': random.choice(['Toyota GR010', 'Ferrari 499P']),
                'sector_1': lap_time * 0.33,
                'sector_2': lap_time * 0.33,
                'sector_3': lap_time * 0.34
            })
        
        # Сортируем по дате
        self.lap_times_data.sort(key=lambda x: x['date'])
    
    def update_charts(self):
        """Обновление графиков"""
        self.update_lap_times_chart()
        self.update_consistency_chart()
        self.update_sectors_chart()
        self.update_statistics()
    
    def update_lap_times_chart(self):
        """Обновление графика времен кругов"""
        self.lap_times_figure.clear()
        ax = self.lap_times_figure.add_subplot(111)
        
        # Настройка темной темы
        ax.set_facecolor('#2b2b2b')
        self.lap_times_figure.patch.set_facecolor('#2b2b2b')
        
        # Получаем данные
        dates = [data['date'] for data in self.lap_times_data]
        lap_times = [data['lap_time'] for data in self.lap_times_data]
        
        # Строим график
        ax.plot(dates, lap_times, color='#4ecdc4', linewidth=2, alpha=0.7, label='Время круга')
        
        # Линия тренда
        if len(lap_times) > 1:
            z = np.polyfit(range(len(lap_times)), lap_times, 1)
            p = np.poly1d(z)
            ax.plot(dates, p(range(len(lap_times))), color='#ff6b6b', linewidth=2, linestyle='--', label='Тренд')
        
        # Настройка осей
        ax.set_xlabel('Дата', color='white')
        ax.set_ylabel('Время круга (сек)', color='white')
        ax.set_title('Динамика времен кругов', color='white', fontweight='bold')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3, color='white')
        ax.legend(facecolor='#3c3c3c', edgecolor='white', labelcolor='white')
        
        # Поворачиваем подписи дат
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        self.lap_times_figure.tight_layout()
        self.lap_times_canvas.draw()
    
    def update_consistency_chart(self):
        """Обновление графика консистентности"""
        self.consistency_figure.clear()
        ax = self.consistency_figure.add_subplot(111)
        
        # Настройка темной темы
        ax.set_facecolor('#2b2b2b')
        self.consistency_figure.patch.set_facecolor('#2b2b2b')
        
        # Рассчитываем консистентность по скользящему окну
        window_size = 10
        consistency_scores = []
        dates = []
        
        for i in range(window_size, len(self.lap_times_data)):
            window_data = self.lap_times_data[i-window_size:i]
            times = [d['lap_time'] for d in window_data]
            
            # Консистентность как обратная величина стандартного отклонения
            std_dev = np.std(times)
            consistency = max(0, 100 - std_dev * 100)  # Преобразуем в проценты
            
            consistency_scores.append(consistency)
            dates.append(window_data[-1]['date'])
        
        if consistency_scores:
            ax.fill_between(dates, consistency_scores, alpha=0.6, color='#a8e6cf', label='Консистентность')
            ax.plot(dates, consistency_scores, color='#4ecdc4', linewidth=2)
        
        ax.set_xlabel('Дата', color='white')
        ax.set_ylabel('Консистентность (%)', color='white')
        ax.set_title('Развитие консистентности', color='white', fontweight='bold')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3, color='white')
        ax.set_ylim(0, 100)
        
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        self.consistency_figure.tight_layout()
        self.consistency_canvas.draw()
    
    def update_sectors_chart(self):
        """Обновление графика по секторам"""
        self.sectors_figure.clear()
        ax = self.sectors_figure.add_subplot(111)
        
        # Настройка темной темы
        ax.set_facecolor('#2b2b2b')
        self.sectors_figure.patch.set_facecolor('#2b2b2b')
        
        # Рассчитываем средние времена по секторам
        recent_data = self.lap_times_data[-50:]  # Последние 50 кругов
        
        if recent_data:
            sector_1_times = [d['sector_1'] for d in recent_data]
            sector_2_times = [d['sector_2'] for d in recent_data]
            sector_3_times = [d['sector_3'] for d in recent_data]
            
            sectors = ['Сектор 1', 'Сектор 2', 'Сектор 3']
            avg_times = [
                np.mean(sector_1_times),
                np.mean(sector_2_times),
                np.mean(sector_3_times)
            ]
            
            colors = ['#ff6b6b', '#4ecdc4', '#ffa500']
            bars = ax.bar(sectors, avg_times, color=colors, alpha=0.8)
            
            # Добавляем значения на столбцы
            for bar, time in zip(bars, avg_times):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{time:.2f}', ha='center', va='bottom', color='white', fontweight='bold')
        
        ax.set_ylabel('Время (сек)', color='white')
        ax.set_title('Средние времена по секторам', color='white', fontweight='bold')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3, color='white', axis='y')
        
        self.sectors_figure.tight_layout()
        self.sectors_canvas.draw()
    
    def update_statistics(self):
        """Обновление статистики"""
        if not self.lap_times_data:
            return
        
        lap_times = [d['lap_time'] for d in self.lap_times_data]
        
        # Рассчитываем статистику
        total_laps = len(lap_times)
        best_lap = min(lap_times)
        avg_lap = np.mean(lap_times)
        
        # Улучшение (разница между первыми и последними 10 кругами)
        if len(lap_times) >= 20:
            first_10 = np.mean(lap_times[:10])
            last_10 = np.mean(lap_times[-10:])
            improvement = first_10 - last_10
        else:
            improvement = 0
        
        # Консистентность
        consistency = max(0, 100 - np.std(lap_times) * 50)
        
        # Количество сессий (примерно)
        sessions = max(1, total_laps // 20)
        
        # Обновляем карточки
        self.stats_cards['total_laps'].value_label.setText(str(total_laps))
        self.stats_cards['best_lap'].value_label.setText(self.format_lap_time(best_lap))
        self.stats_cards['avg_lap'].value_label.setText(self.format_lap_time(avg_lap))
        self.stats_cards['improvement'].value_label.setText(f"{improvement:.3f} сек")
        self.stats_cards['consistency'].value_label.setText(f"{consistency:.1f}%")
        self.stats_cards['sessions'].value_label.setText(str(sessions))
    
    def format_lap_time(self, seconds):
        """Форматирование времени круга"""
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes}:{seconds:06.3f}"
