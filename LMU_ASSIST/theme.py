"""
Современная темная тема для LMU Assistant
Минималистичный дизайн в темных тонах
"""

class ModernDarkTheme:
    """Современная темная тема с минималистичным дизайном"""
    
    # Основная палитра цветов
    COLORS = {
        # Базовые цвета
        'primary': '#0F172A',      # Основной темный цвет
        'secondary': '#1E293B',    # Вторичный фон
        'tertiary': '#334155',     # Третичный элемент
        'surface': '#475569',      # Поверхности
        
        # Акцентные цвета
        'accent': '#3B82F6',       # Синий акцент
        'accent_hover': '#2563EB', # Акцент при наведении
        'accent_pressed': '#1D4ED8', # Акцент при нажатии
        
        # Статусные цвета
        'success': '#10B981',      # Зеленый - успех
        'warning': '#F59E0B',      # Желтый - предупреждение
        'error': '#EF4444',        # Красный - ошибка
        'info': '#06B6D4',         # Голубой - информация
        
        # Текст
        'text_primary': '#F8FAFC',   # Основной текст
        'text_secondary': '#CBD5E1',  # Вторичный текст
        'text_muted': '#94A3B8',     # Приглушенный текст
        'text_disabled': '#64748B',   # Отключенный текст
        
        # Границы и разделители
        'border': '#334155',         # Основные границы
        'border_light': '#475569',   # Светлые границы
        'divider': '#1E293B',        # Разделители
        
        # Специальные
        'transparent': 'transparent',
        'overlay': 'rgba(0, 0, 0, 0.5)',
        'glass': 'rgba(30, 41, 59, 0.8)',
    }
    
    # Размеры и отступы
    SPACING = {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        'xxl': '48px',
    }
    
    # Радиусы скругления
    RADIUS = {
        'none': '0',
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        'full': '50px',
    }
    
    # Тени
    SHADOWS = {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'glow': '0 0 20px rgba(59, 130, 246, 0.3)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    }
    
    # Шрифты
    FONTS = {
        'family': "'Inter', 'Segoe UI', 'Roboto', sans-serif",
        'mono': "'JetBrains Mono', 'Consolas', monospace",
        'sizes': {
            'xs': '12px',
            'sm': '14px',
            'md': '16px',
            'lg': '18px',
            'xl': '20px',
            'xxl': '24px',
            'title': '32px',
        },
        'weights': {
            'normal': '400',
            'medium': '500',
            'semibold': '600',
            'bold': '700',
        }
    }
    
    # Анимации
    TRANSITIONS = {
        'fast': '150ms ease',
        'normal': '250ms ease',
        'slow': '350ms ease',
        'bounce': '300ms cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    }

    @classmethod
    def get_main_stylesheet(cls) -> str:
        """Основной стиль приложения"""
        c = cls.COLORS
        s = cls.SPACING
        r = cls.RADIUS
        f = cls.FONTS
        
        return f"""
        /* Основное окно приложения */
        QMainWindow {{
            background: {c['primary']};
            color: {c['text_primary']};
            font-family: {f['family']};
            font-size: {f['sizes']['md']};
        }}
        
        /* Центральный виджет */
        QWidget {{
            background: {c['primary']};
            color: {c['text_primary']};
            border: none;
            outline: none;
        }}
        
        /* Статус бар */
        QStatusBar {{
            background: {c['secondary']};
            border-top: 1px solid {c['border']};
            color: {c['text_secondary']};
            padding: {s['sm']};
            font-size: {f['sizes']['sm']};
        }}
        
        /* Основные вкладки */
        QTabWidget::pane {{
            background: {c['primary']};
            border: 1px solid {c['border']};
            border-radius: {r['lg']};
            margin-top: -1px;
        }}
        
        QTabBar {{
            qproperty-drawBase: 0;
            background: transparent;
        }}
        
        QTabBar::tab {{
            background: {c['secondary']};
            color: {c['text_secondary']};
            padding: {s['md']} {s['lg']};
            margin-right: {s['xs']};
            border-radius: {r['md']};
            font-weight: {f['weights']['medium']};
            min-width: 120px;
            transition: all {cls.TRANSITIONS['normal']};
        }}
        
        QTabBar::tab:hover {{
            background: {c['tertiary']};
            color: {c['text_primary']};
            transform: translateY(-2px);
        }}
        
        QTabBar::tab:selected {{
            background: {c['accent']};
            color: white;
            font-weight: {f['weights']['semibold']};
        }}
        """

    @classmethod
    def get_button_stylesheet(cls) -> str:
        """Стили для кнопок"""
        c = cls.COLORS
        s = cls.SPACING
        r = cls.RADIUS
        f = cls.FONTS
        
        return f"""
        /* Основные кнопки */
        QPushButton {{
            background: {c['accent']};
            color: white;
            border: none;
            border-radius: {r['md']};
            padding: {s['md']} {s['lg']};
            font-weight: {f['weights']['medium']};
            font-size: {f['sizes']['md']};
            min-height: 40px;
            transition: all {cls.TRANSITIONS['normal']};
        }}
        
        QPushButton:hover {{
            background: {c['accent_hover']};
            transform: translateY(-1px);
            box-shadow: {cls.SHADOWS['md']};
        }}
        
        QPushButton:pressed {{
            background: {c['accent_pressed']};
            transform: translateY(0px);
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        QPushButton:disabled {{
            background: {c['surface']};
            color: {c['text_disabled']};
        }}
        
        /* Вторичные кнопки */
        QPushButton[class="secondary"] {{
            background: {c['secondary']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
        }}
        
        QPushButton[class="secondary"]:hover {{
            background: {c['tertiary']};
            border-color: {c['border_light']};
        }}
        
        /* Кнопки-иконки */
        QPushButton[class="icon"] {{
            background: transparent;
            border: none;
            border-radius: {r['sm']};
            padding: {s['sm']};
            min-width: 36px;
            min-height: 36px;
        }}
        
        QPushButton[class="icon"]:hover {{
            background: {c['tertiary']};
        }}
        """

    @classmethod
    def get_input_stylesheet(cls) -> str:
        """Стили для полей ввода"""
        c = cls.COLORS
        s = cls.SPACING
        r = cls.RADIUS
        f = cls.FONTS
        
        return f"""
        /* Поля ввода */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background: {c['secondary']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            padding: {s['md']};
            font-size: {f['sizes']['md']};
            selection-background-color: {c['accent']};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {c['accent']};
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }}
        
        /* Комбобоксы */
        QComboBox {{
            background: {c['secondary']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            padding: {s['md']};
            min-height: 36px;
            font-size: {f['sizes']['md']};
        }}
        
        QComboBox:hover {{
            border-color: {c['border_light']};
        }}
        
        QComboBox:focus {{
            border-color: {c['accent']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {c['text_secondary']};
            margin-right: {s['sm']};
        }}
        
        QComboBox QAbstractItemView {{
            background: {c['secondary']};
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            color: {c['text_primary']};
            selection-background-color: {c['accent']};
            selection-color: white;
            padding: {s['xs']};
        }}
        """

    @classmethod
    def get_card_stylesheet(cls) -> str:
        """Стили для карточек"""
        c = cls.COLORS
        s = cls.SPACING
        r = cls.RADIUS
        
        return f"""
        /* Карточки */
        QFrame[class="card"] {{
            background: {c['secondary']};
            border: 1px solid {c['border']};
            border-radius: {r['lg']};
            padding: {s['lg']};
            margin: {s['sm']};
        }}
        
        QFrame[class="card"]:hover {{
            border-color: {c['border_light']};
            box-shadow: {cls.SHADOWS['md']};
        }}
        
        /* Glassmorphism карточки */
        QFrame[class="glass-card"] {{
            background: {c['glass']};
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: {r['lg']};
            padding: {s['lg']};
            backdrop-filter: blur(10px);
        }}
        
        /* Группы */
        QGroupBox {{
            color: {c['text_primary']};
            font-weight: {cls.FONTS['weights']['semibold']};
            font-size: {cls.FONTS['sizes']['lg']};
            border: 1px solid {c['border']};
            border-radius: {r['lg']};
            margin-top: {s['md']};
            padding-top: {s['lg']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {s['md']};
            padding: 0 {s['sm']};
            color: {c['accent']};
            background: {c['primary']};
        }}
        """

    @classmethod
    def get_list_stylesheet(cls) -> str:
        """Стили для списков"""
        c = cls.COLORS
        s = cls.SPACING
        r = cls.RADIUS
        f = cls.FONTS
        
        return f"""
        /* Списки */
        QListWidget, QTreeWidget {{
            background: {c['secondary']};
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            color: {c['text_primary']};
            outline: none;
            font-size: {f['sizes']['md']};
        }}
        
        QListWidget::item, QTreeWidget::item {{
            padding: {s['md']};
            border-bottom: 1px solid {c['divider']};
            border-radius: {r['sm']};
            margin: 2px;
        }}
        
        QListWidget::item:hover, QTreeWidget::item:hover {{
            background: {c['tertiary']};
        }}
        
        QListWidget::item:selected, QTreeWidget::item:selected {{
            background: {c['accent']};
            color: white;
        }}
        
        /* Таблицы */
        QTableWidget {{
            background: {c['secondary']};
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            gridline-color: {c['divider']};
            color: {c['text_primary']};
        }}
        
        QTableWidget::item {{
            padding: {s['md']};
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background: {c['accent']};
            color: white;
        }}
        
        QHeaderView::section {{
            background: {c['tertiary']};
            color: {c['text_primary']};
            padding: {s['md']};
            border: none;
            border-right: 1px solid {c['border']};
            font-weight: {f['weights']['semibold']};
        }}
        """

    @classmethod
    def get_slider_stylesheet(cls) -> str:
        """Стили для слайдеров"""
        c = cls.COLORS
        s = cls.SPACING
        r = cls.RADIUS
        
        return f"""
        /* Слайдеры */
        QSlider::groove:horizontal {{
            background: {c['tertiary']};
            height: 6px;
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background: {c['accent']};
            width: 20px;
            height: 20px;
            border-radius: 10px;
            margin: -7px 0;
            border: 2px solid white;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {c['accent_hover']};
            box-shadow: {cls.SHADOWS['glow']};
        }}
        
        QSlider::sub-page:horizontal {{
            background: {c['accent']};
            border-radius: 3px;
        }}
        
        /* Прогресс бары */
        QProgressBar {{
            background: {c['tertiary']};
            border: none;
            border-radius: {r['sm']};
            text-align: center;
            color: {c['text_primary']};
            font-weight: {cls.FONTS['weights']['medium']};
        }}
        
        QProgressBar::chunk {{
            background: {c['accent']};
            border-radius: {r['sm']};
        }}
        """

    @classmethod
    def get_scrollbar_stylesheet(cls) -> str:
        """Стили для скроллбаров"""
        c = cls.COLORS
        r = cls.RADIUS
        
        return f"""
        /* Скроллбары */
        QScrollBar:vertical {{
            background: {c['secondary']};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background: {c['surface']};
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {c['accent']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        
        QScrollBar:horizontal {{
            background: {c['secondary']};
            height: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {c['surface']};
            border-radius: 6px;
            min-width: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {c['accent']};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}
        """

    @classmethod
    def get_full_stylesheet(cls) -> str:
        """Полный стиль приложения"""
        return f"""
        {cls.get_main_stylesheet()}
        {cls.get_button_stylesheet()}
        {cls.get_input_stylesheet()}
        {cls.get_card_stylesheet()}
        {cls.get_list_stylesheet()}
        {cls.get_slider_stylesheet()}
        {cls.get_scrollbar_stylesheet()}
        
        /* Дополнительные элементы */
        QCheckBox {{
            color: {cls.COLORS['text_primary']};
            spacing: {cls.SPACING['sm']};
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: {cls.RADIUS['sm']};
            border: 2px solid {cls.COLORS['border']};
            background: {cls.COLORS['secondary']};
        }}
        
        QCheckBox::indicator:checked {{
            background: {cls.COLORS['accent']};
            border-color: {cls.COLORS['accent']};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {cls.COLORS['accent']};
        }}
        
        QRadioButton {{
            color: {cls.COLORS['text_primary']};
            spacing: {cls.SPACING['sm']};
        }}
        
        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 9px;
            border: 2px solid {cls.COLORS['border']};
            background: {cls.COLORS['secondary']};
        }}
        
        QRadioButton::indicator:checked {{
            background: {cls.COLORS['accent']};
            border-color: {cls.COLORS['accent']};
        }}
        
        /* Сплиттеры */
        QSplitter::handle {{
            background: {cls.COLORS['border']};
        }}
        
        QSplitter::handle:horizontal {{
            width: 2px;
        }}
        
        QSplitter::handle:vertical {{
            height: 2px;
        }}
        
        /* Тултипы */
        QToolTip {{
            background: {cls.COLORS['tertiary']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['sm']};
            font-size: {cls.FONTS['sizes']['sm']};
        }}
        
        /* Меню */
        QMenuBar {{
            background: {cls.COLORS['secondary']};
            color: {cls.COLORS['text_primary']};
            border-bottom: 1px solid {cls.COLORS['border']};
        }}
        
        QMenuBar::item {{
            padding: {cls.SPACING['sm']} {cls.SPACING['md']};
            background: transparent;
            border-radius: {cls.RADIUS['sm']};
        }}
        
        QMenuBar::item:selected {{
            background: {cls.COLORS['tertiary']};
        }}
        
        QMenu {{
            background: {cls.COLORS['secondary']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['xs']};
        }}
        
        QMenu::item {{
            padding: {cls.SPACING['sm']} {cls.SPACING['md']};
            border-radius: {cls.RADIUS['sm']};
        }}
        
        QMenu::item:selected {{
            background: {cls.COLORS['accent']};
            color: white;
        }}
        """

    @classmethod
    def apply_modern_style(cls, app):
        """Применить современную тему к приложению"""
        app.setStyleSheet(cls.get_full_stylesheet())
        
        # Устанавливаем палитру для системных элементов
        from PyQt5.QtGui import QPalette, QColor
        from PyQt5.QtCore import Qt
        
        palette = QPalette()
        
        # Основные цвета
        palette.setColor(QPalette.Window, QColor(cls.COLORS['primary']))
        palette.setColor(QPalette.WindowText, QColor(cls.COLORS['text_primary']))
        palette.setColor(QPalette.Base, QColor(cls.COLORS['secondary']))
        palette.setColor(QPalette.AlternateBase, QColor(cls.COLORS['tertiary']))
        palette.setColor(QPalette.ToolTipBase, QColor(cls.COLORS['tertiary']))
        palette.setColor(QPalette.ToolTipText, QColor(cls.COLORS['text_primary']))
        palette.setColor(QPalette.Text, QColor(cls.COLORS['text_primary']))
        palette.setColor(QPalette.Button, QColor(cls.COLORS['secondary']))
        palette.setColor(QPalette.ButtonText, QColor(cls.COLORS['text_primary']))
        palette.setColor(QPalette.BrightText, QColor(cls.COLORS['error']))
        palette.setColor(QPalette.Link, QColor(cls.COLORS['accent']))
        palette.setColor(QPalette.Highlight, QColor(cls.COLORS['accent']))
        palette.setColor(QPalette.HighlightedText, QColor('white'))
        
        app.setPalette(palette)
