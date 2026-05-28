"""Content caption generator — produces captions, hooks, and CTAs for all formats."""

import sys
import random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.generation.tones import (
    TONES, HOOKS, CTA_TEMPLATES, HASHTAG_SETS,
    apply_tone, get_hook, get_hashtag_set
)


class CaptionGenerator:
    """Generate structured content ready for Instagram publishing."""

    def __init__(self, topic="", tone="edukatif", platform="instagram", index=0):
        self.topic = topic
        self.tone_val = tone
        self.platform = platform
        self.index = index
        self.tone = TONES.get(tone, TONES["edukatif"])

    def caption(self):
        """Generate a single carousel/feed caption."""
        hook = get_hook(self.topic)
        pembuka = random.choice(self.tone["pembuka"])
        penutup = random.choice(self.tone["penutup"])
        cta = random.choice(CTA_TEMPLATES[:5])
        hashtags = " ".join(get_hashtag_set(self.index))

        body = f"""📌 {hook}

{pembuka}

{self.topic}

{self.tone["style"]}

— Bang Nevgo

{cta}

{hashtags}"""

        return {
            "title": self.topic,
            "caption": body,
            "hashtags": get_hashtag_set(self.index),
            "hook": hook,
            "cta": cta,
            "type": "caption",
            "tone": self.tone_val,
        }

    def quote_caption(self):
        """Generate a quote card caption (short, punchy)."""
        hook = get_hook(self.topic)
        penutup = random.choice(self.tone["penutup"])
        hashtags = " ".join(get_hashtag_set(self.index))

        caption = f"""{hook}

"{self.topic}"

— Neville Goddard

{penutup}

{hashtags}"""

        return {
            "title": self.topic,
            "caption": caption,
            "hashtags": get_hashtag_set(self.index),
            "hook": hook,
            "type": "quote_card",
            "tone": self.tone_val,
        }

    def carousel_caption(self, slides=7):
        """Generate full carousel content with slide-by-slide breakdown."""
        hook = get_hook(self.topic)
        pembuka = random.choice(self.tone["pembuka"])
        penutup = random.choice(self.tone["penutup"])
        cta = random.choice(CTA_TEMPLATES)

        slides_content = []
        slide_templates = []

        # Generate slide sequence based on topic
        if "sats" in self.topic.lower():
            slide_templates = [
                {"title": f"Apa itu {self.topic}?", "body": "Konsep dasar yang perlu dipahami dulu"},
                {"title": "Salah kaprah umum", "body": "Banyak yang mengira teknik ini adalah meditasi"},
                {"title": "Cara yang benar", "title_line": "Langkah 1: Enter the state", "body": "Tidur tidak, terjaga tidak — state khusus"},
                {"title": "Langkah 2: Bikin scene", "title_line": "Konten scene", "body": "Skecil mungkin, tapi kamu di dalamnya"},
                {"title": "Langkah 3: Feel it real", "title_line": "Feeling is the secret", "body": "Bukan lihat, tapi RASAKAN"},
                {"title": "Kapan latihan?", "title_line": "Setiap malam sebelum tidur", "body": "5 menit cukup. Konsisten > durasi"},
                {"title": "CTA: Mulai malam ini", "body": "Siapkan scene kamu sebelum tidur"},
            ]
        elif "kesalahan" in self.topic.lower() or "mistake" in self.topic.lower():
            slide_templates = [
                {"title": f"Hook: {self.topic}", "body": f"Penyebaban manifestasi yang kebalik"},
                {"title": "Kesalahan #1: Overtracing", "body": "'Kenapa belum manifestasi?' = keraguan"},
                {"title": "Kesalahan #2: Cari validasi luar", "body": "Perubahan dari dalam dulu"},
                {"title": "Kesalahan #3: Berharap bukan mengasumsikan", "body": "Berharap = penyangkalan"},
                {"title": "Kesalahan #4: Fokus ke masalah", "body": "Fokus ke jawaban, bukan masalah"},
                {"title": "Kesalahan #5: Ganti-ganti teknik", "content": "Satu teknik persisten > banyak teknik konsisten"},
                {"title": "CTA", "body": "Stop overtracing. Assume it's done."},
            ]
        elif "money" in self.topic.lower() or "kekayaan" in self.topic.lower() or "debt" in self.topic.lower():
            slide_templates = [
                {"title": f"💰 {self.topic}", "body": "Yang Neville ajarkan soal kekayaan"},
                {"title": "Mitos: Kerja keras dulu", "body": "KERJA KERAS TIDAK MENCIPTAKAN KEKAYAAN"},
                {"title": "Fakta: Kesadaran dulu", "content": "Uang adalah efek. Kesadaran adalah cause."},
                {"title": "State of Conciounsness of Wealth", "body": "Bagaimana masuk ke state kekayaan sekarang juga"},
                {"title": "Teknik Debt Free", "body": "Asumsikan bebas hutang — rasakan leganya"},
                {"title": "Revision for Wealth", "body": "Malam ini, revisi hari sebagai orang kaya"},
                {"title": "Start tonight", "body": "Assume the wish fulfilled. Don't ask how."},
            ]
        elif "love" in self.topic.lower() or "cinta" in self.topic.lower() or "pasangan" in self.topic.lower():
            slide_templates = [
                {"title": f"❤️ {self.topic}", "body": "Cara Neville ajarkan manifestasi cinta"},
                {"title": "Stop mencari", "body": "Mencari = mengkonfirmasi belum punya"},
                {"title": "Jadilah, jangan cari", "body": "Jadilah pasangan yang kamu inginkan"},
                {"title": "SATS untuk Cinta", "body": "Scene: mereka sudah denganmu, rasakan"},
                {"title": "Biarkan bridge muncul", "body": "Jembatannya mungkin aneh — biarkan"},
                {"title": "Change self-concept", "body": "Others see you as you see yourself"},
                {"title": "Start tonight", "content": "SATS malam ini: sudah nyata bagimu"},
            ]
        else:
            slide_templates = [
                {"title": f"📌 {self.topic}", "body": "Inti pengajaran Neville yang sering terlewat"},
                {"title": "Hook: Why this matters", "body": "Kebanyakan gagal di tahap ini"},
                {"title": "Konsep Dasar", "body": "Pemahaman yang benar dulu sebelum praktek"},
                {"title": "Cara yang Benar", "body": "Teknik yang Neville sendiri pakai"},
                {"title": "Kesalahan Umum", "body": "Yang sering bikin orang stuck"},
                {"title": "Implementasi Hari Ini", "body": "Mulai dari malam ini bisa"},
                {"title": "CTA: Save & Share", "content": "Share ke teman yang butuh!"},
            ]

        slides_content = slide_templates[:slides]

        penutup_slide = random.choice(self.tone["penutup"])
        cta_full = random.choice(CTA_TEMPLATES)
        hashtags = " ".join(get_hashtag_set(self.index))

        slides_count = len(slides_content)
        caption = f"""🎯 {hook}

{pembuka}

Swipe untuk breakdown lengkap {self.topic} →

{self.tone["style"]}

({slides_count} slides)

{penutup_slide}

{cta_full}

{hashtags}"""

        return {
            "title": self.topic,
            "caption": caption,
            "hashtags": get_hashtag_set(self.index),
            "hook": hook,
            "cta": cta_full,
            "type": "carousel",
            "tone": self.tone_val,
            "slides": [
                f"{i+1}. {s['title']}" for i, s in enumerate(slides_content)
            ],
        }

    def reels_script(self, duration=60):
        """Generate a Reels video script."""
        hook = get_hook(self.topic)
        penutup = random.choice(self.tone["penutup"])

        # Time allocation
        intro_sec = min(5, duration // 10)
        body_sec = duration - intro_sec - 5
        cta_sec = 5

        script = f"""🎬 REELS SCRIPT — {self.topic}
⏱ Durasi: {durasi}s
🎤 Tone: {self.tone["name"]}

━━━━━━━━━━━━━━━━━━━━━━
⏱ 0:{intro_sec}s — HOOK (attention grab)

TEXT ON SCREEN: "{hook}"

SPEAK: "{hook} ... bukan bermimpi. Tapi ini fakta yang Neville Goddard ajarkan sejak 1940-an."

━━━━━━━━━━━━━━━━━━━━━━
⏱ {intro_sec}:{intro_sec + body_sec}s — BODY (value delivery)

SLIDE 1 [Text on screen]:
"Kebanyakan orang gagal karena..."

SLIDE 2 [Text on screen]:
"Berharap bukan mengasumsikan."

SLIDE 3 [Hit CTA]:
"Ini yang Neville katakan..."

SLIDE 4 [Core message]:
"Asumsimu mencipta realitasmu."

SPEAK (Soft, confident):
"Jadi kalau kamu masih berharap, kamu sedang menyangkal. Neville bilang:
'Waiting, hoping, wishing are denial of the wish fulfilled.'
Kamu harus ANDAKAN."

━━━━━━━━━━━━━━━━━━━━━━
⏱ {intro_sec + body_sec}:{durasi}s — CTA

TEXT ON SCREEN: "Follow @nevgoinstitute"

SPEAK: "{penutup}"

━━━━━━━━━━━━━━━━━━━━━━
HASHTAGS: {" ".join(get_hashtag_set(self.index)[:5])}
CAPTION: {hook} — swipe ke salin carousel di profil untuk breakdown lengkap! @nevgoinstitute
━━━━━━━━━━━━━━━━━━━━━━"""

        return {
            "title": self.topic,
            "caption": script,
            "hashtags": get_hashtag_set(self.index),
            "hook": hook,
            "type": "reels_script",
            "tone": self.tone_val,
            "duration": durasi,
        }

    def email(self, day=1):
        """Generate nurture email."""
        subject_lines = [
            f"Hari {day}: Yang kebanyakan orang TAHU soal {self.topic}",
            f"Hari {day}: Satu hal yang rubah semuanya",
            f"Hari {day}: Kenapa {self.topic} bikin beda",
            f"Hari {day}: Terima kasih sudah sampai di sini",
        ]

        content_by_day = {
            1: f"""Halo!

Terima kasih sudah mendownload Panduan {self.topic}!

Selama 7 hari ke depan, kamu akan dapat seri email tentang cara praktik Law of Assumption ala NEVGO.

Minggu ini kita fokus ke:

- Hari 1 (HARI INI): Fondasi {self.topic}
- Hari 2: Cara praktik yang benar
- Hari 3: Kesalahan fatal yang harus dihindari
- Hari 4: Teknik SATS kondisi
- Hari 5: Review dan rutinitas
- Hari 6: FAQ & pertanyaan member
- Hari 7: Undangan spesial

Baca panduan ini pelan-pelan. Tidak perlu buru-buru.

Kalau ada pertanyaan, reply email ini ya.

Salam,
Bang Nevgo
@nevgoinstitute""",
            2: f"""Pagi,

Hari ini mau bahas satu kesalahan fatal soal {self.topic}.

Kebanyakan orang melakukan ini tanpa sadar — dan karenanya manifestasinya mentok.

👉 Jangan over-tracing.

"Kenapa belum manifestasi?" adalah bentuk keraguan.

Neville bilang: "Your assumption is already done."

Coba hari ini: stop checking. Assume it's done. Act from the end, not from the problem.

Beri tahu kalau kamu paham.

Salam,
Bang Nevgo""",
            3: f"""Hari 3.

Cerita dari komunitas NEVGO:

Banyak member yang report "bingung kenapa gagal" ternyata:

1. Ganti-ganti teknik tiap hari
2. Cari validasi dari luar
3. Tidak persisten di satu asumsi

Satu teknik yang persisten > 10 teknik yang random.

Kebanyakan butuh 3-7 hari persisten sebelum melihat hasil.

Malam ini: SATS 10 menit. Skena sederhana. Asumsi yang sama seperti 3 hari teratur.

Kasih tahu kabarnya.

Bang Nevgo""",
        }

        content = content_by_day.get(day, content_by_day[2])

        return {
            "title": f"Nurture Day {day}: {self.topic}",
            "caption": content,
            "subject": subject_lines[day - 1] if day <= len(subject_lines) else subject_lines[0],
            "type": "email",
            "day": day,
            "tone": self.tone_val,
        }

    def detect_format(self):
        """Auto-detect best format based on topic."""
        t = self.topic.lower()
        if "kesalahan" in t or "fatal" in t or "error" in t:
            return "carousel"
        if "cara" in t or "teknik" in t or "how" in t:
            return "carousel"
        if "sats" in t:
            return "carousel"
        if "love" in t or "money" in t or "story" in t:
            return "reels_script"
        return "quote_card"
