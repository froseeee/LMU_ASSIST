"""
Утилиты для работы с темами LMU Assistant
Вспомогательные функции и компоненты для UI
"""

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFrame, QLabel, QHBoxLayout, QVBoxLayout,
    QGraphicsDropShadowEffect, QPropertyAnimation, QEasingCurve
)
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QLinearGradient
from theme import get_current_theme, set_widget_style_class


class ModernCard(QFrame):
    """Современная карточка с эффектами"""
    
    clicked = pyqtSignal()
    
    def __init__(self, title: str = "", subtitle: str = "", clickable: bool = False, parent=None):
        super().__init__(parent)
        self.clickable = clickable
        self.hover_animation = None
        self.setup_ui(title, subtitle)
        self.setup_effects()
    
    def setup_ui(self, title: str, subtitle: str):
        """Настройка интерфейса карточки"""
        self.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        
        if title:
            title_label = QLabel(title)
            title_label.setObjectName("cardTitle")
            layout.addWidget(title_label)
        
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setObjectName("cardSubtitle")
            layout.addWidget(subtitle_label)
    
    def setup_effects(self):
        """Настройка эффектов"""
        # Тень
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)
        
        # Стили
        theme = get_current_theme()
        self.setStyleSheet(f"""
            ModernCard {{
                background: {theme.colors['background_secondary']};
                border: 1px solid {theme.colors['border']};
                border-radius: {theme.effects['border_radius_xl']};
                padding: 24px;
            }}
            ModernCard:hover {{
                border-color: {theme.colors['border_light']};
                background: {theme.colors['background_elevated']};
            }}
            QLabel#cardTitle {{
                color: {theme.colors['text_primary']};
                font-size: {theme.fonts['size_xl']};
                font-weight: {theme.fonts['weight_semibold']};
                margin-bottom: 8px;
            }}
            QLabel#cardSubtitle {{
                color: {theme.colors['text_secondary']};
                font-size: {theme.fonts['size_base']};
                line-height: 1.5;
            }}
        """)
    
    def enterEvent(self, event):
        """Анимация при наведении"""
        if self.clickable:
            self.animate_hover(True)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Анимация при убирании курсора"""
        if self.clickable:
            self.animate_hover(False)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Обработка клика"""
        if self.clickable and event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
    
    def animate_hover(self, hover: bool):
        """Анимация наведения"""
        if self.hover_animation:
            self.hover_animation.stop()
        
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        current_geometry = self.geometry()
        if hover:
            # Поднимаем карточку
            new_geometry = QRect(
                current_geometry.x(),
                current_geometry.y() - 2,
                current_geometry.width(),
                current_geometry.height()
            )
        else:
            # Опускаем карточку
            new_geometry = QRect(
                current_geometry.x(),
                current_geometry.y() + 2,
                current_geometry.width(),
                current_geometry.height()
            )
        
        self.hover_animation.setEndValue(new_geometry)
        self.hover_animation.start()


class ModernButton(QPushButton):
    """Современная кнопка с анимациями"""
    
    def __init__(self, text: str = "", style_class: str = "primary", icon=None, parent=None):
        super().__init__(text, parent)
        self.style_class = style_class
        self.press_animation = None
        
        if icon:
            self.setIcon(icon)
        
        self.setup_style()
        set_widget_style_class(self, style_class)
    
    def setup_style(self):
        """Настройка стилей"""
        self.setCursor(Qt.PointingHandCursor)
        
        # Добавляем эффект нажатия
        self.pressed.connect(self.animate_press)
    
    def animate_press(self):
        """Анимация нажатия"""
        if self.press_animation:
            self.press_animation.stop()
        
        # Создаем анимацию масштабирования
        self.press_animation = QPropertyAnimation(self, b"geometry")
        self.press_animation.setDuration(100)
        self.press_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # Уменьшаем размер на 2px
        current = self.geometry()
        pressed = QRect(
            current.x() + 1,
            current.y() + 1,
            current.width() - 2,
            current.height() - 2
        )
        
        self.press_animation.setStartValue(current)
        self.press_animation.setEndValue(pressed)
        self.press_animation.finished.connect(self.animate_release)
        self.press_animation.start()
    
    def animate_release(self):
        """Анимация отпускания"""
        # Возвращаем исходный размер
        release_animation = QPropertyAnimation(self, b"geometry")
        release_animation.setDuration(100)
        release_animation.setEasingCurve(QEasingCurve.OutBounce)
        
        current = self.geometry()
        released = QRect(
            current.x() - 1,
            current.y() - 1,
            current.width() + 2,
            current.height() + 2
        )
        
        release_animation.setStartValue(current)
        release_animation.setEndValue(released)
        release_animation.start()


