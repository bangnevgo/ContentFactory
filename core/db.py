import sqlite3
import os
from datetime import datetime
from pathlib import Path


class FactoryDB:
    def __init__(self, db_path="data/factory.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS content_pool (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                quote TEXT,
                concept TEXT,
                source TEXT,
                tags TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                topic TEXT NOT NULL,
                tone TEXT DEFAULT 'edukatif',
                title TEXT,
                body TEXT,
                caption TEXT,
                hashtags TEXT,
                image_path TEXT,
                tags TEXT,
                status TEXT DEFAULT 'draft',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS content_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT NOT NULL,
                version INTEGER NOT NULL,
                caption TEXT,
                body TEXT,
                changed_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (content_id) REFERENCES content(content_id)
            );

            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT NOT NULL,
                platform TEXT DEFAULT 'instagram',
                scheduled_at TEXT NOT NULL,
                published_at TEXT,
                status TEXT DEFAULT 'scheduled',
                FOREIGN KEY (content_id) REFERENCES content(content_id)
            );

            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                followers INTEGER,
                following INTEGER,
                posts_count INTEGER,
                avg_likes REAL,
                avg_comments REAL,
                engagement_rate REAL,
                best_post_id TEXT,
                best_post_likes INTEGER,
                worst_post_id TEXT,
                worst_post_likes INTEGER,
                captured_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS post_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_shortcode TEXT,
                likes INTEGER,
                comments INTEGER,
                post_type TEXT,
                timestamp TEXT,
                content_topic TEXT,
                captured_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                format TEXT,
                metric TEXT,
                value REAL,
                insight TEXT,
                applied BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_content_status ON content(status);
            CREATE INDEX IF NOT EXISTS idx_content_topic ON content(topic);
            CREATE INDEX IF NOT EXISTS idx_schedule_status ON schedule(status);
            CREATE INDEX IF NOT EXISTS idx_schedule_date ON schedule(scheduled_at);
            CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics(date);
        """)
        self.db.commit()

    def insert_content(self, row):
        fields = {k: v for k, v in row.items() if k != 'id'}
        cols = ", ".join(fields.keys())
        placeholders = ", ".join("?" for _ in fields)
        self.db.execute(f"INSERT INTO content ({cols}) VALUES ({placeholders})", list(fields.values()))
        self.db.commit()

    def update_content(self, content_id, updates):
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [content_id]
        self.db.execute(f"UPDATE content SET {set_clause}, updated_at = datetime('now') WHERE content_id = ?", values)
        self.db.commit()

    def insert_version(self, content_id, version, caption=None, body=None):
        self.db.execute(
            "INSERT INTO content_versions (content_id, version, caption, body) VALUES (?, ?, ?, ?)",
            (content_id, version, caption, body)
        )
        self.db.commit()

    def query(self, sql, params=None):
        cur = self.db.execute(sql, params or [])
        return [dict(r) for r in cur.fetchall()]

    def execute(self, sql, params=None):
        self.db.execute(sql, params or [])
        self.db.commit()

    def close(self):
        self.db.close()
