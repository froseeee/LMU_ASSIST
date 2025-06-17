"""
Современная система тем для LMU Assistant
Полная реализация минималистичного дизайна с поддержкой нескольких тем
"""

from enum import Enum
from typing import Dict, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication


class ThemeType(Enum):
    """Типы доступных тем"""
    DARK = "dark"
    LIGHT = "light"
    AUTO = "auto"
    RACING = "racing"
    MINIMAL = "minimal"


class AnimationType(Enum):
    """Типы анимаций"""
    NONE = "none"
    SUBTLE = "subtle"
    SMOOTH = "smooth"
    DYNAMIC = "dynamic"


class ThemeManager(QObject):
    """Менеджер тем с поддержкой динамического переключения"""
    
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_theme = ThemeType.DARK
        self.animation_level = AnimationType.SMOOTH
        self.custom_fonts_loaded = False
        
    def set_theme(self, theme: ThemeType):
        """Установка темы"""
        if self.current_theme != theme:
            self.current_theme = theme
            self.theme_changed.emit(theme.value)
    
    def load_custom_fonts(self) -> bool:
        """Загрузка кастомных шрифтов"""
        try:
            # Пытаемся загрузить Inter шрифт если доступен
            font_db = QFontDatabase()
            families = font_db.families()
            
            if "Inter" in families:
                self.custom_fonts_loaded = True
                return True
            
            # Fallback на системные шрифты
            return False
            
        except Exception:
            return False


class BaseTheme:
    """Базовый класс для всех тем"""
    
    def __init__(self):
        self.name = "Base"
        self.colors = {}
        self.fonts = {}
        self.animations = {}
        self.effects = {}
    
    def get_color(self, key: str, fallback: str = "#000000") -> str:
        """Получение цвета по ключу"""
        return self.colors.get(key, fallback)
    
    def get_stylesheet(self) -> str:
        """Базовый метод для получения стилей"""
        return ""