class LoadingSpinner(QWidget):
    """Спиннер загрузки"""
    
    def __init__(self, size: int = 24, parent=None):
        super().__init__(parent)
        self.size = size
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rotation)
        
        self.setFixedSize(size, size)
        self.setup_style()
    
    def setup_style(self):
        """Настройка стилей"""
        theme = get_current_theme()
        self.primary_color = QColor(theme.colors['accent'])
        self.secondary_color = QColor(theme.colors['border'])
    
    def start(self):
        """Запуск анимации"""
        self.timer.start(16)  # ~60 FPS
    
    def stop(self):
        """Остановка анимации"""
        self.timer.stop()
    
    def update_rotation(self):
        """Обновление поворота"""
        self.angle = (self.angle + 6) % 360
        self.update()
    
    def paintEvent(self, event):
        """Отрисовка спиннера"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Центр
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(center_x, center_y) - 2
        
        # Рисуем круговые сегменты
        pen = QPen()
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap)
        
        for i in range(12):
            angle = (self.angle + i * 30) % 360
            
            # Прозрачность зависит от позиции
            alpha = int(255 * (i / 12))
            color = QColor(self.primary_color)
            color.setAlpha(alpha)
            
            pen.setColor(color)
            painter.setPen(pen)
            
            # Рассчитываем координаты
            start_angle = angle * 16  # Qt использует 1/16 градуса
            span_angle = 20 * 16
            
            painter.drawArc(
                center_x - radius, center_y - radius,
                radius * 2, radius * 2,
                start_angle, span_angle
            )


class ProgressCard(ModernCard):
    """Карточка с прогресс-баром"""
    
    def __init__(self, title: str, progress: float = 0.0, parent=None):
        super().__init__(title, "", parent=parent)
        self.progress_value = progress
        self.setup_progress()
    
    def setup_progress(self):
        """Настройка прогресс-бара"""
        from PyQt5.QtWidgets import QProgressBar
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(int(self.progress_value))
        set_widget_style_class(self.progress_bar, "modern")
        
        self.layout().addWidget(self.progress_bar)
    
    def set_progress(self, value: float):
        """Установка прогресса"""
        self.progress_value = value
        self.progress_bar.setValue(int(value))


class StatCard(ModernCard):
    """Карточка статистики"""
    
    def __init__(self, title: str, value: str, icon: str = "", color: str = None, parent=None):
        super().__init__("", "", parent=parent)
        self.setup_stat_ui(title, value, icon, color)
    
    def setup_stat_ui(self, title: str, value: str, icon: str, color: str):
        """Настройка интерфейса статистики"""
        theme = get_current_theme()
        stat_color = color or theme.colors['accent']
        
        # Очищаем layout
        layout = self.layout()
        
        # Заголовок с иконкой
        header_layout = QHBoxLayout()
        
        if icon:
            icon_label = QLabel(icon)
            icon_label.setObjectName("statIcon")
            header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Значение
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        layout.addWidget(value_label)
        
        # Заголовок
        title_label = QLabel(title)
        title_label.setObjectName("statTitle")
        layout.addWidget(title_label)
        
        # Стили
        self.setStyleSheet(f"""
            StatCard {{
                background: {theme.colors['background_secondary']};
                border: 1px solid {stat_color}40;
                border-radius: {theme.effects['border_radius_xl']};
            }}
            StatCard:hover {{
                border-color: {stat_color}80;
                background: {theme.colors['background_elevated']};
            }}
            QLabel#statIcon {{
                color: {stat_color};
                font-size: {theme.fonts['size_3xl']};
                font-weight: {theme.fonts['weight_bold']};
            }}
            QLabel#statValue {{
                color: {stat_color};
                font-size: {theme.fonts['size_4xl']};
                font-weight: {theme.fonts['weight_black']};
                margin: 8px 0;
            }}
            QLabel#statTitle {{
                color: {theme.colors['text_muted']};
                font-size: {theme.fonts['size_sm']};
                font-weight: {theme.fonts['weight_medium']};
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
        """)


class NotificationToast(QWidget):
    """Уведомление-тост"""
    
    def __init__(self, message: str, notification_type: str = "info", duration: int = 3000, parent=None):
        super().__init__(parent)
        self.notification_type = notification_type
        self.duration = duration
        self.setup_ui(message)
        self.setup_animations()
    
    def setup_ui(self, message: str):
        """Настройка интерфейса"""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # Иконка
        icon_map = {
            "success": "✅",
            "error": "❌", 
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        icon_label = QLabel(icon_map.get(self.notification_type, "ℹ️"))
        icon_label.setObjectName("toastIcon")
        layout.addWidget(icon_label)
        
        # Сообщение
        message_label = QLabel(message)
        message_label.setObjectName("toastMessage")
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        # Кнопка закрытия
        close_btn = QPushButton("×")
        close_btn.setObjectName("toastClose")
        close_btn.clicked.connect(self.hide_toast)
        layout.addWidget(close_btn)
        
        self.setup_style()
    
    def setup_style(self):
        """Настройка стилей"""
        theme = get_current_theme()
        
        # Цвета по типу уведомления
        color_map = {
            "success": theme.colors['success'],
            "error": theme.colors['error'],
            "warning": theme.colors['warning'],
            "info": theme.colors['info']
        }
        
        accent_color = color_map.get(self.notification_type, theme.colors['info'])
        
        self.setStyleSheet(f"""
            NotificationToast {{
                background: {theme.colors['background_modal']};
                border: 1px solid {accent_color};
                border-radius: {theme.effects['border_radius_lg']};
                box-shadow: {theme.effects['shadow_xl']};
            }}
            QLabel#toastIcon {{
                font-size: {theme.fonts['size_xl']};
                color: {accent_color};
            }}
            QLabel#toastMessage {{
                color: {theme.colors['text_primary']};
                font-size: {theme.fonts['size_base']};
                font-weight: {theme.fonts['weight_medium']};
            }}
            QPushButton#toastClose {{
                background: transparent;
                border: none;
                color: {theme.colors['text_muted']};
                font-size: {theme.fonts['size_xl']};
                font-weight: {theme.fonts['weight_bold']};
                width: 24px;
                height: 24px;
                border-radius: 12px;
            }}
            QPushButton#toastClose:hover {{
                background: {theme.colors['background_tertiary']};
                color: {theme.colors['text_primary']};
            }}
        """)
    
    def setup_animations(self):
        """Настройка анимаций"""
        # Анимация появления
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.OutCubic)
        
        # Анимация исчезновения
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.InCubic)
        self.fade_out.finished.connect(self.close)
        
        # Таймер автоскрытия
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.setSingleShot(True)
        self.auto_hide_timer.timeout.connect(self.hide_toast)
    
    def show_toast(self, parent_widget=None):
        """Показать уведомление"""
        if parent_widget:
            # Позиционируем относительно родительского виджета
            parent_rect = parent_widget.geometry()
            self.move(
                parent_rect.right() - self.width() - 20,
                parent_rect.top() + 20
            )
        
        self.show()
        self.fade_in.start()
        
        if self.duration > 0:
            self.auto_hide_timer.start(self.duration)
    
    def hide_toast(self):
        """Скрыть уведомление"""
        self.auto_hide_timer.stop()
        self.fade_out.start()


class GlassPanel(QFrame):
    """Панель с эффектом стекла"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
    
    def setup_style(self):
        """Настройка стеклянного эффекта"""
        theme = get_current_theme()
        
        self.setStyleSheet(f"""
            GlassPanel {{
                background: {theme.colors['glass']};
                border: 1px solid {theme.colors['border_light']};
                border-radius: {theme.effects['border_radius_xl']};
                backdrop-filter: {theme.effects['blur_md']};
            }}
        """)
        
        # Добавляем тень
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)


