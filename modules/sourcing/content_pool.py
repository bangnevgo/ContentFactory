"""Content Pool — single source of truth for all Neville Goddard content ideas."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.db import FactoryDB

POOL = [
    # ============ CORE NEVILLE CONCEPTS ============
    {
        "topic": "Law of Assumption",
        "quotes": [
            "Assume the feeling of the wish fulfilled and observe the route that your attention follows.",
            "The world is a mirror, forever reflecting what you are doing within yourself.",
            "An assumption, though false, if persisted in, will harden into fact.",
        ],
        "concept": "Hukum Asumsi: Asumsi yang bertahan jadi fakta. Dunia adalah cermin dari asumsi internal.",
        "source": "Neville Goddard - The Power of Awareness",
        "tags": "fundamental,law-of-assumption,core,neville",
    },
    {
        "topic": "SATS (State Akin To Sleep)",
        "quotes": [
            "Enter a state akin to sleep, yet in full possession of your waking faculties.",
            "In SATS, construct a small scene that implies the wish fulfilled. Live in it.",
        ],
        "concept": "Teknik manifestasi di ambang tidur. Theta brainwave state = medium paling powerful untuk menanam asumsi.",
        "source": "Neville Goddard - At Your Command",
        "tags": "technique,sats,manifestation,sleep",
    },
    {
        "topic": "Living in the End",
        "quotes": [
            "Live in the end — the feeling of the wish fulfilled.",
            "All hardship comes from dwelling in the means and losing sight of the end.",
        ],
        "concept": "Tinggal di akhir (goal state), abaikan cara/means. Jalan muncul dengan sendirinya.",
        "source": "Neville Goddard - Feeling is the Secret",
        "tags": "fundamental,living-in-the-end,state,goal",
    },
    {
        "topic": "Revision",
        "quotes": [
            "Revise the day each night. Rewrite every scene as you wished it had happened.",
            "Revision is the great cleansing of the soul.",
        ],
        "concept": "Teknik revisi harian sebelum tidur — rewrite realitas seperti yang diinginkan.",
        "source": "Neville Goddard - The Law and the Promise",
        "tags": "technique,revision,night,daily-practice",
    },
    {
        "topic": "Mental Diet",
        "quotes": [
            "Watch your inner conversations. Every mental act objectifies itself as fact.",
            "Stop entertaining thoughts that contradict your assumption.",
        ],
        "concept": "Diet mental: jaga percakapan internal, jangan biarkan pikiran bertentangan dengan asumsi.",
        "source": "Neville Goddard - The Power of Awareness",
        "tags": "daily-practice,mental,awareness,habit",
    },
    {
        "topic": "I AM Meditation",
        "quotes": [
            "I AM is the Creator. The voice of God.",
            "I AM the wish fulfilled, and it is done.",
        ],
        "concept": "I AM adalah kesadaran tertinggi — meditasi identitas kreatif.",
        "source": "Neville Goddard - The Power of Awareness",
        "tags": "advanced,meditation,i-am,consciousness",
    },
    {
        "topic": "The Promise",
        "quotes": [
            "The Promise: persist in your assumption and it will harden into fact.",
            "Within three days, your assumption will objectify itself.",
        ],
        "concept": "Janji Neville: Asumsi yang bertahan jadi fakta dalam 3 hari. Human patience vs persistence.",
        "source": "Neville Goddard - The Law and the Promise",
        "tags": "fundamental,faith,persistence,promise",
    },
    {
        "topic": "Bridge of Events",
        "quotes": [
            "The bridge of incidents is the way it works out. Never worry about the bridge.",
            "Do not be surprised if the person moves strangely toward you.",
        ],
        "concept": "Jembatan peristiwa: cara manifestasi terwujud. Sering tidak terduga dan aneh — jangan khawatir.",
        "source": "Neville Goddard - The Law and the Promise",
        "tags": "advanced,bridge,process,surrender",
    },
    {
        "topic": "The Theater of the Mind",
        "quotes": [
            "Construct a tiny scene implying your wish fulfilled. Repeat until real.",
            "The theater of your mind is your workshop.",
        ],
        "concept": "Workshop mental: bangun skena kecil yang mengindikasikan wish fulfilled. Ulangi sampai terasa nyata.",
        "source": "Neville Goddard - Resurrection",
        "tags": "technique,theater,visualization,mind",
    },
    {
        "topic": "Feeling is the Secret",
        "quotes": [
            "Feeling is the secret of prayer.",
            "The world is the mirror of your feeling, not your thinking.",
        ],
        "concept": "Bukan visualisasi/speech yang mencipta — tapi feeling. Dunia memperlihatkan perasaan, bukan pikiran.",
        "source": "Neville Goddard - Feeling is the Secret",
        "tags": "core,feeling,secret,heart",
    },

    # ============ COMMON MISTAKES ============
    {
        "topic": "Kesalahan Fatal: Tunggu-Harap-Ingin",
        "quotes": [
            "Waiting, hoping, and wishing are denial of the wish fulfilled.",
            "Jangan berharap — ANDAKAN.",
        ],
        "concept": "Berharap adalah penyangkalan. Ganti 'saya harap' dengan 'saya adalah/saya sudah'.",
        "source": "Neville Goddard - The Power of Awareness",
        "tags": "mistakes,denial,fundamental,daily-practice",
    },
    {
        "topic": "Kesalahan Fatal: Overtracing",
        "quotes": [
            "The more you try to force, the more you push it away.",
            "Stop checking. Stop wondering. Your assumption is already done.",
        ],
        "concept": "Overtracing (mengecek berlebihan): 'Kenapa belum?' adalah bentuk keraguan.",
        "source": "Neville Goddard - Your Faith is Your Fortune",
        "tags": "mistakes,overtracing,patience,faith",
    },
    {
        "topic": "Kesalahan Fatal: Cari Validasi Eksternal",
        "quotes": [
            "No man can come to me except my own consciousness draws him.",
            "The outer world cannot teach you. Only consciousness can.",
        ],
        "concept": "Kesalahan cari bukti dari luar. Perubahan selalu dari dalam dulu.",
        "source": "Neville Goddard - Out of This World",
        "tags": "mistakes,validation,inside-out,consciousness",
    },
    {
        "topic": "Kesalahan Fatal: Fokus ke Masalah Bukan Jawaban",
        "quotes": [
            "Focus on the answer, not the problem. The problem is just an old assumption.",
            "You do not destroy problems — you REPLACE them with new assumptions.",
        ],
        "concept": "Jangan fokus ke masalah. Fokus ke jawaban (siapa yang sudah solve).",
        "source": "Neville Goddard - The Power of Awareness",
        "tags": "mistakes,focus,answer,shift",
    },

    # ============ MONEY & WEALTH ============
    {
        "topic": "Manifestasi Kekayaan",
        "quotes": [
            "There is no want. Want is belief in separation.",
            "Assume the state of the person who already has, and watch the world conform.",
        ],
        "concept": "Kekayaan datang dari state kesadaran, bukan kerja keras. Asumsi 'saya sudah cukup'.",
        "source": "Neville Goddard - Feeling is the Secret",
        "tags": "money,wealth,abundance,assumption",
    },
    {
        "topic": "Debt Free State",
        "quotes": [
            "Assume you are free of debt and remain in that state until fact.",
            "Man makes his own prison of lack. Walk out by assumption.",
        ],
        "concept": "Teknik Debt Free State: asumsi bebas hutang + perasaan lega.",
        "source": "Neville Goddard - The Power of Awareness",
        "tags": "money,debt,technique,state",
    },
    {
        "topic": "Uang Bukan Tapi Kesadaran",
        "quotes": [
            "Stop making money your goal. Seek the consciousness of abundance instead.",
            "Money is the effect. Consciousness is the cause.",
        ],
        "concept": "Uang adalah efek samping dari state kekayaan. Fokus ke cause, bukan effect.",
        "source": "Neville Goddard - Awakened Imagination",
        "tags": "money,mindset,cause-effect,consciousness",
    },

    # ============ LOVE & RELATIONSHIPS ============
    {
        "topic": "Manifestasi Cinta & Pasangan",
        "quotes": [
            "You are already the lover you want to be in imagination. Feel it real.",
            "Do not seek — BECOME. Then it comes to you.",
        ],
        "concept": "Cinta dimanifestasi menjadi, bukan mencari. Self-concept menentukan pasangan.",
        "source": "Neville Goddard - The Law and the Promise",
        "tags": "love,relationship,become,manifestation",
    },
    {
        "topic": "Konsep Diri Menentukan Hubungan",
        "quotes": [
            "Others see you as you see yourself.",
            "To change your marriage, change your conception of yourself as a spouse.",
        ],
        "concept": "Orang lain merefleksikan konsep diri. Ganti konsep, ganti hubungan.",
        "source": "Neville Goddard - Your Faith is Your Fortune",
        "tags": "love,self-concept,relationship,change",
    },

    # ============ MINDSET & IDENTITY ============
    {
        "topic": "Identitas Kesadaran (NEVGO Core)",
        "quotes": [
            "Change your conception of yourself and you will automatically change the world.",
            "I AM is the self-definition given by God.",
        ],
        "concept": "Ini inti pengajaran NEVGO: Kesadaran Identitas bukan teknik. Siapa dirimu menciptakan siapa duniamu.",
        "source": "Neville Goddard - The Power of Awareness + NEVGO synthesis",
        "tags": "core,identity,consciousness,nevgo-differentiation",
    },
    {
        "topic": "The Power of Neutrality",
        "quotes": [
            "Neutrality assumes nothing, and therefore all things are possible.",
            "In detachment from all outcomes, infinite power flows.",
        ],
        "concept": "Tenang (neutrality) = puncak kekuatan manifestasi. Asumsi tanpa axiety = manifestasi murni.",
        "source": "Neville Goddard - At Your Command",
        "tags": "advanced,neutrality,detachment,peace",
    },
    {
        "topic": "Inner Child Healing",
        "quotes": [
            "Your inner child holds the blueprint of your assumptions.",
            "Heal the child — heal the assumptions — heal the reality.",
        ],
        "concept": "Inner child menyimpan asumsi mendasar. Sering jadi blind spot manifestasi.",
        "source": "Inner Work synthesis - NEVGO",
        "tags": "healing,inner-child,mindset,deep-work",
    },
    {
        "topic": "Visualisasi Bukan Cukup — Feeling Diperlukan",
        "quotes": [
            "Many visualize and fail. Feeling is the secret, not seeing.",
            "See it → FEEL it → Be it. Most stop at 'see'.",
        ],
        "concept": "Visualisasi tanpa feeling = wishful thinking. Feeling is the bridge.",
        "source": "Neville Goddard - Feeling is the Secret",
        "tags": "technique,feeling,visualization,common-mistake",
    },
    {
        "topic": "Keberanian Asumsi",
        "quotes": [
            "It takes courage to assume what the senses deny.",
            "Faith is assumption despite evidence to the contrary.",
        ],
        "concept": "Manifestasi butuh keberanian — saat dunia berlawanan, tanam asumsi.",
        "source": "Neville Goddard - Your Faith is Your Fortune",
        "tags": "faith,courage,persistence,conspiracy",
    },
]


class ContentPool:
    """Access Neville Goddard content pool as structured data."""

    def __init__(self, db=None, db_path="data/factory.db"):
        self.db = db or FactoryDB(db_path)

    def seed(self):
        """Insert pool into database if empty."""
        existing = self.db.query("SELECT COUNT(*) as cnt FROM content_pool")[0]["cnt"]
        if existing > 0:
            return existing
        for item in POOL:
            self.db.execute(
                "INSERT INTO content_pool (topic, quote, concept, source, tags) VALUES (?, ?, ?, ?, ?)",
                (item["topic"], "\n".join(item["quotes"]), item["concept"], item["source"], item["tags"])
            )
        return len(POOL)

    def get_topics(self):
        """List all available topics."""
        return self.db.query("SELECT DISTINCT topic, tags FROM content_pool ORDER BY topic")

    def get_by_tag(self, tag):
        """Get topics filtered by tag."""
        return self.db.query(
            "SELECT * FROM content_pool WHERE tags LIKE ? ORDER BY topic",
            [f"%{tag}%"]
        )

    def get_random(self, count=1):
        """Get random topics for batch generation."""
        return self.db.query(
            "SELECT * FROM content_pool ORDER BY RANDOM() LIMIT ?",
            [count]
        )

    def search(self, keyword):
        """Search topics, quotes, or concepts."""
        return self.db.query(
            "SELECT * FROM content_pool WHERE topic LIKE ? OR concept LIKE ? OR quote LIKE ?",
            [f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"]
        )