class ModernDarkTheme(BaseTheme):
    """Современная темная тема с улучшенным дизайном"""
    
    def __init__(self):
        super().__init__()
        self.name = "Modern Dark"
        self._setup_colors()
        self._setup_fonts()
        self._setup_animations()
        self._setup_effects()
    
    def _setup_colors(self):
        """Настройка цветовой палитры"""
        self.colors = {
            # Основные цвета
            'primary': '#0F172A',           # Slate 900
            'primary_light': '#1E293B',     # Slate 800
            'secondary': '#334155',         # Slate 700
            'tertiary': '#475569',          # Slate 600
            'surface': '#64748B',           # Slate 500
            
            # Фоны
            'background': '#0F172A',
            'background_secondary': '#1E293B',
            'background_tertiary': '#334155',
            'background_elevated': '#1E293B',
            'background_modal': 'rgba(15, 23, 42, 0.95)',
            
            # Акценты
            'accent': '#3B82F6',            # Blue 500
            'accent_light': '#60A5FA',      # Blue 400
            'accent_dark': '#2563EB',       # Blue 600
            'accent_hover': '#1D4ED8',      # Blue 700
            'accent_pressed': '#1E40AF',    # Blue 800
            
            # Статусные цвета
            'success': '#10B981',           # Emerald 500
            'success_light': '#34D399',     # Emerald 400
            'success_dark': '#059669',      # Emerald 600
            'warning': '#F59E0B',           # Amber 500
            'warning_light': '#FBBF24',     # Amber 400
            'warning_dark': '#D97706',      # Amber 600
            'error': '#EF4444',             # Red 500
            'error_light': '#F87171',       # Red 400
            'error_dark': '#DC2626',        # Red 600
            'info': '#06B6D4',              # Cyan 500
            'info_light': '#22D3EE',        # Cyan 400
            'info_dark': '#0891B2',         # Cyan 600
            
            # Текст
            'text_primary': '#F8FAFC',      # Slate 50
            'text_secondary': '#E2E8F0',    # Slate 200
            'text_tertiary': '#CBD5E1',     # Slate 300
            'text_muted': '#94A3B8',        # Slate 400
            'text_disabled': '#64748B',     # Slate 500
            'text_inverse': '#0F172A',      # Slate 900
            
            # Границы и разделители
            'border': '#334155',            # Slate 700
            'border_light': '#475569',      # Slate 600
            'border_focus': '#3B82F6',      # Blue 500
            'border_error': '#EF4444',      # Red 500
            'border_success': '#10B981',    # Emerald 500
            'divider': '#1E293B',           # Slate 800
            
            # Специальные эффекты
            'shadow': 'rgba(0, 0, 0, 0.25)',
            'shadow_light': 'rgba(0, 0, 0, 0.1)',
            'shadow_heavy': 'rgba(0, 0, 0, 0.5)',
            'overlay': 'rgba(0, 0, 0, 0.6)',
            'glass': 'rgba(30, 41, 59, 0.8)',
            'glass_light': 'rgba(30, 41, 59, 0.6)',
            'glow': 'rgba(59, 130, 246, 0.3)',
            'glow_success': 'rgba(16, 185, 129, 0.3)',
            'glow_error': 'rgba(239, 68, 68, 0.3)',
            
            # Градиенты
            'gradient_primary': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3B82F6, stop:1 #1D4ED8)',
            'gradient_success': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10B981, stop:1 #059669)',
            'gradient_warning': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F59E0B, stop:1 #D97706)',
            'gradient_surface': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1E293B, stop:1 #334155)',
        }
    
    def _setup_fonts(self):
        """Настройка шрифтов"""
        self.fonts = {
            'family_primary': "'Inter', 'SF Pro Display', 'Segoe UI', 'Roboto', sans-serif",
            'family_secondary': "'JetBrains Mono', 'SF Mono', 'Consolas', monospace",
            'family_display': "'Inter', 'SF Pro Display', sans-serif",
            
            'size_xs': '11px',
            'size_sm': '13px',
            'size_base': '14px',
            'size_lg': '16px',
            'size_xl': '18px',
            'size_2xl': '20px',
            'size_3xl': '24px',
            'size_4xl': '30px',
            'size_5xl': '36px',
            
            'weight_light': '300',
            'weight_normal': '400',
            'weight_medium': '500',
            'weight_semibold': '600',
            'weight_bold': '700',
            'weight_black': '900',
        }
    
    def _setup_animations(self):
        """Настройка анимаций"""
        self.animations = {
            'duration_fast': '150ms',
            'duration_normal': '250ms',
            'duration_slow': '350ms',
            'duration_slower': '500ms',
            
            'easing_linear': 'linear',
            'easing_ease': 'ease',
            'easing_ease_in': 'ease-in',
            'easing_ease_out': 'ease-out',
            'easing_ease_in_out': 'ease-in-out',
            'easing_bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
            'easing_smooth': 'cubic-bezier(0.4, 0, 0.2, 1)',
        }
    
    def _setup_effects(self):
        """Настройка эффектов"""
        self.effects = {
            'border_radius_sm': '6px',
            'border_radius_md': '8px',
            'border_radius_lg': '12px',
            'border_radius_xl': '16px',
            'border_radius_2xl': '20px',
            'border_radius_full': '50px',
            
            'shadow_sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
            'shadow_md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            'shadow_lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
            'shadow_xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
            'shadow_inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
            
            'blur_sm': 'blur(4px)',
            'blur_md': 'blur(8px)',
            'blur_lg': 'blur(16px)',
        }
    
    def get_application_stylesheet(self) -> str:
        """Основные стили приложения"""
        return f"""
        /* Глобальные стили */
        * {{
            outline: none;
        }}
        
        QApplication {{
            font-family: {self.fonts['family_primary']};
            font-size: {self.fonts['size_base']};
            color: {self.colors['text_primary']};
        }}
        
        /* Главное окно */
        QMainWindow {{
            background: {self.colors['background']};
            color: {self.colors['text_primary']};
        }}
        
        /* Центральный виджет */
        QWidget {{
            background: transparent;
            color: {self.colors['text_primary']};
            border: none;
        }}
        
        /* Статус бар */
        QStatusBar {{
            background: {self.colors['background_secondary']};
            border-top: 1px solid {self.colors['border']};
            color: {self.colors['text_secondary']};
            padding: 8px 16px;
            font-size: {self.fonts['size_sm']};
        }}
        
        QStatusBar::item {{
            border: none;
        }}
        """
    
    def get_tab_stylesheet(self) -> str:
        """Стили для вкладок"""
        return f"""
        /* Система вкладок */
        QTabWidget::pane {{
            background: {self.colors['background']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_lg']};
            margin-top: -1px;
        }}
        
        QTabBar {{
            qproperty-drawBase: 0;
            background: transparent;
            font-weight: {self.fonts['weight_medium']};
        }}
        
        QTabBar::tab {{
            background: {self.colors['background_secondary']};
            color: {self.colors['text_secondary']};
            padding: 14px 24px;
            margin-right: 4px;
            margin-bottom: 4px;
            border-radius: {self.effects['border_radius_lg']};
            font-size: {self.fonts['size_base']};
            font-weight: {self.fonts['weight_medium']};
            min-width: 120px;
            border: 1px solid transparent;
            transition: all {self.animations['duration_normal']} {self.animations['easing_smooth']};
        }}
        
        QTabBar::tab:hover {{
            background: {self.colors['background_tertiary']};
            color: {self.colors['text_primary']};
            transform: translateY(-1px);
            border-color: {self.colors['border_light']};
        }}
        
        QTabBar::tab:selected {{
            background: {self.colors['gradient_primary']};
            color: white;
            font-weight: {self.fonts['weight_semibold']};
            border-color: {self.colors['accent']};
            box-shadow: {self.effects['shadow_md']}, 0 0 20px {self.colors['glow']};
        }}
        
        QTabBar::tab:disabled {{
            background: {self.colors['background_secondary']};
            color: {self.colors['text_disabled']};
        }}
        """
    
    def get_button_stylesheet(self) -> str:
        """Стили для кнопок"""
        return f"""
        /* Основные кнопки */
        QPushButton {{
            background: {self.colors['gradient_primary']};
            color: white;
            border: none;
            border-radius: {self.effects['border_radius_lg']};
            padding: 14px 28px;
            font-weight: {self.fonts['weight_semibold']};
            font-size: {self.fonts['size_base']};
            min-height: 20px;
            transition: all {self.animations['duration_normal']} {self.animations['easing_smooth']};
        }}
        
        QPushButton:hover {{
            background: {self.colors['accent_hover']};
            transform: translateY(-2px);
            box-shadow: {self.effects['shadow_lg']}, 0 0 25px {self.colors['glow']};
        }}
        
        QPushButton:pressed {{
            background: {self.colors['accent_pressed']};
            transform: translateY(0px);
            box-shadow: {self.effects['shadow_md']};
        }}
        
        QPushButton:disabled {{
            background: {self.colors['surface']};
            color: {self.colors['text_disabled']};
            transform: none;
            box-shadow: none;
        }}
        
        /* Вторичные кнопки */
        QPushButton[styleClass="secondary"] {{
            background: {self.colors['background_secondary']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border']};
        }}
        
        QPushButton[styleClass="secondary"]:hover {{
            background: {self.colors['background_tertiary']};
            border-color: {self.colors['border_light']};
            color: {self.colors['text_primary']};
        }}
        
        QPushButton[styleClass="secondary"]:pressed {{
            background: {self.colors['background_tertiary']};
            border-color: {self.colors['accent']};
        }}
        
        /* Кнопки успеха */
        QPushButton[styleClass="success"] {{
            background: {self.colors['gradient_success']};
            color: white;
        }}
        
        QPushButton[styleClass="success"]:hover {{
            background: {self.colors['success_dark']};
            box-shadow: {self.effects['shadow_lg']}, 0 0 25px {self.colors['glow_success']};
        }}
        
        /* Кнопки предупреждения */
        QPushButton[styleClass="warning"] {{
            background: {self.colors['gradient_warning']};
            color: white;
        }}
        
        QPushButton[styleClass="warning"]:hover {{
            background: {self.colors['warning_dark']};
        }}
        
        /* Кнопки ошибки */
        QPushButton[styleClass="danger"] {{
            background: {self.colors['error']};
            color: white;
        }}
        
        QPushButton[styleClass="danger"]:hover {{
            background: {self.colors['error_dark']};
            box-shadow: {self.effects['shadow_lg']}, 0 0 25px {self.colors['glow_error']};
        }}
        
        /* Кнопки-призраки */
        QPushButton[styleClass="ghost"] {{
            background: transparent;
            color: {self.colors['text_secondary']};
            border: none;
            padding: 12px 20px;
        }}
        
        QPushButton[styleClass="ghost"]:hover {{
            background: {self.colors['background_secondary']};
            color: {self.colors['text_primary']};
        }}
        
        /* Кнопки-иконки */
        QPushButton[styleClass="icon"] {{
            background: transparent;
            border: none;
            border-radius: {self.effects['border_radius_md']};
            padding: 8px;
            min-width: 40px;
            min-height: 40px;
            max-width: 40px;
            max-height: 40px;
        }}
        
        QPushButton[styleClass="icon"]:hover {{
            background: {self.colors['background_secondary']};
        }}
        """
    
    def get_input_stylesheet(self) -> str:
        """Стили для полей ввода"""
        return f"""
        /* Поля ввода */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background: {self.colors['background_secondary']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_lg']};
            padding: 14px 16px;
            font-size: {self.fonts['size_base']};
            font-family: {self.fonts['family_primary']};
            selection-background-color: {self.colors['accent']};
            selection-color: white;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {self.colors['border_focus']};
            box-shadow: 0 0 0 3px {self.colors['glow']};
        }}
        
        QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
            background: {self.colors['background_tertiary']};
            color: {self.colors['text_disabled']};
            border-color: {self.colors['border']};
        }}
        
        /* Комбобоксы */
        QComboBox {{
            background: {self.colors['background_secondary']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_lg']};
            padding: 14px 16px;
            min-height: 20px;
            font-size: {self.fonts['size_base']};
            font-family: {self.fonts['family_primary']};
        }}
        
        QComboBox:hover {{
            border-color: {self.colors['border_light']};
        }}
        
        QComboBox:focus {{
            border-color: {self.colors['border_focus']};
            box-shadow: 0 0 0 3px {self.colors['glow']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
            padding-right: 8px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {self.colors['text_secondary']};
            margin-right: 8px;
        }}
        
        QComboBox::down-arrow:hover {{
            border-top-color: {self.colors['text_primary']};
        }}
        
        QComboBox QAbstractItemView {{
            background: {self.colors['background_elevated']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_lg']};
            color: {self.colors['text_primary']};
            selection-background-color: {self.colors['accent']};
            selection-color: white;
            padding: 4px;
            margin: 4px;
            box-shadow: {self.effects['shadow_xl']};
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: 12px 16px;
            border-radius: {self.effects['border_radius_md']};
            margin: 2px;
        }}
        
        QComboBox QAbstractItemView::item:hover {{
            background: {self.colors['background_tertiary']};
        }}
        
        QComboBox QAbstractItemView::item:selected {{
            background: {self.colors['accent']};
            color: white;
        }}
        
        /* Спинбоксы */
        QSpinBox, QDoubleSpinBox {{
            background: {self.colors['background_secondary']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_lg']};
            padding: 14px 16px;
            font-size: {self.fonts['size_base']};
        }}
        
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {self.colors['border_focus']};
            box-shadow: 0 0 0 3px {self.colors['glow']};
        }}
        
        QSpinBox::up-button, QDoubleSpinBox::up-button,
        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            background: {self.colors['background_tertiary']};
            border: none;
            border-radius: {self.effects['border_radius_sm']};
            width: 20px;
            margin: 2px;
        }}
        
        QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
        QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
            background: {self.colors['accent']};
        }}
        """
    
    def get_container_stylesheet(self) -> str:
        """Стили для контейнеров"""
        return f"""
        /* Группы */
        QGroupBox {{
            color: {self.colors['text_primary']};
            font-weight: {self.fonts['weight_semibold']};
            font-size: {self.fonts['size_lg']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_xl']};
            margin-top: 16px;
            padding-top: 20px;
            background: {self.colors['background_secondary']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 20px;
            padding: 0 12px;
            color: {self.colors['accent']};
            background: {self.colors['background']};
            border-radius: {self.effects['border_radius_sm']};
        }}
        
        /* Фреймы */
        QFrame {{
            border: none;
            background: transparent;
        }}
        
        QFrame[frameShape="1"] {{
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_lg']};
            background: {self.colors['background_secondary']};
        }}
        
        QFrame[frameShape="2"] {{
            border: 2px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_xl']};
            background: {self.colors['background_elevated']};
            box-shadow: {self.effects['shadow_lg']};
        }}
        
        /* Сплиттеры */
        QSplitter::handle {{
            background: {self.colors['border']};
            border-radius: 2px;
        }}
        
        QSplitter::handle:horizontal {{
            width: 4px;
            margin: 4px 0;
        }}
        
        QSplitter::handle:vertical {{
            height: 4px;
            margin: 0 4px;
        }}
        
        QSplitter::handle:hover {{
            background: {self.colors['accent']};
        }}
        """
    
    def get_list_stylesheet(self) -> str:
        """Стили для списков и таблиц"""
        return f"""
        /* Списки */
        QListWidget, QTreeWidget {{
            background: {self.colors['background_secondary']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_lg']};
            color: {self.colors['text_primary']};
            outline: none;
            font-size: {self.fonts['size_base']};
            padding: 8px;
        }}
        
        QListWidget::item, QTreeWidget::item {{
            padding: 14px 16px;
            border-radius: {self.effects['border_radius_md']};
            margin: 2px;
            border: 1px solid transparent;
        }}
        
        QListWidget::item:hover, QTreeWidget::item:hover {{
            background: {self.colors['background_tertiary']};
            border-color: {self.colors['border_light']};
        }}
        
        QListWidget::item:selected, QTreeWidget::item:selected {{
            background: {self.colors['accent']};
            color: white;
            border-color: {self.colors['accent_light']};
        }}
        
        QListWidget::item:selected:!active, QTreeWidget::item:selected:!active {{
            background: {self.colors['accent_dark']};
        }}
        
        /* Заголовки деревьев */
        QHeaderView {{
            background: {self.colors['background_tertiary']};
            color: {self.colors['text_primary']};
            border: none;
            border-radius: {self.effects['border_radius_md']};
        }}
        
        QHeaderView::section {{
            background: {self.colors['background_tertiary']};
            color: {self.colors['text_primary']};
            padding: 12px 16px;
            border: none;
            border-right: 1px solid {self.colors['border']};
            font-weight: {self.fonts['weight_semibold']};
            font-size: {self.fonts['size_sm']};
        }}
        
        QHeaderView::section:hover {{
            background: {self.colors['surface']};
        }}
        
        QHeaderView::section:pressed {{
            background: {self.colors['accent']};
            color: white;
        }}
        
        /* Таблицы */
        QTableWidget {{
            background: {self.colors['background_secondary']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_lg']};
            gridline-color: {self.colors['border']};
            color: {self.colors['text_primary']};
            selection-background-color: {self.colors['accent']};
            font-size: {self.fonts['size_base']};
        }}
        
        QTableWidget::item {{
            padding: 12px 16px;
            border: none;
            border-bottom: 1px solid {self.colors['divider']};
        }}
        
        QTableWidget::item:hover {{
            background: {self.colors['background_tertiary']};
        }}
        
        QTableWidget::item:selected {{
            background: {self.colors['accent']};
            color: white;
        }}
        """
    
    def get_slider_stylesheet(self) -> str:
        """Стили для слайдеров и прогресс-баров"""
        return f"""
        /* Горизонтальные слайдеры */
        QSlider::groove:horizontal {{
            background: {self.colors['background_tertiary']};
            height: 8px;
            border-radius: 4px;
            border: 1px solid {self.colors['border']};
        }}
        
        QSlider::handle:horizontal {{
            background: {self.colors['gradient_primary']};
            width: 24px;
            height: 24px;
            border-radius: 12px;
            margin: -8px 0;
            border: 3px solid white;
            box-shadow: {self.effects['shadow_md']};
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {self.colors['accent_hover']};
            box-shadow: {self.effects['shadow_lg']}, 0 0 20px {self.colors['glow']};
            transform: scale(1.1);
        }}
        
        QSlider::handle:horizontal:pressed {{
            background: {self.colors['accent_pressed']};
        }}
        
        QSlider::sub-page:horizontal {{
            background: {self.colors['gradient_primary']};
            border-radius: 4px;
        }}
        
        /* Вертикальные слайдеры */
        QSlider::groove:vertical {{
            background: {self.colors['background_tertiary']};
            width: 8px;
            border-radius: 4px;
            border: 1px solid {self.colors['border']};
        }}
        
        QSlider::handle:vertical {{
            background: {self.colors['gradient_primary']};
            width: 24px;
            height: 24px;
            border-radius: 12px;
            margin: 0 -8px;
            border: 3px solid white;
            box-shadow: {self.effects['shadow_md']};
        }}
        
        QSlider::sub-page:vertical {{
            background: {self.colors['gradient_primary']};
            border-radius: 4px;
        }}
        
        /* Прогресс-бары */
        QProgressBar {{
            background: {self.colors['background_tertiary']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_md']};
            text-align: center;
            color: {self.colors['text_primary']};
            font-weight: {self.fonts['weight_semibold']};
            font-size: {self.fonts['size_sm']};
            min-height: 20px;
        }}
        
        QProgressBar::chunk {{
            background: {self.colors['gradient_primary']};
            border-radius: {self.effects['border_radius_sm']};
            margin: 2px;
        }}
        
        QProgressBar[styleClass="success"]::chunk {{
            background: {self.colors['gradient_success']};
        }}
        
        QProgressBar[styleClass="warning"]::chunk {{
            background: {self.colors['gradient_warning']};
        }}
        
        QProgressBar[styleClass="danger"]::chunk {{
            background: {self.colors['error']};
        }}
        """
    
    def get_checkbox_stylesheet(self) -> str:
        """Стили для чекбоксов и радиокнопок"""
        return f"""
        /* Чекбоксы */
        QCheckBox {{
            color: {self.colors['text_primary']};
            spacing: 12px;
            font-size: {self.fonts['size_base']};
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border-radius: {self.effects['border_radius_sm']};
            border: 2px solid {self.colors['border']};
            background: {self.colors['background_secondary']};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {self.colors['accent']};
            background: {self.colors['background_tertiary']};
        }}
        
        QCheckBox::indicator:checked {{
            background: {self.colors['gradient_primary']};
            border-color: {self.colors['accent']};
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQgTCA0LjUgNy41IEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
        }}
        
        QCheckBox::indicator:checked:hover {{
            background: {self.colors['accent_hover']};
            box-shadow: 0 0 15px {self.colors['glow']};
        }}
        
        QCheckBox::indicator:disabled {{
            background: {self.colors['background_tertiary']};
            border-color: {self.colors['text_disabled']};
        }}
        
        /* Радиокнопки */
        QRadioButton {{
            color: {self.colors['text_primary']};
            spacing: 12px;
            font-size: {self.fonts['size_base']};
        }}
        
        QRadioButton::indicator {{
            width: 20px;
            height: 20px;
            border-radius: 10px;
            border: 2px solid {self.colors['border']};
            background: {self.colors['background_secondary']};
        }}
        
        QRadioButton::indicator:hover {{
            border-color: {self.colors['accent']};
            background: {self.colors['background_tertiary']};
        }}
        
        QRadioButton::indicator:checked {{
            background: {self.colors['gradient_primary']};
            border-color: {self.colors['accent']};
        }}
        
        QRadioButton::indicator:checked:hover {{
            background: {self.colors['accent_hover']};
            box-shadow: 0 0 15px {self.colors['glow']};
        }}
        
        QRadioButton::indicator:checked::after {{
            content: '';
            width: 8px;
            height: 8px;
            border-radius: 4px;
            background: white;
            margin: 4px;
        }}
        """
    
    def get_scrollbar_stylesheet(self) -> str:
        """Стили для скроллбаров"""
        return f"""
        /* Вертикальные скроллбары */
        QScrollBar:vertical {{
            background: {self.colors['background_secondary']};
            width: 12px;
            border-radius: 6px;
            margin: 0;
            border: none;
        }}
        
        QScrollBar::handle:vertical {{
            background: {self.colors['surface']};
            border-radius: 6px;
            min-height: 30px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {self.colors['accent']};
        }}
        
        QScrollBar::handle:vertical:pressed {{
            background: {self.colors['accent_dark']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
            border: none;
        }}
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: transparent;
        }}
        
        /* Горизонтальные скроллбары */
        QScrollBar:horizontal {{
            background: {self.colors['background_secondary']};
            height: 12px;
            border-radius: 6px;
            margin: 0;
            border: none;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {self.colors['surface']};
            border-radius: 6px;
            min-width: 30px;
            margin: 2px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {self.colors['accent']};
        }}
        
        QScrollBar::handle:horizontal:pressed {{
            background: {self.colors['accent_dark']};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
            border: none;
        }}
        
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: transparent;
        }}
        """
    
    def get_menu_stylesheet(self) -> str:
        """Стили для меню"""
        return f"""
        /* Меню бар */
        QMenuBar {{
            background: {self.colors['background_secondary']};
            color: {self.colors['text_primary']};
            border-bottom: 1px solid {self.colors['border']};
            spacing: 4px;
        }}
        
        QMenuBar::item {{
            padding: 12px 16px;
            background: transparent;
            border-radius: {self.effects['border_radius_md']};
        }}
        
        QMenuBar::item:selected {{
            background: {self.colors['background_tertiary']};
        }}
        
        QMenuBar::item:pressed {{
            background: {self.colors['accent']};
            color: white;
        }}
        
        /* Выпадающие меню */
        QMenu {{
            background: {self.colors['background_elevated']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.effects['border_radius_lg']};
            padding: 8px;
            box-shadow: {self.effects['shadow_xl']};
        }}
        
        QMenu::item {{
            padding: 12px 20px;
            border-radius: {self.effects['border_radius_md']};
            margin: 2px;
        }}
        
        QMenu::item:selected {{
            background: {self.colors['accent']};
            color: white;
        }}
        
        QMenu::item:disabled {{
            color: {self.colors['text_disabled']};
        }}
        
        QMenu::separator {{
            height: 1px;
            background: {self.colors['border']};
            margin: 8px 12px;
        }}
        
        QMenu::indicator {{
            width: 16px;
            height: 16px;
            margin-right: 8px;
        }}
        """
    
    def get_tooltip_stylesheet(self) -> str:
        """Стили для подсказок"""
        return f"""
        /* Тултипы */
        QToolTip {{
            background: {self.colors['background_modal']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border_light']};
            border-radius: {self.effects['border_radius_lg']};
            padding: 12px 16px;
            font-size: {self.fonts['size_sm']};
            box-shadow: {self.effects['shadow_xl']};
            backdrop-filter: {self.effects['blur_md']};
        }}
        """
    
    def get_full_stylesheet(self) -> str:
        """Полный стиль темы"""
        return f"""
        {self.get_application_stylesheet()}
        {self.get_tab_stylesheet()}
        {self.get_button_stylesheet()}
        {self.get_input_stylesheet()}
        {self.get_container_stylesheet()}
        {self.get_list_stylesheet()}
        {self.get_slider_stylesheet()}
        {self.get_checkbox_stylesheet()}
        {self.get_scrollbar_stylesheet()}
        {self.get_menu_stylesheet()}
        {self.get_tooltip_stylesheet()}
        """