class ModernSlider(QWidget):
    """Современный слайдер с индикатором значения"""
    
    valueChanged = pyqtSignal(int)
    
    def __init__(self, label: str = "", min_val: int = 0, max_val: int = 100, 
                 value: int = 50, suffix: str = "", parent=None):
        super().__init__(parent)
        self.suffix = suffix
        self.setup_ui(label, min_val, max_val, value)
    
    def setup_ui(self, label: str, min_val: int, max_val: int, value: int):
        """Настройка интерфейса"""
        from PyQt5.QtWidgets import QSlider
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Заголовок с значением
        header_layout = QHBoxLayout()
        
        if label:
            label_widget = QLabel(label)
            label_widget.setObjectName("sliderLabel")
            header_layout.addWidget(label_widget)
        
        header_layout.addStretch()
        
        self.value_label = QLabel(f"{value}{self.suffix}")
        self.value_label.setObjectName("sliderValue")
        header_layout.addWidget(self.value_label)
        
        layout.addLayout(header_layout)
        
        # Слайдер
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(self.on_value_changed)
        
        layout.addWidget(self.slider)
        
        self.setup_style()
    
    def setup_style(self):
        """Настройка стилей"""
        theme = get_current_theme()
        
        self.setStyleSheet(f"""
            QLabel#sliderLabel {{
                color: {theme.colors['text_secondary']};
                font-size: {theme.fonts['size_base']};
                font-weight: {theme.fonts['weight_medium']};
            }}
            QLabel#sliderValue {{
                color: {theme.colors['accent']};
                font-size: {theme.fonts['size_lg']};
                font-weight: {theme.fonts['weight_semibold']};
                background: {theme.colors['background_secondary']};
                border-radius: {theme.effects['border_radius_sm']};
                padding: 6px 12px;
                border: 1px solid {theme.colors['border']};
            }}
        """)
    
    def on_value_changed(self, value: int):
        """Обработка изменения значения"""
        self.value_label.setText(f"{value}{self.suffix}")
        self.valueChanged.emit(value)
    
    def value(self) -> int:
        """Получить значение"""
        return self.slider.value()
    
    def setValue(self, value: int):
        """Установить значение"""
        self.slider.setValue(value)


