import sqlite3
import json
import datetime
import logging
import threading
from typing import List, Dict, Optional, Any
from pathlib import Path
from contextlib import contextmanager

from .constants import ErrorMessages


class DatabaseError(Exception):
    """Базовая ошибка базы данных"""
    pass


class DatabaseConnectionError(DatabaseError):
    """Ошибка подключения к базе данных"""
    pass


class DatabaseQueryError(DatabaseError):
    """Ошибка выполнения запроса"""
    pass


class DatabaseManager:
    """Улучшенный менеджер базы данных с proper resource management"""
    
    def __init__(self, db_name=None):
        self.logger = logging.getLogger(__name__)  # Инициализируем логгер ПЕРВЫМ
        self.db_name = db_name or "lmu_data.db"  # Используем строку напрямую для избежания circular import
        self.db_path = Path(self.db_name)
        self._conn = None
        self._lock = threading.RLock()
        
        # Создаем директорию если нужно
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Инициализируем базу данных
        try:
            self._initialize_database()
            self.logger.info(f"Database initialized: {self.db_name}")
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise DatabaseConnectionError(f"Failed to initialize database: {e}")

    @property
    def connection(self) -> sqlite3.Connection:
        """Получение соединения с базой данных (thread-safe)"""
        with self._lock:
            if self._conn is None or self._is_connection_closed():
                self._create_connection()
            return self._conn

    def _is_connection_closed(self) -> bool:
        """Проверка состояния соединения"""
        try:
            self._conn.execute("SELECT 1")
            return False
        except (sqlite3.ProgrammingError, AttributeError):
            return True

    def _create_connection(self):
        """Создание нового соединения"""
        try:
            self._conn = sqlite3.connect(
                self.db_name,
                check_same_thread=False,
                timeout=DatabaseConstants.DB_CONNECTION_TIMEOUT
            )
            self._conn.row_factory = sqlite3.Row
            # Включаем WAL режим для лучшей производительности
            self._conn.execute("PRAGMA journal_mode=WAL")
            # Включаем foreign keys
            self._conn.execute("PRAGMA foreign_keys=ON")
            
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Failed to create database connection: {e}")

    def _initialize_database(self):
        """Инициализация структуры базы данных"""
        with self.get_cursor() as cursor:
            self._create_sessions_table(cursor)
            self._create_laps_table(cursor)
            self._create_car_setups_table(cursor)
            self._create_performance_analysis_table(cursor)
            self._create_telemetry_data_table(cursor)

    def _create_sessions_table(self, cursor):
        """Создание таблицы сессий"""
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
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Индексы для производительности
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_track ON sessions(track)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_car ON sessions(car)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_timestamp ON sessions(timestamp)')

    def _create_laps_table(self, cursor):
        """Создание таблицы кругов"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS laps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                lap_number INTEGER NOT NULL,
                lap_time REAL NOT NULL,
                sector_times TEXT,
                telemetry_data TEXT,
                is_valid BOOLEAN DEFAULT 1,
                weather_conditions TEXT,
                tire_compound TEXT,
                fuel_level REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_laps_session ON laps(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_laps_time ON laps(lap_time)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_laps_valid ON laps(is_valid)')

    def _create_car_setups_table(self, cursor):
        """Создание таблицы настроек автомобиля"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS car_setups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car TEXT NOT NULL,
                track TEXT NOT NULL,
                setup_name TEXT NOT NULL,
                setup_data TEXT NOT NULL,
                notes TEXT,
                rating INTEGER DEFAULT 0,
                weather_conditions TEXT,
                is_public BOOLEAN DEFAULT 0,
                author TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(car, track, setup_name)
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_setups_car_track ON car_setups(car, track)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_setups_rating ON car_setups(rating)')

    def _create_performance_analysis_table(self, cursor):
        """Создание таблицы анализа производительности"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                analysis_type TEXT NOT NULL,
                metrics TEXT NOT NULL,
                recommendations TEXT,
                confidence_score REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
            )
        ''')

    def _create_telemetry_data_table(self, cursor):
        """Создание таблицы телеметрии"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS telemetry_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                timestamp REAL NOT NULL,
                data_blob TEXT NOT NULL,
                data_type TEXT NOT NULL DEFAULT 'json',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_telemetry_session ON telemetry_data(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp ON telemetry_data(timestamp)')

    @contextmanager
    def get_cursor(self):
        """Context manager для безопасной работы с курсором"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            yield cursor
            self.connection.commit()
        except sqlite3.Error as e:
            if self.connection:
                self.connection.rollback()
            self.logger.error(f"Database error: {e}")
            raise DatabaseQueryError(f"Database query failed: {e}")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            self.logger.error(f"Unexpected database error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def save_session(self, track: str, car: str, session_type: str, 
                    data: dict, weather: str = None, temperature: float = None,
                    lap_time: float = None, best_lap: float = None) -> int:
        """Сохранение сессии с улучшенной обработкой ошибок"""
        try:
            timestamp = datetime.datetime.now().isoformat()
            
            with self.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO sessions (timestamp, track, car, session_type, weather, 
                                        temperature, data, lap_time, best_lap)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (timestamp, track, car, session_type, weather, temperature, 
                      json.dumps(data), lap_time, best_lap))
                
                session_id = cursor.lastrowid
                self.logger.debug(f"Session saved with ID: {session_id}")
                return session_id
                
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
            raise DatabaseQueryError(f"Failed to save session: {e}")

    def save_lap(self, session_id: int, lap_number: int, lap_time: float,
                sector_times: List[float] = None, telemetry_data: dict = None, 
                is_valid: bool = True, weather_conditions: str = None,
                tire_compound: str = None, fuel_level: float = None) -> int:
        """Сохранение круга с дополнительными полями"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO laps (session_id, lap_number, lap_time, sector_times, 
                                    telemetry_data, is_valid, weather_conditions, 
                                    tire_compound, fuel_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (session_id, lap_number, lap_time, 
                      json.dumps(sector_times) if sector_times else None,
                      json.dumps(telemetry_data) if telemetry_data else None,
                      is_valid, weather_conditions, tire_compound, fuel_level))
                
                lap_id = cursor.lastrowid
                self.logger.debug(f"Lap saved with ID: {lap_id}")
                return lap_id
                
        except Exception as e:
            self.logger.error(f"Failed to save lap: {e}")
            raise DatabaseQueryError(f"Failed to save lap: {e}")

    def save_car_setup(self, car: str, track: str, setup_name: str, 
                      setup_data: dict, notes: str = "", rating: int = 0,
                      weather_conditions: str = None, author: str = None,
                      is_public: bool = False) -> int:
        """Сохранение настройки автомобиля"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    INSERT OR REPLACE INTO car_setups 
                    (car, track, setup_name, setup_data, notes, rating, 
                     weather_conditions, author, is_public, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (car, track, setup_name, json.dumps(setup_data), notes, 
                      rating, weather_conditions, author, is_public))
                
                setup_id = cursor.lastrowid
                self.logger.debug(f"Car setup saved with ID: {setup_id}")
                return setup_id
                
        except Exception as e:
            self.logger.error(f"Failed to save car setup: {e}")
            raise DatabaseQueryError(f"Failed to save car setup: {e}")

    def get_sessions(self, track: str = None, car: str = None, 
                    session_type: str = None, limit: int = None) -> List[Dict]:
        """Получение сессий с улучшенной фильтрацией"""
        try:
            limit = limit or 50  # Используем число напрямую
            
            with self.get_cursor() as cursor:
                query = "SELECT * FROM sessions WHERE 1=1"
                params = []
                
                if track:
                    query += " AND track = ?"
                    params.append(track)
                if car:
                    query += " AND car = ?"
                    params.append(car)
                if session_type:
                    query += " AND session_type = ?"
                    params.append(session_type)
                    
                query += " ORDER BY created_at DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Failed to get sessions: {e}")
            raise DatabaseQueryError(f"Failed to get sessions: {e}")

    def get_best_laps(self, track: str = None, car: str = None, 
                     valid_only: bool = True, limit: int = None) -> List[Dict]:
        """Получение лучших кругов"""
        try:
            limit = limit or 100  # Используем число напрямую
            
            with self.get_cursor() as cursor:
                query = """
                    SELECT l.*, s.track, s.car, s.weather, s.temperature
                    FROM laps l
                    JOIN sessions s ON l.session_id = s.id
                    WHERE 1=1
                """
                params = []
                
                if valid_only:
                    query += " AND l.is_valid = 1"
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
                
        except Exception as e:
            self.logger.error(f"Failed to get best laps: {e}")
            raise DatabaseQueryError(f"Failed to get best laps: {e}")

    def get_car_setups(self, car: str = None, track: str = None, 
                      weather_conditions: str = None) -> List[Dict]:
        """Получение настроек автомобиля"""
        try:
            with self.get_cursor() as cursor:
                query = "SELECT * FROM car_setups WHERE 1=1"
                params = []
                
                if car:
                    query += " AND car = ?"
                    params.append(car)
                if track:
                    query += " AND track = ?"
                    params.append(track)
                if weather_conditions:
                    query += " AND (weather_conditions = ? OR weather_conditions IS NULL)"
                    params.append(weather_conditions)
                    
                query += " ORDER BY rating DESC, updated_at DESC"
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Failed to get car setups: {e}")
            raise DatabaseQueryError(f"Failed to get car setups: {e}")

    def save_telemetry_batch(self, session_id: int, telemetry_batch: List[Dict]) -> bool:
        """Сохранение пакета данных телеметрии"""
        try:
            with self.get_cursor() as cursor:
                batch_data = []
                for telemetry in telemetry_batch:
                    timestamp = telemetry.get('timestamp', datetime.datetime.now().timestamp())
                    batch_data.append((
                        session_id,
                        timestamp,
                        json.dumps(telemetry),
                        'json'
                    ))
                
                cursor.executemany("""
                    INSERT INTO telemetry_data (session_id, timestamp, data_blob, data_type)
                    VALUES (?, ?, ?, ?)
                """, batch_data)
                
                self.logger.debug(f"Saved {len(batch_data)} telemetry records")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to save telemetry batch: {e}")
            return False

    def get_session_statistics(self, session_id: int) -> Dict:
        """Получение статистики сессии"""
        try:
            with self.get_cursor() as cursor:
                # Основная информация о сессии
                cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
                session = cursor.fetchone()
                
                if not session:
                    return {}
                
                # Статистика кругов
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_laps,
                        MIN(lap_time) as best_lap,
                        AVG(lap_time) as avg_lap,
                        COUNT(CASE WHEN is_valid = 1 THEN 1 END) as valid_laps
                    FROM laps WHERE session_id = ?
                """, (session_id,))
                
                lap_stats = cursor.fetchone()
                
                return {
                    'session': dict(session),
                    'lap_statistics': dict(lap_stats) if lap_stats else {}
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get session statistics: {e}")
            return {}

    def cleanup_old_data(self, days_to_keep: int = None) -> bool:
        """Очистка старых данных"""
        try:
            days_to_keep = days_to_keep or 90  # Используем число напрямую
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_to_keep)
            
            with self.get_cursor() as cursor:
                # Удаляем старые сессии (каскадно удалятся связанные данные)
                cursor.execute("""
                    DELETE FROM sessions 
                    WHERE created_at < ? AND id NOT IN (
                        SELECT DISTINCT session_id FROM laps 
                        WHERE lap_time = (SELECT MIN(lap_time) FROM laps)
                    )
                """, (cutoff_date.isoformat(),))
                
                deleted_sessions = cursor.rowcount
                self.logger.info(f"Cleaned up {deleted_sessions} old sessions")
                
                # Оптимизируем базу данных
                cursor.execute("VACUUM")
                
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup old data: {e}")
            return False

    def backup_database(self, backup_path: str = None) -> bool:
        """Создание резервной копии базы данных"""
        try:
            if not backup_path:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"{self.db_name}.backup_{timestamp}"
            
            backup_conn = sqlite3.connect(backup_path)
            self.connection.backup(backup_conn)
            backup_conn.close()
            
            self.logger.info(f"Database backup created: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to backup database: {e}")
            return False

    def get_database_info(self) -> Dict:
        """Получение информации о базе данных"""
        try:
            with self.get_cursor() as cursor:
                info = {}
                
                # Размер базы данных
                if self.db_path.exists():
                    info['file_size'] = self.db_path.stat().st_size
                
                # Количество записей в таблицах
                tables = ['sessions', 'laps', 'car_setups', 'performance_analysis', 'telemetry_data']
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    info[f'{table}_count'] = cursor.fetchone()[0]
                
                # Версия SQLite
                cursor.execute("SELECT sqlite_version()")
                info['sqlite_version'] = cursor.fetchone()[0]
                
                return info
                
        except Exception as e:
            self.logger.error(f"Failed to get database info: {e}")
            return {}

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def close(self):
        """Закрытие соединения с базой данных"""
        with self._lock:
            if self._conn:
                try:
                    self._conn.close()
                    self.logger.debug("Database connection closed")
                except Exception as e:
                    self.logger.error(f"Error closing database connection: {e}")
                finally:
                    self._conn = None

    def __del__(self):
        """Деструктор для гарантированного закрытия соединения"""
        self.close()
