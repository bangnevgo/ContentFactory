"""Repurposing Engine — 1 konten → banyak format."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class Repurposer:
    """Repurpose content into multiple formats."""

    def __init__(self, content_item):
        self.item = content_item
        self.topic = content_item.get("topic", "")
        self.caption = content_item.get("caption", "")
        self.slides = content_item.get("body", "")
        self.hashtags = content_item.get("hashtags", "")

    def to_all(self):
        """Generate all format variations."""
        return {
            "carousel_to_quote_cards": self.to_quote_cards(),
            "carousel_to_reels": self.to_reels_script(),
            "carousel_to_blog": self.to_blog(),
            "carousel_to_email": self.to_email(),
            "carousel_to_thread": self.to_thread(),
            "carousel_to_story": self.to_story_series(),
        }

    def to_quote_cards(self):
        """Extract individual quotes from carousel as shareable cards."""
        lines = self.caption.split("\n")
        quotes = [l.strip() for l in lines if l.strip().startswith(("📌", "🎯", "👉", '"', "✦", "💡"))]

        if not quotes:
            quotes = [
                f"{self.topic}: Asumsimu mencipta realitasmu. — Neville Goddard",
                f"Assume the feeling of the wish fulfilled. — {self.topic}",
                f"Kamu lebih kuat dari yang kamu kira. Mulai malam ini. — NEVGO",
            ]

        return {
            "format": "quote_cards",
            "count": len(quotes),
            "cards": [
                {"text": q, "background": "dark_gradient", "overlay": "nevillegodard"}
                for q in quotes
            ],
        }

    def to_reels_script(self):
        """Carousels -> Reels script: each slide = 1 scene."""
        has_slides = []
        if isinstance(self.slides, list):
            has_slides = self.slides
        elif isinstance(self.slides, str) and self.slides:
            has_slides = [s.strip() for s in self.slides.split("\n") if s.strip()]

        if not has_slides:
            has_slides = [
                f"Hook: {self.topic}",
                "Slide 2: Core concept",
                "Slide 3: How to practice",
                "CTA: Follow for more",
            ]

        total_duration = min(60, max(30, len(has_slides) * 10))

        scenes = []
        time_pointer = 0
        for i, slide in enumerate(has_slides[:8]):
            duration = total_duration // len(has_slides[:8])
            scenes.append({
                "scene": i + 1,
                "time": f"{time_pointer}s-{time_pointer + duration}s",
                "text_on_screen": slide[:80],
                "speaker": slide,
            })
            time_pointer += duration

        return {
            "format": "reels_script",
            "duration": total_duration,
            "scenes": scenes,
            "title": f"Reels: {self.topic}",
        }

    def to_blog(self):
        """Expand carousel into blog post."""
        blog = f"""# {self.topic}

## Pendahuluan

Dalam pengajaran Neville Goddard tentang Law of Assumption, ada satu konsep yang sering salah dipahami: **{self.topic}**.

Banyak praktisi yang sudah bertahun-tahun belajar tapi masih stuck di titik yang sama. Mengapa?

## Inti Konsep

{self.caption.split(chr(10))[0] if self.caption else "Konsep ini berkaitan dengan asumsi mendasar kita tentang realitas."}

## Cara Praktek

Neville sendiri selalu mengajarkan bahwa teori tanpa praktek tidak berarti. Berikut implementasi hariannya:

1. **Pagi hari**: Awali dengan SATS 5 menit sebelum benar-benar bangun
2. **Siang hari**: Jaga inner conversation — stop negative assumptions
3. **Malam hari**: Revision sebelum tidur

## Kesalahan Umum

- Over-tracing / terlalu cek hasil
- Ganti-ganti teknik tiap hari
- Cari validasi dari luar

## Kesimpulan

{self.topic} bukan sekadar teknik — tapi perubahan kesadaran. Siapa dirimu sekarang menentukan siapa dirimu besok.

---

*Dari @nevgoinstitute — Pure Teaching Neville Goddard*
"""

        return {
            "format": "blog_post",
            "title": f"{self.topic} — Panduan Lengkap",
            "body": blog,
            "word_count": len(blog.split()),
        }

    def to_email(self):
        """Convert carousel into nurture email."""
        email = f"""Subject: {self.topic} — Insight penting yang perlu kamu baca

Halo,

Mau bahas soal {self.topic} — konsep yang sering jadi titik balik member NEVGO.

{self.caption[:500] if self.caption else "Inti dari pengajaran Neville adalah: asumsimu mencipta realitasmu."}

Takeaway utama: Assume the wish fulfilled. Bukan besok. Bukan nanti. TAPI SEKARANG.

Mau deep dive lebih dalam? Kelas Private 101 tersedia tiap bulan.

Salam,
Bang Nevgo
Nevgo Institute
@nevgoinstitute
"""

        return {
            "format": "email",
            "subject": f"{self.topic} — Insight penting",
            "body": email,
        }

    def to_thread(self):
        """Convert carousel to Twitter/X thread."""
        lines = self.caption.split("\n")
        tweets = []
        tweet = f"🧵 {self.topic}\n\n— Dalam pengajaran Neville Goddard, ada satu konsep yang mengubah segalanya.\n\nThread 🧵"
        tweets.append(tweet)

        key_lines = [l.strip() for l in lines if l.strip() and len(l.strip()) > 10][:8]
        for i, line in enumerate(key_lines, 2):
            if len(line) < 250:
                tweets.append(f"{i}/ {line}")

        tweets.append(f"{len(tweets)}/ Follow @nevgoinstitute untuk materi Neville Goddard setiap hari. 🙏")

        return {
            "format": "twitter_thread",
            "tweet_count": len(tweets),
            "tweets": tweets,
        }

    def to_story_series(self):
        """Split carousel slides into Instagram Story sequence."""
        has_slides = []
        if isinstance(self.slides, list):
            has_slides = self.slides
        elif isinstance(self.slides, str) and self.slides:
            has_slides = [s.strip() for s in self.slides.split("\n") if s.strip()]

        if not has_slides:
            has_slides = [f"Story: {self.topic}", "Hook", "Value", "CTA"]

        stories = []
        for i, slide in enumerate(has_slides):
            stories.append({
                "slide": i + 1,
                "type": "value" if i < len(has_slides) - 1 else "cta",
                "text": slide[:60],
                "dimensions": "1080x1920",
                "cta_button": "Swipe Up" if i == len(has_slides) - 1 else None,
            })

        return {
            "format": "story_series",
            "story_count": len(stories),
            "stories": stories,
        }

    def resize_for_platform(self, content, platform):
        """Auto-resize content specifications per platform."""
        specs = {
            "instagram_feed": {"width": 1080, "height": 1080, "caption_max": 2200},
            "instagram_story": {"width": 1080, "height": 1920, "caption_max": 0},
            "instagram_reels": {"width": 1080, "height": 1920, "caption_max": 2200},
            "twitter": {"width": 1200, "height": 675, "caption_max": 280},
            "tiktok": {"width": 1080, "height": 1920, "caption_max": 2200},
            "linkedin": {"width": 1200, "height": 627, "caption_max": 3000},
        }
        spec = specs.get(platform, specs["instagram_feed"])
        return {"content": content, "platform": platform, "specs": spec}