class ModernLightTheme(ModernDarkTheme):
    """Современная светлая тема"""
    
    def __init__(self):
        super().__init__()
        self.name = "Modern Light"
        self._setup_light_colors()
    
    def _setup_light_colors(self):
        """Настройка светлой палитры"""
        self.colors.update({
            # Основные цвета (инвертированы)
            'primary': '#FFFFFF',
            'primary_light': '#F8FAFC',
            'secondary': '#F1F5F9',
            'tertiary': '#E2E8F0',
            'surface': '#CBD5E1',
            
            # Фоны
            'background': '#FFFFFF',
            'background_secondary': '#F8FAFC',
            'background_tertiary': '#F1F5F9',
            'background_elevated': '#FFFFFF',
            'background_modal': 'rgba(255, 255, 255, 0.95)',
            
            # Текст (инвертирован)
            'text_primary': '#1E293B',
            'text_secondary': '#475569',
            'text_tertiary': '#64748B',
            'text_muted': '#94A3B8',
            'text_disabled': '#CBD5E1',
            'text_inverse': '#FFFFFF',
            
            # Границы
            'border': '#E2E8F0',
            'border_light': '#CBD5E1',
            'divider': '#F1F5F9',
            
            # Эффекты
            'shadow': 'rgba(0, 0, 0, 0.1)',
            'shadow_light': 'rgba(0, 0, 0, 0.05)',
            'shadow_heavy': 'rgba(0, 0, 0, 0.15)',
            'overlay': 'rgba(255, 255, 255, 0.8)',
            'glass': 'rgba(248, 250, 252, 0.8)',
            'glass_light': 'rgba(248, 250, 252, 0.6)',
        })


