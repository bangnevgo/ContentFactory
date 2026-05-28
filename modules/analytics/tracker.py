"""Instagram analytics tracker via Apify."""

import sys
import os
import json
import urllib.request
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.db import FactoryDB


class AnalyticsTracker:
    """Track Instagram metrics via Apify scraper."""

    APIFY_BASE = "https://api.apify.com/v2"

    def __init__(self, apify_token=None, db=None):
        import os
        token = apify_token or os.environ.get("APIFY_TOKEN", "")
        if not token:
            raise ValueError("Apify token required. Set APIFY_TOKEN env var or pass apify_token=...")
        self.token = token
        self.db = db or FactoryDB()

    def pull_data(self, username="nevgoinstitute", results_limit=50):
        """Scrape Instagram data via Apify."""
        url = f"{self.APIFY_BASE}/acts/dSCLg0C3YEZ83HzYX/runs"
        data = json.dumps({"usernames": [username]}).encode()

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            resp = urllib.request.urlopen(req, timeout=15)
            result = json.loads(resp.read().decode())
            run_id = result["data"]["id"]
            dataset_id = result["data"]["defaultDatasetId"]
        except Exception as e:
            return {"error": str(e)}

        import time
        for _ in range(20):
            time.sleep(10)
            status = self._check_run(run_id)
            if status == "SUCCEEDED":
                break
            elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
                return {"error": f"Run {status}"}

        return self._fetch_dataset(dataset_id, username)

    def _check_run(self, run_id):
        url = f"{self.APIFY_BASE}/actor-runs/{run_id}?token={self.token}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.token}"})
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read().decode())
            return data["data"]["status"]
        except Exception:
            return "UNKNOWN"

    def _fetch_dataset(self, dataset_id, username):
        url = f"{self.APIFY_BASE}/datasets/{dataset_id}/items?token={self.token}&format=json&clean=true"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.token}"})
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            items = json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}

        if not items or "no_items" in items[0]:
            # Fallback: try direct post scraper
            return self._fallback_scrape(username)

        profile = items[0] if isinstance(items[0], dict) else {}
        return {
            "followers": profile.get("followersCount", 0),
            "following": profile.get("followsCount", 0),
            "posts_count": profile.get("postsCount", 0),
            "biography": profile.get("biography", ""),
            "is_verified": profile.get("isVerified", False),
            "profile_pic": profile.get("profilePicUrl", ""),
        }

    def _fallback_scrape(self, username):
        """Fallback using apify instagram-scraper actor."""
        url = f"{self.APIFY_BASE}/acts/shu8hvrXbJbY3Eb9W/runs"
        data = json.dumps({
            "directUrls": [f"https://www.instagram.com/{username}/"],
            "resultsType": "posts",
            "resultsLimit": 20,
        }).encode()

        req = urllib.request.Request(
            url, data=data,
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            method="POST",
        )

        import time
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            result = json.loads(resp.read().decode())
            run_id = result["data"]["id"]
            dataset_id = result["data"]["defaultDatasetId"]
        except Exception as e:
            return {"error": str(e)}

        for _ in range(10):
            time.sleep(10)
            s = self._check_run(run_id)
            if s == "SUCCEEDED":
                break
            elif s in ("FAILED", "ABORTED"):
                return {"error": f"Fallback run {s}"}

        posts_url = f"{self.APIFY_BASE}/datasets/{dataset_id}/items?token={self.token}&format=json&clean=true"
        req = urllib.request.Request(posts_url, headers={"Authorization": f"Bearer {self.token}"})
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            posts = json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}

        valid_posts = [p for p in posts if "no_items" not in p]
        total_likes = sum(p.get("likesCount", 0) for p in valid_posts)
        total_comments = sum(p.get("commentsCount", 0) for p in valid_posts)
        posts_count = len(valid_posts)

        followers = valid_posts[0].get("ownerFollowersCount", 0) if valid_posts else 0
        following = valid_posts[0].get("ownerFollowingCount", 0) if valid_posts else 0
        engagement_rate = ((total_likes + total_comments) / max(followers, 1)) * 100 if valid_posts else 0

        return {
            "followers": followers,
            "following": following,
            "posts_count": posts_count,
            "avg_likes": (total_likes / posts_count) if posts_count else 0,
            "avg_comments": (total_comments / posts_count) if posts_count else 0,
            "engagement_rate": round(engagement_rate, 3),
            "posts": [
                {
                    "shortcode": p.get("shortCode", ""),
                    "likes": p.get("likesCount", 0),
                    "comments": p.get("commentsCount", 0),
                    "type": p.get("type", ""),
                    "timestamp": p.get("timestamp", ""),
                }
                for p in valid_posts
            ],
        }

    def save_snapshot(self, data):
        """Save analytics snapshot to database."""
        today = datetime.now().strftime("%Y-%m-%d")
        self.db.execute("""
            INSERT OR REPLACE INTO analytics
            (date, followers, following, posts_count, avg_likes, avg_comments, engagement_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            today, data.get("followers", 0), data.get("following", 0),
            data.get("posts_count", 0), data.get("avg_likes", 0),
            data.get("avg_comments", 0), data.get("engagement_rate", 0),
        ))
        return {"date": today, "followers": data.get("followers", 0)}

    def compare_with_previous(self):
        """Compare today's data with previous snapshot."""
        rows = self.db.query(
            "SELECT * FROM analytics ORDER BY date DESC LIMIT 2"
        )
        if len(rows) < 2:
            return {"message": "Need at least 2 snapshots to compare"}

        current, previous = rows[0], rows[1]
        return {
            "date": current["date"],
            "previous_date": previous["date"],
            "follower_growth": current["followers"] - previous["followers"],
            "follower_growth_pct": round(
                ((current["followers"] - previous["followers"]) / max(previous["followers"], 1)) * 100, 2
            ),
            "engagement_trend": round(current["engagement_rate"] - previous["engagement_rate"], 3),
            "avg_likes_trend": round(current["avg_likes"] - previous["avg_likes"], 2),
            "current_followers": current["followers"],
            "previous_followers": previous["followers"],
        }

    def generate_report(self):
        """Generate full analytics report."""
        rows = self.db.query("SELECT * FROM analytics ORDER BY date DESC LIMIT 7")
        if not rows:
            return {"message": "No analytics data. Run: factory analytics pull"}

        latest = rows[0]
        history = rows[::-1]

        return {
            "date": latest["date"],
            "followers": latest["followers"],
            "following": latest["following"],
            "posts_count": latest["posts_count"],
            "avg_likes": latest["avg_likes"],
            "avg_comments": latest["avg_comments"],
            "engagement_rate": latest["engagement_rate"],
            "history": [{"date": h["date"], "followers": h["followers"]} for h in history],
            "alert": self._check_alert(latest, rows[1] if len(rows) > 1 else None),
        }

    def _check_alert(self, current, previous):
        """Check for anomalies requiring attention."""
        if not previous:
            return None
        alerts = []
        if current["engagement_rate"] > 0 and previous["engagement_rate"] > 0:
            change = (current["engagement_rate"] - previous["engagement_rate"]) / max(previous["engagement_rate"], 0.01)
            if change < -0.2:
                alerts.append(f"⚠️ Engagement dropped {abs(change*100):.0f}% — investigate!")
        if current["followers"] < previous["followers"]:
            alerts.append(f"⚠️ Followers decreased: {previous['followers']} → {current['followers']}")
        return alerts if alerts else None
