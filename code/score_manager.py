# score_manager.py
import sqlite3
import datetime
from code.settings import DB_FILE

class ScoreManager:
    """
    Gerencia armazenamento e leitura de scores em SQLite.
    Tabela: scores (id, player_name, points, play_time_seconds, created_at)
    """

    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._ensure_table()

    def _ensure_table(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                points INTEGER NOT NULL,
                play_time_seconds REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def add_score(self, player_name: str, points: int, play_time_seconds: float):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO scores (player_name, points, play_time_seconds, created_at)
            VALUES (?, ?, ?, ?)
        """, (player_name, points, play_time_seconds, datetime.datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()

    def top_scores(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            SELECT player_name, points, play_time_seconds, created_at
            FROM scores
            ORDER BY points DESC, play_time_seconds DESC
            LIMIT ?
        """, (limit,))
        rows = c.fetchall()
        conn.close()
        return rows
