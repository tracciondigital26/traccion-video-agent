import sqlite3
import os
from typing import Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "metrics.db")

class MetricsEngine:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                title TEXT,
                slot TEXT, -- 'morning' or 'evening'
                style TEXT, -- 'Grip' or 'B-Roll Tech'
                hook TEXT,
                topic TEXT,
                video_path TEXT,
                audio_path TEXT,
                views INTEGER DEFAULT 0,
                retention_3s REAL DEFAULT 0.0, -- porcentaje de retención en primeros 3 segundos
                likes INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                performance_score REAL DEFAULT 0.0
            )
            """)
            conn.commit()

    def register_video(self, video_data: Dict[str, Any]) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO videos (title, slot, style, hook, topic, video_path, audio_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                video_data.get("title", "Video Tracción Digital"),
                video_data.get("slot", "morning"),
                video_data.get("style", "Grip"),
                video_data.get("hook", ""),
                video_data.get("topic", ""),
                video_data.get("video_path", ""),
                video_data.get("audio_path", "")
            ))
            conn.commit()
            return cursor.lastrowid

    def update_metrics(self, video_id: int, views: int, retention_3s: float, likes: int, shares: int):
        # Fórmula de puntuación de rendimiento ponderado (virales ponderan retención inicial y compartidos)
        score = (retention_3s * 0.4) + (likes * 0.2) + (shares * 0.4)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE videos
            SET views = ?, retention_3s = ?, likes = ?, shares = ?, performance_score = ?
            WHERE id = ?
            """, (views, retention_3s, likes, shares, score, video_id))
            conn.commit()

    def get_top_performing_topics(self, limit: int = 5) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
            SELECT topic, style, AVG(performance_score) as avg_score, AVG(retention_3s) as avg_retention
            FROM videos
            GROUP BY topic, style
            ORDER BY avg_score DESC
            LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def list_all_videos(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM videos ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    metrics = MetricsEngine()
    print("Base de datos de métricas inicializada en:", metrics.db_path)
    print("Videos registrados:", len(metrics.list_all_videos()))
