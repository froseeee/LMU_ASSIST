#!/usr/bin/env python3
"""
Демонстрация современной системы тем LMU Assistant
Показывает все компоненты и их стили
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QScrollArea, QGridLayout, QLabel, QLineEdit, QComboBox,
    QCheckBox, QRadioButton, QSlider, QProgressBar, QPushButton, QGroupBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

# Импортируем нашу систему тем
from theme import apply_theme, ThemeType, get_current_theme, set_widget_style_class
from theme_utils import (
    ModernCard, ModernButton, LoadingSpinner, ProgressCard, StatCard,
    NotificationToast, GlassPanel, ModernSlider, IconButton, ModernDialog,
    show_notification, create_separator, apply_glow_effect
)


class ThemeDemo(QMainWindow):
    """Демонстрация тем"""
    
    def __init__(self):
        super().__init__()
        self.current_theme = ThemeType.DARK
        self.notification_counter = 0
        self.setup_ui()
        self.setup_demo_timer()
        
        # Применяем тему
        apply_theme(QApplication.instance(), self.current_theme)
    
    def setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("LMU Assistant - Theme Demo")
        self.setGeometry(100, 100, 1400, 900)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Заголовок и управление темами
        self.create_header(layout)
        
        # Основной контент в табах
        self.create_content_tabs(layout)
        
        # Статус бар
        self.statusBar().showMessage("🎨 Theme Demo - Демонстрация современных тем LMU Assistant")
    
    def create_header(self, parent_layout):
        """Создание заголовка"""
        header_layout = QHBoxLayout()
        
        # Заголовок
        title = QLabel("🎨 LMU Assistant Theme Demo")
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: 700;
                margin: 16px 0;
            }
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Кнопки переключения тем
        theme_layout = QHBoxLayout()
        theme_layout.setSpacing(8)
        
        dark_btn = ModernButton("🌙 Dark", "primary")
        dark_btn.clicked.connect(lambda: self.switch_theme(ThemeType.DARK))
        theme_layout.addWidget(dark_btn)
        
        light_btn = ModernButton("☀️ Light", "secondary")
        light_btn.clicked.connect(lambda: self.switch_theme(ThemeType.LIGHT))
        theme_layout.addWidget(light_btn)
        
        racing_btn = ModernButton("🏁 Racing", "danger")
        racing_btn.clicked.connect(lambda: self.switch_theme(ThemeType.RACING))
        theme_layout.addWidget(racing_btn)
        
        # Кнопка уведомлений
        notify_btn = ModernButton("🔔 Test Notification", "success")
        notify_btn.clicked.connect(self.show_test_notification)
        theme_layout.addWidget(notify_btn)
        
        header_layout.addLayout(theme_layout)
        parent_layout.addLayout(header_layout)
        
        # Разделитель
        parent_layout.addWidget(create_separator())
    
    def create_content_tabs(self, parent_layout):
        """Создание вкладок с контентом"""
        tabs = QTabWidget()
        
        # Вкладка компонентов
        components_tab = self.create_components_tab()
        tabs.addTab(components_tab, "🧩 Components")
        
        # Вкладка карточек
        cards_tab = self.create_cards_tab()
        tabs.addTab(cards_tab, "🃏 Cards")
        
        # Вкладка форм
        forms_tab = self.create_forms_tab()
        tabs.addTab(forms_tab, "📝 Forms")
        
        # Вкладка статистики
        stats_tab = self.create_stats_tab()
        tabs.addTab(stats_tab, "📊 Statistics")
        
        parent_layout.addWidget(tabs)
    
    def create_components_tab(self):
        """Вкладка базовых компонентов"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.NoFrame)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(24)
        
        # Кнопки
        buttons_group = QGroupBox("Кнопки")
        buttons_layout = QHBoxLayout(buttons_group)
        
        primary_btn = ModernButton("Primary", "primary")
        secondary_btn = ModernButton("Secondary", "secondary")
        success_btn = ModernButton("Success", "success")
        warning_btn = ModernButton("Warning", "warning")
        danger_btn = ModernButton("Danger", "danger")
        ghost_btn = ModernButton("Ghost", "ghost")
        
        for btn in [primary_btn, secondary_btn, success_btn, warning_btn, danger_btn, ghost_btn]:
            buttons_layout.addWidget(btn)
        
        layout.addWidget(buttons_group)
        
        # Иконочные кнопки
        icon_buttons_group = QGroupBox("Иконочные кнопки")
        icon_layout = QHBoxLayout(icon_buttons_group)
        
        icons = ["⚙️", "🎯", "📊", "🔍", "💾", "🔄", "❌"]
        for icon in icons:
            icon_btn = IconButton(icon, 40)
            icon_layout.addWidget(icon_btn)
        
        layout.addWidget(icon_buttons_group)
        
        # Элементы формы
        form_group = QGroupBox("Элементы форм")
        form_layout = QGridLayout(form_group)
        
        # Текстовые поля
        form_layout.addWidget(QLabel("Текстовое поле:"), 0, 0)
        line_edit = QLineEdit("Пример текста")
        form_layout.addWidget(line_edit, 0, 1)
        
        # Комбобокс
        form_layout.addWidget(QLabel("Выпадающий список:"), 1, 0)
        combo = QComboBox()
        combo.addItems(["Опция 1", "Опция 2", "Опция 3"])
        form_layout.addWidget(combo, 1, 1)
        
        # Чекбоксы
        form_layout.addWidget(QLabel("Чекбоксы:"), 2, 0)
        check_layout = QHBoxLayout()
        check1 = QCheckBox("Опция A")
        check2 = QCheckBox("Опция B")
        check3 = QCheckBox("Опция C")
        check1.setChecked(True)
        check_layout.addWidget(check1)
        check_layout.addWidget(check2)
        check_layout.addWidget(check3)
        form_layout.addLayout(check_layout, 2, 1)
        
        # Радиокнопки
        form_layout.addWidget(QLabel("Радиокнопки:"), 3, 0)
        radio_layout = QHBoxLayout()
        radio1 = QRadioButton("Выбор 1")
        radio2 = QRadioButton("Выбор 2")
        radio3 = QRadioButton("Выбор 3")
        radio2.setChecked(True)
        radio_layout.addWidget(radio1)
        radio_layout.addWidget(radio2)
        radio_layout.addWidget(radio3)
        form_layout.addLayout(radio_layout, 3, 1)
        
        layout.addWidget(form_group)
        
        # Слайдеры и прогресс-бары
        controls_group = QGroupBox("Слайдеры и прогресс")
        controls_layout = QVBoxLayout(controls_group)
        
        # Обычный слайдер
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(75)
        controls_layout.addWidget(QLabel("Обычный слайдер:"))
        controls_layout.addWidget(slider)
        
        # Современный слайдер
        modern_slider = ModernSlider("Современный слайдер", 0, 100, 60, "%")
        controls_layout.addWidget(modern_slider)
        
        # Прогресс-бары
        controls_layout.addWidget(QLabel("Прогресс-бары:"))
        
        progress1 = QProgressBar()
        progress1.setValue(45)
        controls_layout.addWidget(progress1)
        
        progress2 = QProgressBar()
        progress2.setValue(78)
        set_widget_style_class(progress2, "success")
        controls_layout.addWidget(progress2)
        
        progress3 = QProgressBar()
        progress3.setValue(90)
        set_widget_style_class(progress3, "warning")
        controls_layout.addWidget(progress3)
        
        layout.addWidget(controls_group)
        
        # Спиннеры
        spinners_group = QGroupBox("Индикаторы загрузки")
        spinners_layout = QHBoxLayout(spinners_group)
        
        for size in [16, 24, 32, 48]:
            spinner = LoadingSpinner(size)
            spinner.start()
            spinners_layout.addWidget(spinner)
        
        layout.addWidget(spinners_group)
        
        scroll.setWidget(content)
        return scroll
    
    def create_cards_tab(self):
        """Вкладка с карточками"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.NoFrame)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(24)
        
        # Обычные карточки
        cards_layout = QGridLayout()
        
        # Простая карточка
        simple_card = ModernCard(
            "Простая карточка",
            "Это пример простой карточки с заголовком и описанием."
        )
        cards_layout.addWidget(simple_card, 0, 0)
        
        # Кликабельная карточка
        clickable_card = ModernCard(
            "Кликабельная карточка",
            "Эта карточка реагирует на клики и имеет анимации.",
            clickable=True
        )
        clickable_card.clicked.connect(lambda: self.show_notification("Карточка нажата!", "info"))
        cards_layout.addWidget(clickable_card, 0, 1)
        
        # Стеклянная панель
        glass_panel = GlassPanel()
        glass_layout = QVBoxLayout(glass_panel)
        glass_layout.addWidget(QLabel("🌟 Стеклянная панель"))
        glass_layout.addWidget(QLabel("Панель с эффектом размытого стекла"))
        apply_glow_effect(glass_panel)
        cards_layout.addWidget(glass_panel, 0, 2)
        
        layout.addLayout(cards_layout)
        
        # Карточки прогресса
        progress_layout = QHBoxLayout()
        
        progress_card1 = ProgressCard("Задача A", 65)
        progress_card2 = ProgressCard("Задача B", 90)
        progress_card3 = ProgressCard("Задача C", 30)
        
        progress_layout.addWidget(progress_card1)
        progress_layout.addWidget(progress_card2)
        progress_layout.addWidget(progress_card3)
        
        layout.addLayout(progress_layout)
        
        scroll.setWidget(content)
        return scroll
    
    def create_forms_tab(self):
        """Вкладка с формами"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.NoFrame)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(24)
        
        # Форма настроек
        settings_card = ModernCard("⚙️ Настройки приложения", "")
        settings_layout = QVBoxLayout()
        
        # Настройки телеметрии
        telemetry_group = QGroupBox("Телеметрия")
        telemetry_layout = QGridLayout(telemetry_group)
        
        telemetry_layout.addWidget(QLabel("UDP Порт:"), 0, 0)
        port_edit = QLineEdit("20777")
        telemetry_layout.addWidget(port_edit, 0, 1)
        
        telemetry_layout.addWidget(QLabel("Частота обновления:"), 1, 0)
        frequency_slider = ModernSlider("", 10, 100, 50, " мс")
        telemetry_layout.addWidget(frequency_slider, 1, 1)
        
        settings_layout.addWidget(telemetry_group)
        
        # Настройки отображения
        display_group = QGroupBox("Отображение")
        display_layout = QVBoxLayout(display_group)
        
        fps_check = QCheckBox("Показывать FPS")
        fps_check.setChecked(True)
        display_layout.addWidget(fps_check)
        
        overlay_check = QCheckBox("Включить оверлей")
        overlay_check.setChecked(True)
        display_layout.addWidget(overlay_check)
        
        smooth_check = QCheckBox("Плавная анимация")
        smooth_check.setChecked(True)
        display_layout.addWidget(smooth_check)
        
        settings_layout.addWidget(display_group)
        
        # Кнопки действий
        actions_layout = QHBoxLayout()
        save_btn = ModernButton("💾 Сохранить", "success")
        reset_btn = ModernButton("🔄 Сбросить", "secondary")
        cancel_btn = ModernButton("❌ Отмена", "ghost")
        
        actions_layout.addWidget(save_btn)
        actions_layout.addWidget(reset_btn)
        actions_layout.addStretch()
        actions_layout.addWidget(cancel_btn)
        
        settings_layout.addLayout(actions_layout)
        settings_card.layout().addLayout(settings_layout)
        
        layout.addWidget(settings_card)
        
        scroll.setWidget(content)
        return scroll
    
    def create_stats_tab(self):
        """Вкладка статистики"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.NoFrame)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(24)
        
        # Статистические карточки
        stats_layout = QGridLayout()
        
        # Основная статистика
        stats_data = [
            ("Всего кругов", "1,247", "🏁", None),
            ("Лучший круг", "1:23.456", "⏱️", "#10B981"),
            ("Средняя скорость", "187 км/ч", "🏎️", "#3B82F6"),
            ("Время в игре", "142 ч", "⏰", "#F59E0B"),
            ("Аварий", "23", "💥", "#EF4444"),
            ("Подиумов", "89", "🏆", "#F59E0B"),
        ]
        
        for i, (title, value, icon, color) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            stat_card = StatCard(title, value, icon, color)
            stats_layout.addWidget(stat_card, row, col)
        
        layout.addLayout(stats_layout)
        
        # Дополнительная информация
        info_card = ModernCard("📈 Анализ производительности", "")
        info_layout = QVBoxLayout()
        
        # Прогресс по категориям
        categories = [
            ("Торможение", 85),
            ("Ускорение", 78),
            ("Повороты", 92),
            ("Консистентность", 67),
        ]
        
        for category, progress in categories:
            cat_layout = QHBoxLayout()
            cat_layout.addWidget(QLabel(category))
            cat_layout.addStretch()
            
            progress_bar = QProgressBar()
            progress_bar.setValue(progress)
            progress_bar.setFixedWidth(200)
            
            # Цвет по уровню
            if progress >= 80:
                set_widget_style_class(progress_bar, "success")
            elif progress >= 60:
                set_widget_style_class(progress_bar, "warning")
            
            cat_layout.addWidget(progress_bar)
            cat_layout.addWidget(QLabel(f"{progress}%"))
            
            info_layout.addLayout(cat_layout)
        
        info_card.layout().addLayout(info_layout)
        layout.addWidget(info_card)
        
        scroll.setWidget(content)
        return scroll
    
    def switch_theme(self, theme_type: ThemeType):
        """Переключение темы"""
        self.current_theme = theme_type
        apply_theme(QApplication.instance(), theme_type)
        
        # Показываем уведомление
        theme_names = {
            ThemeType.DARK: "Dark",
            ThemeType.LIGHT: "Light", 
            ThemeType.RACING: "Racing"
        }
        
        self.show_notification(
            f"Тема изменена на {theme_names[theme_type]}",
            "success"
        )
    
    def show_test_notification(self):
        """Показать тестовое уведомление"""
        self.notification_counter += 1
        
        types = ["info", "success", "warning", "error"]
        messages = [
            f"Информационное сообщение #{self.notification_counter}",
            f"Операция #{self.notification_counter} выполнена успешно!",
            f"Предупреждение #{self.notification_counter}",
            f"Ошибка #{self.notification_counter} - что-то пошло не так"
        ]
        
        notification_type = types[self.notification_counter % len(types)]
        message = messages[self.notification_counter % len(messages)]
        
        self.show_notification(message, notification_type)
    
    def show_notification(self, message: str, notification_type: str = "info"):
        """Показать уведомление"""
        show_notification(message, notification_type, 3000, self)
    
    def setup_demo_timer(self):
        """Настройка таймера для демо-эффектов"""
        self.demo_timer = QTimer()
        self.demo_timer.timeout.connect(self.update_demo_stats)
        self.demo_timer.start(2000)  # Обновляем каждые 2 секунды
    
    def update_demo_stats(self):
        """Обновление демо-статистики"""
        # Здесь можно добавить анимированные изменения значений
        pass


def main():
    """Главная функция демо"""
    app = QApplication(sys.argv)
    
    # Настраиваем приложение
    app.setApplicationName("LMU Assistant Theme Demo")
    app.setApplicationVersion("2.0.1")
    
    # Создаем и показываем демо
    demo = ThemeDemo()
    demo.show()
    
    # Запускаем приложение
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
