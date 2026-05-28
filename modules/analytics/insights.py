"""Insights Engine — learn from analytics to improve content generation."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.db import FactoryDB


class InsightsEngine:
    """Analyze content performance → insights → feed back to generation."""

    def __init__(self, db=None):
        self.db = db or FactoryDB()

    def analyze(self):
        """Analyze what content works best on this account."""
        content_rows = self.db.query(
            "SELECT topic, type, tone, tags, status FROM content WHERE status = 'published' OR status = 'approved'"
        )
        analytics_rows = self.db.query("SELECT * FROM post_analytics ORDER BY captured_at DESC LIMIT 100")

        if not content_rows and not analytics_rows:
            return None

        return self._compute_insights(content_rows, analytics_rows)

    def _compute_insights(self, content_rows, analytics_rows):
        """Compute actionable insights from data."""
        from collections import Counter, defaultdict

        # Topic performance
        topic_perf = defaultdict(lambda: {"count": 0, "avg_likes": 0, "total_likes": 0})
        for row in analytics_rows:
            topic = row.get("content_topic", "unknown") or "unknown"
            likes = row.get("likes") or 0
            topic_perf[topic]["count"] += 1
            topic_perf[topic]["total_likes"] += likes

        top_topics = []
        for topic, data in topic_perf.items():
            if data["count"] > 0:
                data["avg_likes"] = round(data["total_likes"] / data["count"], 1)
                top_topics.append({"topic": topic, "avg_likes": data["avg_likes"], "count": data["count"]})

        top_topics.sort(key=lambda x: x["avg_likes"], reverse=True)

        # Format performance
        format_perf = defaultdict(lambda: {"count": 0, "total_likes": 0})
        for row in analytics_rows:
            fmt = row.get("post_type", "unknown") or "unknown"
            likes = row.get("likes") or 0
            format_perf[fmt]["count"] += 1
            format_perf[fmt]["total_likes"] += likes

        best_formats = []
        for fmt, data in format_perf.items():
            if data["count"] > 0:
                avg = round(data["total_likes"] / data["count"], 1)
                best_formats.append({"format": fmt, "avg_likes": avg, "count": data["count"]})

        best_formats.sort(key=lambda x: x["avg_likes"], reverse=True)

        # Content pool topics frequency — which topics we post most
        topic_freq = Counter(row.get("topic", "") for row in content_rows if row.get("topic"))

        # Underused high-potential topics (in pool but not yet posted)
        pool_rows = self.db.query("SELECT DISTINCT topic FROM content_pool")
        pool_topics = set(r["topic"] for r in pool_rows)
        posted_topics = set(topic_freq.keys())
        underused = list(pool_topics - posted_topics)[:10]

        actions = []
        if top_topics:
            actions.append(f"Prioritize topic: '{top_topics[0]['topic']}' (avg ❤️{top_topics[0]['avg_likes']:.1f})")
        if best_formats:
            actions.append(f"Prioritize format: '{best_formats[0]['format']}' (avg ❤️{best_formats[0]['avg_likes']:.1f})")
        if underused:
            actions.append(f"Untapped topics from pool: {', '.join(underused[:3])}")

        # Save insights to feedback table
        for topic in top_topics[:3]:
            self.db.execute(
                "INSERT OR IGNORE INTO feedback (topic, metric, value, insight) VALUES (?, ?, ?, ?)",
                (topic["topic"], "avg_likes", topic["avg_likes"], f"Top performing topic")
            )
        for fmt in best_formats[:3]:
            self.db.execute(
                "INSERT OR IGNORE INTO feedback (topic, format, metric, value, insight) VALUES (?, ?, ?, ?, ?)",
                ("general", fmt["format"], "avg_likes", fmt["avg_likes"], f"Best performing format")
            )

        return {
            "top_topics": top_topics[:5],
            "best_formats": best_formats[:3],
            "topic_frequency": [{"topic": k, "count": v} for k, v in topic_freq.most_common(10)],
            "underused_pool_topics": underused,
            "feedback_actions": actions,
        }

    def get_feedback(self):
        """Get accumulated feedback for generation engine."""
        rows = self.db.query(
            "SELECT * FROM feedback WHERE applied = 0 ORDER BY value DESC LIMIT 20"
        )
        return rows

    def mark_applied(self, feedback_id):
        """Mark feedback as applied to generation."""
        self.db.execute("UPDATE feedback SET applied = 1 WHERE id = ?", [feedback_id])
