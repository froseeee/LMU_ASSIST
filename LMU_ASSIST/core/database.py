import sqlite3
import json
import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    """Улучшенный менеджер базы данных"""
    
    def __init__(self, db_name="lmu_data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Создание таблиц базы данных"""
        cursor = self.conn.cursor()
        
        # Таблица сессий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                track TEXT NOT NULL,
                car TEXT NOT NULL,
                session_type TEXT NOT NULL,
                weather TEXT,
                temperature REAL,
                data TEXT NOT NULL,
                lap_time REAL,
                best_lap REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица кругов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS laps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                lap_number INTEGER,
                lap_time REAL,
                sector_times TEXT,
                telemetry_data TEXT,
                is_valid BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        # Таблица настроек автомобиля
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS car_setups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car TEXT NOT NULL,
                track TEXT NOT NULL,
                setup_name TEXT NOT NULL,
                setup_data TEXT NOT NULL,
                notes TEXT,
                rating INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица анализа производительности
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                analysis_type TEXT,
                metrics TEXT,
                recommendations TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        self.conn.commit()

    def save_session(self, track: str, car: str, session_type: str, 
                    data: dict, weather: str = None, temperature: float = None) -> int:
        """Сохранение сессии"""
        cursor = self.conn.cursor()
        timestamp = datetime.datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO sessions (timestamp, track, car, session_type, weather, temperature, data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, track, car, session_type, weather, temperature, json.dumps(data)))
        
        session_id = cursor.lastrowid
        self.conn.commit()
        return session_id

    def save_lap(self, session_id: int, lap_number: int, lap_time: float,
                sector_times: List[float], telemetry_data: dict, is_valid: bool = True):
        """Сохранение круга"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO laps (session_id, lap_number, lap_time, sector_times, telemetry_data, is_valid)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session_id, lap_number, lap_time, json.dumps(sector_times), 
              json.dumps(telemetry_data), is_valid))
        
        self.conn.commit()

    def save_car_setup(self, car: str, track: str, setup_name: str, 
                      setup_data: dict, notes: str = "", rating: int = 0):
        """Сохранение настройки автомобиля"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO car_setups (car, track, setup_name, setup_data, notes, rating)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (car, track, setup_name, json.dumps(setup_data), notes, rating))
        
        self.conn.commit()

    def get_sessions(self, track: str = None, car: str = None, limit: int = 50) -> List[Dict]:
        """Получение сессий с фильтрацией"""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM sessions"
        params = []
        
        conditions = []
        if track:
            conditions.append("track = ?")
            params.append(track)
        if car:
            conditions.append("car = ?")
            params.append(car)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_best_laps(self, track: str = None, car: str = None, limit: int = 10) -> List[Dict]:
        """Получение лучших кругов"""
        cursor = self.conn.cursor()
        
        query = """
            SELECT l.*, s.track, s.car 
            FROM laps l
            JOIN sessions s ON l.session_id = s.id
            WHERE l.is_valid = 1
        """
        params = []
        
        if track:
            query += " AND s.track = ?"
            params.append(track)
        if car:
            query += " AND s.car = ?"
            params.append(car)
            
        query += " ORDER BY l.lap_time ASC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_car_setups(self, car: str = None, track: str = None) -> List[Dict]:
        """Получение настроек автомобиля"""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM car_setups"
        params = []
        
        conditions = []
        if car:
            conditions.append("car = ?")
            params.append(car)
        if track:
            conditions.append("track = ?")
            params.append(track)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY rating DESC, created_at DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.conn:
            self.conn.close()
