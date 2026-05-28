"""Content calendar & queue management."""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.db import FactoryDB
from core.schemas import ScheduleItem, Platform


DAY_NAMES = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
TIME_SLOTS = ["07:00", "12:00", "19:00"]


class ContentCalendar:
    """Manage content calendar and scheduling."""

    def __init__(self, db=None):
        self.db = db or FactoryDB()

    def get_upcoming(self, days=7):
        """Get upcoming scheduled content."""
        today = datetime.now().strftime("%Y-%m-%d")
        future = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        return self.db.query("""
            SELECT s.id, s.scheduled_at, s.status, s.platform,
                   c.content_id, c.type, c.topic
            FROM schedule s
            JOIN content c ON s.content_id = c.content_id
            WHERE s.scheduled_at >= ? AND s.scheduled_at <= ?
            ORDER BY s.scheduled_at
        """, [today, future])

    def schedule_content(self, content_id, scheduled_at, platform="instagram"):
        """Add content to schedule."""
        self.db.execute(
            "INSERT INTO schedule (content_id, scheduled_at, platform, status) VALUES (?, ?, ?, ?)",
            (content_id, scheduled_at, platform, "scheduled")
        )
        return {"content_id": content_id, "scheduled_at": scheduled_at, "platform": platform}

    def cancel_schedule(self, schedule_id):
        """Cancel a scheduled post."""
        self.db.execute("UPDATE schedule SET status = 'cancelled' WHERE id = ?", [schedule_id])

    def mark_published(self, schedule_id):
        """Mark scheduled content as published."""
        self.db.execute(
            "UPDATE schedule SET status = 'published', published_at = datetime('now') WHERE id = ?",
            [schedule_id]
        )

    def auto_plan(self, days=7, posts_per_day=1):
        """Auto-plan schedule for upcoming days."""
        approved = self.db.query(
            "SELECT content_id, type, topic FROM content WHERE status = 'approved' ORDER BY updated_at DESC LIMIT ?",
            [days * posts_per_day * 2]
        )
        if not approved:
            approved = self.db.query(
                "SELECT content_id, type, topic FROM content ORDER BY created_at DESC LIMIT ?",
                [days * posts_per_day]
            )

        slots = []
        for d in range(days):
            date = datetime.now() + timedelta(days=d)
            for t in range(posts_per_day):
                time_val = TIME_SLots[t % len(TIME_SLOTS)]
                scheduled = date.strftime(f"%Y-%m-%d {time_val}:00")
                slots.append({
                    "date": date.strftime("%d %b %Y"),
                    "day": DAY_NAMES[date.weekday()],
                    "time": time_val,
                    "scheduled_at": scheduled,
                    "content": approved[d * posts_per_day + t] if (d * posts_per_day + t) < len(approved) else None,
                })

        return slots

    def get_stats(self):
        """Get scheduling statistics."""
        today = datetime.now().strftime("%Y-%m-%d")
        total = self.db.query("SELECT COUNT(*) as cnt FROM schedule")[0]["cnt"]
        upcoming = self.db.query("SELECT COUNT(*) as cnt FROM schedule WHERE scheduled_at >= ? AND status = 'scheduled'", [today])[0]["cnt"]
        published = self.db.query("SELECT COUNT(*) as cnt FROM schedule WHERE status = 'published'")[0]["cnt"]
        return {"total": total, "upcoming": upcoming, "published": published}
