"""Auto-feed content ideas from the Neville Goddard content pool."""

import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from modules.sourcing.content_pool import ContentPool


DAY_THEMES = {
    "Senin": ["LAW_OF_ASSUMPTION", "IDENTITY", "FUNDAMENTAL"],
    "Selasa": ["TECHNIQUE", "SATS", "REVISION"],
    "Rabu": ["MONEY", "LOVE", "MANIFESTATION"],
    "Kamis": ["MISTAKES", "MENTAL_DIET", "DAILY_PRACTICE"],
    "Jumat": ["INSPIRED_LIFE", "STORY", "PROMISE"],
    "Sabtu": ["ADVANCED", "I_AM", "CONSCIOUSNESS"],
    "Minggu": ["NEUTRALITY", "HEALING", "REFLECT"],
}


class ContentFeeder:
    """Generate content ideas automatically based on day theme + pool."""

    def __init__(self):
        self.pool = ContentPool()

    def daily_idea(self, date=None):
        """Get content idea for a given date (defaults to today)."""
        if date is None:
            date = datetime.now()
        day_name = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][date.weekday()]
        themes = DAY_THEMES.get(day_name, [])

        tag_map = {
            "LAW_OF_ASSUMPTION": "fundamental",
            "IDENTITY": "identity",
            "FUNDAMENTAL": "fundamental",
            "TECHNIQUE": "technique",
            "SATS": "sats",
            "REVISION": "revision",
            "MONEY": "money",
            "LOVE": "love",
            "MANIFESTATION": "manifestation",
            "MISTAKES": "mistakes",
            "MENTAL_DIET": "mental",
            "DAILY_PRACTICE": "daily-practice",
            "INSPIRED_LIFE": "fundamental",
            "STORY": "general",
            "PROMISE": "promise",
            "ADVANCED": "advanced",
            "I_AM": "i-am",
            "CONSCIOUSNESS": "consciousness",
            "NEUTRALITY": "neutrality",
            "HEALING": "healing",
            "REFLECT": "general",
        }

        for theme in themes:
            tag = tag_map.get(theme, "general")
            items = self.pool.get_by_tag(tag)
            if items:
                candidate = random.choice(items)
                candidate["day"] = day_name
                candidate["theme"] = theme
                candidate["format"] = self._suggest_format(theme)
                return candidate

        return random.choice(self.pool.get_random(1))

    def weekly_plan(self, start_date=None):
        """Plan content ideas for the next 7 days."""
        if start_date is None:
            start_date = datetime.now()
        plan = []
        for i in range(7):
            date = start_date + timedelta(days=i)
            idea = self.daily_idea(date)
            idea["date"] = date.strftime("%Y-%m-%d")
            plan.append(idea)
        return plan

    def _suggest_format(self, theme):
        """Suggest content format based on theme."""
        format_map = {
            "LAW_OF_ASSUMPTION": "carousel",
            "IDENTITY": "quote_card",
            "FUNDAMENTAL": "carousel",
            "TECHNIQUE": "carousel",
            "SATS": "carousel",
            "REVISION": "reels",
            "MONEY": "carousel",
            "LOVE": "reels",
            "MANIFESTATION": "quote_card",
            "MISTAKES": "carousel",
            "MENTAL_DIET": "quote_card",
            "DAILY_PRACTICE": "story",
            "INSPIRED_LIFE": "reels",
            "STORY": "reels",
            "PROMISE": "quote_card",
            "ADVANCED": "carousel",
            "I_AM": "quote_card",
            "CONSCIOUSNESS": "carousel",
            "NEUTRALITY": "quote_card",
            "HEALING": "carousel",
            "REFLECT": "quote_card",
        }
        return format_map.get(theme, "quote_card")
