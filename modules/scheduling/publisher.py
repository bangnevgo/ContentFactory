"""Publisher — notify & distribute scheduled content."""

import sys
import os
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.db import FactoryDB


class Publisher:
    """Semi-auto publisher — prepares content for Telegram notification."""

    def __init__(self, db=None, config=None):
        self.db = db or FactoryDB()
        self.config = config or {}

    def get_due_notifications(self, within_minutes=30):
        """Get content due for posting notification."""
        now = datetime.now()
        future = now + timedelta(minutes=within_minutes)
        return self.db.query("""
            SELECT s.id as schedule_id, s.scheduled_at, s.platform,
                   c.content_id, c.type, c.topic, c.caption, c.hashtags, c.image_path
            FROM schedule s
            JOIN content c ON s.content_id = c.content_id
            WHERE s.scheduled_at BETWEEN ? AND ?
            AND s.status = 'scheduled'
        """, [now.strftime("%Y-%m-%d %H:%M:%S"), future.strftime("%Y-%m-%d %H:%M:%S")])

    def format_notification(self, item):
        """Format a Telegram notification message."""
        caption_preview = item["caption"][:200] if item["caption"] else "(caption kosong)"
        return f"""
🔔 POSTING REMINDER — {item['scheduled_at']}

📱 Platform: {item['platform']}
📌 Topic: {item['topic']}
📝 Type: {item['type']}
🏷 Content ID: {item['content_id']}

━━━━━━━━━━━━━━━━━━━━
CAPTION PREVIEW:
{caption_preview}...
━━━━━━━━━━━━━━━━━━━━

🖼 Image: {item.get('image_path', '(not yet generated)')}

👉 ACTION REQUIRED:
1. Copy caption above
2. Attach image/video
3. Post on {item['platform']}
4. Reply "DONE {item['schedule_id']}" to mark as published

━━━━━━━━━━━━━━━━━━━━
"""

    def send_telegram(self, message, chat_id=None, bot_token=None):
        """Send Telegram notification."""
        import urllib.request
        import urllib.parse

        token = bot_token or self.config.get("telegram_bot_token", "")
        chat = chat_id or self.config.get("telegram_chat_id", "")

        if not token or not chat:
            return {"status": "skipped", "reason": "Telegram not configured"}

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": chat,
            "text": message,
            "parse_mode": "HTML",
        }).encode()

        try:
            req = urllib.request.Request(url, data=data, method="POST")
            resp = urllib.request.urlopen(req, timeout=10)
            return {"status": "sent", "response": resp.read().decode()[:200]}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def notify_all_due(self):
        """Check and notify all due posts."""
        due = self.get_due_notifications(within_minutes=60)
        sent = []
        for item in due:
            msg = self.format_notification(item)
            result = self.send_telegram(msg)
            result["content_id"] = item["content_id"]
            result["topic"] = item["topic"]
            sent.append(result)
        return sent


from datetime import timedelta  # noqa: E402
