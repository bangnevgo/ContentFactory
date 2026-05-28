"""Batch generation — 1 brief → many content outputs."""

import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.sourcing.feeder import ContentFeeder
from modules.generation.caption_gen import CaptionGenerator
from core.schemas import ContentItem, ContentType, ContentStatus, Tone, gen_id


class BatchRunner:
    """Generate a batch of content from a brief."""

    def __init__(self, brief="weekly content plan", count=5, tone="edukatif"):
        self.brief = brief
        self.count = count
        self.tone = tone
        self.feeder = ContentFeeder()

    def run(self):
        """Generate batch content items."""
        from modules.generation.tones import HASHTAG_SETS

        plan = self.feeder.weekly_plan()
        items = []

        tones = ["edukatif", "motivational", "conversational", "authority", "soft_sell"]
        formats = ["quote_card", "carousel", "reels_script", "carousel", "quote_card"]

        for i in range(self.count):
            if i < len(plan):
                idea = plan[i]
            else:
                from modules.sourcing.content_pool import ContentPool
                pool = ContentPool()
                idea = pool.get_random(1)[0]

            topic = idea.get("topic", "Law of Assumption")
            day = idea.get("date", datetime.now().strftime("%Y-%m-%d"))
            suggested_format = idea.get("format", formats[i % len(formats)])
            tone_val = self.tone if self.tone != "auto" else tones[i % len(tones)]

            gen = CaptionGenerator(topic=topic, tone=tone_val, index=i)

            if suggested_format == "reels_script":
                result = gen.reels_script(duration=random.choice([30, 45, 60]))
            elif suggested_format == "carousel":
                result = gen.carousel_caption(slides=random.choice([5, 7, 8, 10]))
            elif suggested_format == "quote_card":
                result = gen.quote_caption()
            else:
                result = gen.caption()

            content_type_map = {
                "reels_script": ContentType.REELS_SCRIPT,
                "carousel": ContentType.CAROUSEL,
                "quote_card": ContentType.QUOTE_CARD,
                "caption": ContentType.CAPTION,
            }

            item = ContentItem(
                type=content_type_map.get(suggested_format, ContentType.CAPTION),
                topic=topic,
                tone=Tone(tone_val),
                title=result.get("title", topic),
                caption=result.get("caption", ""),
                hashtags=result.get("hashtags", []),
                body=result.get("slides", []),
                tags=idea.get("tags", "general").split(","),
            )
            item._day = day
            items.append(item)

        return items