class IconButton(QPushButton):
    """Кнопка только с иконкой"""
    
    def __init__(self, icon_text: str = "", size: int = 32, parent=None):
        super().__init__(parent)
        self.icon_text = icon_text
        self.button_size = size
        self.setup_style()
    
    def setup_style(self):
        """Настройка стилей"""
        theme = get_current_theme()
        
        self.setText(self.icon_text)
        self.setFixedSize(self.button_size, self.button_size)
        self.setCursor(Qt.PointingHandCursor)
        
        self.setStyleSheet(f"""
            IconButton {{
                background: transparent;
                border: none;
                border-radius: {self.button_size // 2}px;
                color: {theme.colors['text_secondary']};
                font-size: {self.button_size // 2}px;
                font-weight: {theme.fonts['weight_bold']};
            }}
            IconButton:hover {{
                background: {theme.colors['background_secondary']};
                color: {theme.colors['text_primary']};
            }}
            IconButton:pressed {{
                background: {theme.colors['accent']};
                color: white;
            }}
        """)


class ModernDialog(QWidget):
    """Современный диалог"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setup_ui(title)
        self.setup_animations()
    
    def setup_ui(self, title: str):
        """Настройка интерфейса"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Основная панель
        self.main_panel = GlassPanel()
        panel_layout = QVBoxLayout(self.main_panel)
        panel_layout.setContentsMargins(32, 32, 32, 32)
        panel_layout.setSpacing(24)
        
        # Заголовок
        if title:
            header_layout = QHBoxLayout()
            
            title_label = QLabel(title)
            title_label.setObjectName("dialogTitle")
            header_layout.addWidget(title_label)
            
            header_layout.addStretch()
            
            close_btn = IconButton("×", 32)
            close_btn.clicked.connect(self.close)
            header_layout.addWidget(close_btn)
            
            panel_layout.addLayout(header_layout)
        
        # Контент (должен быть переопределен в наследниках)
        self.content_layout = QVBoxLayout()
        panel_layout.addLayout(self.content_layout)
        
        main_layout.addWidget(self.main_panel)
        
        self.setup_style()
    
    def setup_style(self):
        """Настройка стилей"""
        theme = get_current_theme()
        
        self.setStyleSheet(f"""
            QLabel#dialogTitle {{
                color: {theme.colors['text_primary']};
                font-size: {theme.fonts['size_2xl']};
                font-weight: {theme.fonts['weight_semibold']};
            }}
        """)
    
    def setup_animations(self):
        """Настройка анимаций"""
        # Анимация появления
        self.scale_in = QPropertyAnimation(self.main_panel, b"geometry")
        self.scale_in.setDuration(300)
        self.scale_in.setEasingCurve(QEasingCurve.OutBack)
        
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
    
    def showEvent(self, event):
        """Событие показа"""
        super().showEvent(event)
        
        # Центрируем диалог
        if self.parent():
            parent_rect = self.parent().geometry()
            self.move(
                parent_rect.center().x() - self.width() // 2,
                parent_rect.center().y() - self.height() // 2
            )
        
        # Запускаем анимации
        self.fade_in.start()


