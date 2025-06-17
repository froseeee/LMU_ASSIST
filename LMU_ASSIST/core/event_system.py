from typing import Dict, List, Callable
from PyQt5.QtCore import QObject, pyqtSignal

class EventSystem(QObject):
    """Система событий для связи между компонентами"""
    
    # Сигналы для различных событий
    telemetry_data_received = pyqtSignal(dict)
    lap_completed = pyqtSignal(dict)
    setup_changed = pyqtSignal(dict)
    session_started = pyqtSignal(str)
    session_ended = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.event_handlers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_name: str, handler: Callable):
        """Подписка на событие"""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)
    
    def unsubscribe(self, event_name: str, handler: Callable):
        """Отписка от события"""
        if event_name in self.event_handlers:
            try:
                self.event_handlers[event_name].remove(handler)
            except ValueError:
                pass
    
    def emit_event(self, event_name: str, data=None):
        """Отправка события"""
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Ошибка в обработчике события {event_name}: {e}")