class RacingTheme(ModernDarkTheme):
    """Гоночная тема с красными акцентами"""
    
    def __init__(self):
        super().__init__()
        self.name = "Racing"
        self._setup_racing_colors()
    
    def _setup_racing_colors(self):
        """Настройка гоночной палитры"""
        self.colors.update({
            # Красные акценты
            'accent': '#DC2626',          # Red 600
            'accent_light': '#EF4444',    # Red 500
            'accent_dark': '#B91C1C',     # Red 700
            'accent_hover': '#991B1B',    # Red 800
            'accent_pressed': '#7F1D1D',  # Red 900
            
            # Гоночные градиенты
            'gradient_primary': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #DC2626, stop:1 #B91C1C)',
            'glow': 'rgba(220, 38, 38, 0.3)',
            
            # Дополнительные цвета
            'warning': '#F59E0B',  # Amber 500 (флаги)
            'success': '#059669',  # Emerald 600 (зеленый флаг)
        })


# Глобальный менеджер тем
theme_manager = ThemeManager()

# Доступные темы
AVAILABLE_THEMES = {
    ThemeType.DARK: ModernDarkTheme,
    ThemeType.LIGHT: ModernLightTheme,
    ThemeType.RACING: RacingTheme,
}

def apply_theme(app: QApplication, theme_type: ThemeType = ThemeType.DARK, enable_effects: bool = True):
    """Применение темы к приложению"""
    try:
        # Создаем экземпляр темы
        theme_class = AVAILABLE_THEMES.get(theme_type, ModernDarkTheme)
        theme = theme_class()
        
        # Применяем стили
        app.setStyleSheet(theme.get_full_stylesheet())
        
        # Настраиваем системную палитру
        palette = QPalette()
        
        # Основные цвета
        palette.setColor(QPalette.Window, QColor(theme.colors['background']))
        palette.setColor(QPalette.WindowText, QColor(theme.colors['text_primary']))
        palette.setColor(QPalette.Base, QColor(theme.colors['background_secondary']))
        palette.setColor(QPalette.AlternateBase, QColor(theme.colors['background_tertiary']))
        palette.setColor(QPalette.ToolTipBase, QColor(theme.colors['background_elevated']))
        palette.setColor(QPalette.ToolTipText, QColor(theme.colors['text_primary']))
        palette.setColor(QPalette.Text, QColor(theme.colors['text_primary']))
        palette.setColor(QPalette.Button, QColor(theme.colors['background_secondary']))
        palette.setColor(QPalette.ButtonText, QColor(theme.colors['text_primary']))
        palette.setColor(QPalette.BrightText, QColor(theme.colors['text_inverse']))
        palette.setColor(QPalette.Link, QColor(theme.colors['accent']))
        palette.setColor(QPalette.Highlight, QColor(theme.colors['accent']))
        palette.setColor(QPalette.HighlightedText, QColor(theme.colors['text_inverse']))
        
        app.setPalette(palette)
        
        # Настраиваем шрифты
        if enable_effects:
            font = QFont(theme.fonts['family_primary'].split(',')[0])
            font.setPointSize(int(theme.fonts['size_base'].replace('px', '')))
            app.setFont(font)
        
        # Обновляем менеджер тем
        theme_manager.set_theme(theme_type)
        
        return True
        
    except Exception as e:
        print(f"Error applying theme: {e}")
        return False

def get_current_theme() -> BaseTheme:
    """Получение текущей темы"""
    theme_class = AVAILABLE_THEMES.get(theme_manager.current_theme, ModernDarkTheme)
    return theme_class()

def set_widget_style_class(widget, style_class: str):
    """Установка класса стиля для виджета"""
    widget.setProperty("styleClass", style_class)
    widget.style().unpolish(widget)
    widget.style().polish(widget)

# Экспорт основных компонентов
__all__ = [
    'ThemeType', 'ThemeManager', 'ModernDarkTheme', 'ModernLightTheme', 'RacingTheme',
    'apply_theme', 'get_current_theme', 'set_widget_style_class', 'theme_manager'
]
