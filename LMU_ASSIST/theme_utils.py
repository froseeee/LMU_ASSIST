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
                border-color: {stat_