# Вспомогательные функции

def show_notification(message: str, notification_type: str = "info", 
                     duration: int = 3000, parent=None):
    """Показать уведомление"""
    toast = NotificationToast(message, notification_type, duration, parent)
    toast.show_toast(parent)
    return toast

def create_separator(orientation: str = "horizontal") -> QFrame:
    """Создать разделитель"""
    separator = QFrame()
    theme = get_current_theme()
    
    if orientation == "horizontal":
        separator.setFrameShape(QFrame.HLine)
        separator.setFixedHeight(1)
    else:
        separator.setFrameShape(QFrame.VLine)
        separator.setFixedWidth(1)
    
    separator.setStyleSheet(f"""
        QFrame {{
            background: {theme.colors['divider']};
            border: none;
        }}
    """)
    
    return separator

def apply_glow_effect(widget: QWidget, color: str = None, blur: int = 20):
    """Применить эффект свечения"""
    theme = get_current_theme()
    glow_color = color or theme.colors['accent']
    
    glow = QGraphicsDropShadowEffect()
    glow.setBlurRadius(blur)
    glow.setXOffset(0)
    glow.setYOffset(0)
    glow.setColor(QColor(glow_color))
    
    widget.setGraphicsEffect(glow)

def set_loading_state(widget: QWidget, loading: bool = True):
    """Установить состояние загрузки для виджета"""
    if loading:
        widget.setEnabled(False)
        # Добавляем спиннер (если нужно)
        if not hasattr(widget, '_loading_spinner'):
            widget._loading_spinner = LoadingSpinner(parent=widget)
            widget._loading_spinner.move(
                widget.width() // 2 - 12,
                widget.height() // 2 - 12
            )
        widget._loading_spinner.show()
        widget._loading_spinner.start()
    else:
        widget.setEnabled(True)
        if hasattr(widget, '_loading_spinner'):
            widget._loading_spinner.stop()
            widget._loading_spinner.hide()

# Экспорт компонентов
__all__ = [
    'ModernCard', 'ModernButton', 'LoadingSpinner', 'ProgressCard', 'StatCard',
    'NotificationToast', 'GlassPanel', 'ModernSlider', 'IconButton', 'ModernDialog',
    'show_notification', 'create_separator', 'apply_glow_effect', 'set_loading_state'
]
