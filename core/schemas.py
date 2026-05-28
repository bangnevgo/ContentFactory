from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid


class ContentType(str, Enum):
    QUOTE_CARD = "quote_card"
    CAROUSEL = "carousel"
    REELS_SCRIPT = "reels_script"
    STORY = "story"
    EMAIL = "email"
    CAPTION = "caption"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Tone(str, Enum):
    EDUKATIF = "edukatif"
    MOTIVATIONAL = "motivational"
    CONVERSATIONAL = "conversational"
    AUTHORITY = "authority"
    SOFT_SELL = "soft_sell"


class Platform(str, Enum):
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    EMAIL = "email"
    TWITTER = "twitter"


def gen_id():
    return uuid.uuid4().hex[:12]


@dataclass
class ContentItem:
    type: ContentType
    topic: str
    tone: Tone = Tone.EDUKATIF
    title: str = ""
    body: str = ""
    caption: str = ""
    hashtags: list = field(default_factory=list)
    image_path: str = ""
    tags: list = field(default_factory=list)
    status: ContentStatus = ContentStatus.DRAFT
    content_id: str = field(default_factory=gen_id)

    def db_row(self):
        return {
            "content_id": self.content_id,
            "type": self.type.value,
            "topic": self.topic,
            "tone": self.tone.value,
            "title": self.title,
            "body": self.body,
            "caption": self.caption,
            "hashtags": " ".join(self.hashtags),
            "image_path": self.image_path,
            "tags": ",".join(self.tags),
            "status": self.status.value,
        }


@dataclass
class ScheduleItem:
    content_id: str
    platform: Platform = Platform.INSTAGRAM
    scheduled_at: str = ""
    status: str = "scheduled"


@dataclass
class AnalyticsSnapshot:
    date: str
    followers: int = 0
    following: int = 0
    posts_count: int = 0
    avg_likes: float = 0.0
    avg_comments: float = 0.0
    engagement_rate: float = 0.0
