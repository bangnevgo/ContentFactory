#!/usr/bin/env python3
"""Neville Goddard Content Factory v1.0 — @nevgoinstitute"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.db import FactoryDB
from core.schemas import ContentItem, ContentType, ContentStatus, Tone, Platform, gen_id


def _load_config():
    """Load config from config.local.yaml > config.yaml > env vars."""
    base = Path(__file__).parent
    for name in ("config.local.yaml", "config.yaml"):
        path = base / name
        if path.exists():
            import yaml
            with open(path) as f:
                cfg = yaml.safe_load(f)
            if cfg and "apis" in cfg:
                for k, v in cfg["apis"].items():
                    env_key = k.upper()
                    if env_key in os.environ:
                        cfg["apis"][k] = os.environ[env_key]
                    elif isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                        env_var = v[2:-1]
                        cfg["apis"][k] = os.environ.get(env_var, "")
                return cfg
    return {}


CONFIG = _load_config()


def cmd_source_list(args):
    """Explore content pool topics."""
    db = FactoryDB()
    rows = db.query("SELECT DISTINCT topic FROM content_pool ORDER BY topic")
    if not rows:
        print("Content pool kosong. Jalankan: factory source seed")
        return
    print(f"\n{'='*50}")
    print(f"  CONTENT POOL ({len(rows)} topik)")
    print(f"{'='*50}")
    for i, r in enumerate(rows, 1):
        print(f"  {i:2d}. {r['topic']}")
    print()


def cmd_source_seed(args):
    """Seed content pool from Neville Goddard knowledge base."""
    db = FactoryDB()
    existing = db.query("SELECT COUNT(*) as cnt FROM content_pool")[0]["cnt"]

    pool = [
        # Core Neville Concepts
        {"topic": "Law of Assumption Fundamentals", "quote": "Assume the feeling of the wish fulfilled and observe the route that your attention follows.", "concept": "Hukum Asumsi Neville Goddard — asumsi adalah pencipta realitas", "source": "Neville Goddard - The Power of Awareness"},
        {"topic": "SATS (State Akin To Sleep)", "quote": "Enter the state akin to sleep... drowsy, sleepy state, yet in full control of your thoughts.", "concept": "Teknik manifestasi di ambang tidur (theta brainwave state)", "source": "Neville Goddard - At Your Command"},
        {"topic": "Living in the End", "quote": "Live in the end — the feeling of the wish fulfilled. All hardship comes from dwelling in the means.", "concept": "Berada di akhir (state tujuan tercapai) vs jalan/means", "source": "Neville Goddard - Feeling is the Secret"},
        {"topic": "Revision Technique", "quote": "Revise the day each night before sleep. Rewrite events as you wished they happened.", "concept": "Teknik revisi mental sebelum tidur", "source": "Neville Goddard - The Law and the Promise"},
        {"topic": "Mental Diet", "quote": "Watch your inner conversations. Every mental act eventually objectifies itself as concrete fact.", "concept": "Diet mental — jaga pikiran dan asumsi internal", "source": "Neville Goddard - The Power of Awareness"},
        {"topic": "Feeling is the Secret", "quote": "Feeling is the secret of prayer. Pray feelingly and you will be answered speedily.", "concept": "Perasaan adalah kunci — bukan sekadar visualisasi tapi feeling", "source": "Neville Goddard - Feeling is the Secret"},
        {"topic": "Bridge of Events", "quote": "The bridge of incidents is the way it works out. Never worry about the bridge.", "concept": "Jembatan peristiwa — cara manifestasi terwujud di dunia fisik", "source": "Neville Goddard - The Law and the Promise"},
        {"topic": "Dwell in the End, Not the Means", "quote": "Man can go directly to the end he desires passing over as beneath his notice all the intermediate 'acts'.", "concept": "Fokus ke hasil akhir, abaikan cara/means", "source": "Neville Goddard - The Search"},
        {"topic": "Identity & Consciousness Shift", "quote": "I AM is the feeling of the wish fulfilled. Change your conception of yourself and you will automatically change.", "concept": "Pergeseran identitas & kesadaran — konsep I AM", "source": "Neville Goddard - The Power of Awareness"},
        {"topic": "Persistence in Assumption", "quote": "If you would assume only one thing — that you already are what you want to be — and continue therein.", "concept": "Kekonsistenan dalam asumsi — sampai lupa sebelumnya", "source": "Neville Goddard - Seedtime and Harvest"},

        # Common Mistakes
        {"topic": "Kesalahan Fatal dalam Manifestasi", "quote": "Kebanyakan orang memanifestasi kebalikannya karena asumsi mereka.", "concept": "15 kesalahan fatal dalam praktik Hukum Asumsi", "source": "Navigasi Manifestasi LOAS"},
        {"topic": "Overtracing & Forcing", "quote": "The more you try to force it, the more you push it away.", "concept": "Kesalahan overtracing — terlalu berusaha memaksakan hasil", "source": "Neville Goddard - Your Faith is Your Fortune"},
        {"topic": "Waiting, Hoping, Wishing vs Assuming", "quote": "Waiting, hoping, and wishing are denial of the wish fulfilled. Only assumption creates.", "concept": "Perbedaan berharap vs mengasumsikan — berharap adalah penyangkalan", "source": "Neville Goddard - The Power of Awareness"},
        {"topic": "External vs Internal Validation", "quote": "No man can come to me except my own consciousness draws him.", "concept": "Jangan cari validasi eksternal — perubahan dimulai dari dalam", "source": "Neville Goddard - Out of This World"},
        {"topic": "Lingkungan vs Keberanian Asumsi", "quote": "Your surroundings are the drama of your assumptions.", "concept": "Lingkungan tidak menentukan — asumsi yang membentuk lingkungan", "source": "Neville Goddard - The Law and the Promise"},

        # Money/Wealth
        {"topic": "Manifestasi Kekayaan", "quote": "There is no want. Want is belief in separation from God.", "concept": "Hapus konsep kekurangan — kekayaan adalah state kesadaran", "source": "Neville Goddard - Feeling is the Secret"},
        {"topic": "Debt Free State", "quote": "Assume you are free of debt and remain in that state until it hardens into fact.", "concept": "Teknik Debt Free State — asumsi bebas hutang", "source": "Neville Goddard - The Power of Awareness"},
        {"topic": "Kaya Bukan Tujuan Tapi Keberlimpahan", "quote": "Stop making money your goal. Instead, seek the state of consciousness that matches your desire.", "concept": "Uang bukan tujuan — tapi state kesadaran yang diwujudkan", "source": "Neville Goddard - Awakened Imagination"},

        # Love/Relationship
        {"topic": "Manifestasi Cinta & Pasangan", "quote": "You are already the lover you want to be in imagination. Feel it real and it will externalize.", "concept": "Cinta adalah asumsi — berhenti cari, jadi", "source": "Neville Goddard - The Law and the Promise"},
        {"topic": "Self-Concept dalam Cinta", "quote": "A change in your concept of yourself will change the concept others have of you.", "concept": "Bagaimana konsep diri mempengaruhi hubungan", "source": "Neville Goddard - Your Faith is Your Fortune"},
        {"topic": "Jembatan Peristiwa Cinta", "quote": "Do not be surprised if the person you want moves strangely toward you. The bridge of events is unknown.", "concept": "Mengapa segalanya berubah setelah SATS sebelum tidur", "source": "Neville Goddard - The Law"},

        # Mindset/Inner Work
        {"topic": "Inner Child Healing", "quote": "Your inner child holds the blueprint of your assumptions. Heal it, heal your reality.", "concept": "Penyembuhan inner child = perbaikan asumsi mendasar", "source": "Inner Work - Neville adaptation"},
        {"topic": "Ho'oponopono & Rekonsiliasi Dalam", "quote": "I'm sorry, please forgive me, thank you, I love you — cleansing the hard drive of consciousness.", "concept": "Ho'oponopono sebagai teknik cleansing asumsi", "source": "Ho'oponopono synthesis"},
        {"topic": "The Power of Neutrality", "quote": "Neutrality assumes nothing. It is the fertile ground where all things are possible.", "concept": "Kekuatan netralitas — keadaan kesadaran tanpa judgment", "source": "Neville Goddard - At Your Command"},
        {"topic": "SATS vs Meditation", "quote": "Meditation empties the mind. SATS fills it with the wish fulfilled.", "concept": "Perbedaan SATS dan meditasi — SATS bersifat intentional", "source": "Neville Goddard comparison"},
        {"topic": "Visualization vs Feeling", "quote": "It's not about seeing. It's about FEELING it real. Feeling is the secret.", "concept": "Visualisasi biasa vs feeling yang menyelam (embodied)", "source": "Neville Goddard - Feeling is the Secret"},

        # Faith/Persistence
        {"topic": "Kepercayaan (Faith) dalam Manifestasi", "quote": "Faith is the substance of things hoped for, the evidence of things not seen. Neville: faith is assumption.", "concept": "Faith bukan harapan — tapi asumsi yang luhur", "source": "Neville Goddard - Your Faith is Your Fortune"},
        {"topic": "The Promise (Janji Neville)", "quote": "The Promise is this: that if you persist in your assumption, it will harden into fact.", "concept": "The Promise Neville Goddard — asumsi jadi fakta dalam 3 hari", "source": "Neville Goddard - The Law and the Promise"},

        # Advanced Techniques
        {"topic": "Ladder Technique", "quote": "Every night, imagine climbing a ladder. With each rung, you move closer to the wish fulfilled.", "concept": "Tangga SATS — teknik klimbing untuk masuk state", "source": "Neville Goddard adaptation"},
        {"topic": "I AM Meditation", "quote": "I AM meditating... I AM the wish fulfilled, and it is done.", "concept": "Meditasi I AM — afirmasi kesadaran tertinggi", "source": "Neville Goddard - The Power of Awareness"},
        {"topic": "Theater of the Mind", "quote": "Construct a small scene that implies the wish fulfilled. Live in it. Repeat until real.", "concept": "Teater mental — skena kecil yang mengindikasikan tercapai", "source": "Neville Goddard - Resurrection"},
        {"topic": "Revision Tonight", "quote": "Tonight, before sleep, revise today. Make every scene match your ideal.", "concept": "Revisi harian malam — rewrite realitas", "source": "Neville Goddard - Givingness"},

        # Free PDF Content
        {"topic": "Feeling is the Secret (Free Ebook)", "quote": "Feeling is the secret — not words, not techniques, but the feeling of the wish fulfilled.", "concept": "Summary Feeling is the Secret untuk sosial media", "source": "Free PDF"},
        {"topic": "7 Hari Ketenangan Manifestasi", "quote": "7 hari untuk membangun keheningan mental yang menjadi media manifestasi.", "concept": "Panduan 7 hari ketenangan dalam praktik Hukum Asumsi", "source": "Free PDF"},
        {"topic": "Satu Satunya Sumber Pencerahan", "quote": "Kamu adalah sumber pencerahan. Bukan dunia, bukan orang lain.", "concept": "Self-sufficiency dalam pencarian kesadaran", "source": "Free PDF"},
        {"topic": "Menyembuhkan Inner Child", "quote": "Setiap asumsi buruk berakar dari inner child yang terluka.", "concept": "Koneksi inner child dengan kesalahan manifestasi", "source": "Free PDF"},

        # Business/Angle for NEVGO
        {"topic": "NEVGO Pure Teaching", "quote": "Kami bukan teknik — kami ajarkan Kesadaran Identitas.", "concept": "Diferensiasi NEVGO: teknik vs kesadaran", "source": "NEVGO Brand"},
        {"topic": "Why Most Fail at Manifestation", "quote": "Bukan karena tekniknya salah — tapi identitas kesadaran yang belum bergeser.", "concept": "Pendekatan NEVGO vs kompetitor", "source": "NEVGO Strategy"},
    ]

    if existing > 0:
        print(f"Content pool sudah ada ({existing} entries). Skipping seed.")
        return

    tags_map = {
        "Law of Assumption Fundamentals": ["fundamental", "law-of-assumption", "core"],
        "SATS (State Akin To Sleep)": ["technique", "sats", "manifestation"],
        "Living in the End": ["fundamental", "state", "end"],
        "Revision Technique": ["technique", "revision", "night"],
        "Mental Diet": ["daily-practice", "mental", "awareness"],
        "Feeling is the Secret": ["core", "feeling", "secret"],
        "Bridge of Events": ["advanced", "bridge", "process"],
        "Identity & Consciousness Shift": ["advanced", "identity", "consciousness"],
        "Kesalahan Fatal dalam Manifestasi": ["mistakes", "education", "awareness"],
    }

    for item in pool:
        tags = tags_map.get(item["topic"], ["general"])
        item["tags"] = ",".join(tags)
        db.execute(
            "INSERT INTO content_pool (topic, quote, concept, source, tags) VALUES (?, ?, ?, ?, ?)",
            (item["topic"], item["quote"], item["concept"], item["source"], item["tags"])
        )

    print(f"✓ Content pool seeded dengan {len(pool)} topik dari Neville Goddard.")


def cmd_generate(args):
    """Generate content from a topic."""
    from modules.generation.caption_gen import CaptionGenerator
    from modules.generation.tones import apply_tone

    topic = args.topic
    tone_val = args.tone or "edukatif"
    platform = args.platform or "instagram"
    content_type = args.type or "carousel"

    gen = CaptionGenerator(topic=topic, tone=tone_val, platform=platform)

    if content_type == "caption":
        result = gen.caption()
    elif content_type == "carousel":
        result = gen.carousel_caption(slides=args.slides or 7)
    elif content_type == "reels":
        result = gen.reels_script(duration=args.duration or 60)
    elif content_type == "quote":
        result = gen.quote_caption()
    elif content_type == "email":
        result = gen.email(day=args.day or 1)
    else:
        result = gen.caption()

    db = FactoryDB()
    item = ContentItem(
        type=ContentType(content_type),
        topic=topic,
        tone=Tone(tone_val),
        caption=result.get("caption", ""),
        hashtags=result.get("hashtags", []),
        title=result.get("title", ""),
        body=result.get("body", ""),
    )
    db.insert_content(item.db_row())

    print(f"\n{'='*55}")
    print(f"  GENERATED: {content_type.upper()} — {topic}")
    print(f"  ID: {item.content_id}")
    print(f"  Tone: {tone_val} | Platform: {platform}")
    print(f"{'='*55}")
    if result.get("title"):
        print(f"\n  TITLE: {result['title']}")
    if result.get("body"):
        print(f"\n  BODY:\n{result['body']}")
    print(f"\n  CAPTION:\n{result['caption']}")
    if result.get("hashtags"):
        print(f"\n  HASHTAGS: {' '.join(result['hashtags'])}")
    if result.get("cta"):
        print(f"\n  CTA: {result['cta']}")
    if result.get("slides"):
        print(f"\n  SLIDES ({len(result['slides'])}):")
        for i, slide in enumerate(result["slides"], 1):
            print(f"    {i}. {slide}")
    print(f"\n  Status: DRAFT (approve: factory curate approve {item.content_id})")
    print()


def cmd_curate(args):
    """Content curation and approval."""
    db = FactoryDB()

    if args.action == "preview":
        status = args.status or "draft"
        rows = db.query("SELECT content_id, type, topic, status, status, created_at, substr(caption, 1, 60) as preview FROM content WHERE status = ? ORDER BY created_at DESC LIMIT 20", [status])
        if not rows:
            print(f"Tidak ada content dengan status '{status}'.")
            return
        print(f"\n{'='*70}")
        print(f"  CURATION — {status.upper()} ({len(rows)} items)")
        print(f"{'='*70}")
        print(f"  {'ID':<14} {'Type':<14} {'Topic':<25} {'Preview'}")
        print(f"  {'-'*66}")
        for r in rows:
            print(f"  {r['content_id']:<14} {r['type']:<14} {r['topic'][:23]:<25} {r['preview']}...")
        print()

    elif args.action == "approve":
        content_id = args.id
        row = db.query("SELECT * FROM content WHERE content_id = ?", [content_id])
        if not row:
            print(f"Content '{content_id}' tidak ditemukan.")
            return
        db.update_content(content_id, {"status": "approved"})
        print(f"✓ Content '{content_id}' — {row[0]['topic']} — APPROVED")

    elif args.action == "reject":
        content_id = args.id
        db.update_content(content_id, {"status": "draft"})
        print(f"✓ Content '{content_id}' — REJECTED (back to draft)")

    elif args.action == "edit":
        content_id = args.id
        field = args.field or "caption"
        value = args.value or input(f"New {field}: ")
        db.update_content(content_id, {field: value})
        db.insert_version(content_id, 99, **{field: value})
        print(f"✓ Content '{content_id}' — {field} updated")


def cmd_batch(args):
    """Run a batch generation from a brief."""
    from modules.generation.caption_gen import CaptionGenerator
    from modules.generation.batch import BatchRunner

    brief = args.brief or "weekly content plan"
    count = args.count or 5

    runner = BatchRunner(brief=brief, count=count)
    items = runner.run()
    db = FactoryDB()

    print(f"\n{'='*60}")
    print(f"  BATCH RUN — '{brief}'")
    print(f"  Generated: {len(items)} content pieces")
    print(f"{'='*60}\n")

    for i, item in enumerate(items, 1):
        db.insert_content(item.db_row())
        print(f"  [{i}/{len(items)}] {item.type.value:<14} {item.topic[:40]}")
        print(f"           ID: {item.content_id}")

    print(f"\n  ✓ Semua content disimpan sebagai DRAFT.")
    print(f"  Review: factory curate preview")
    print(f"  Approve all: factory curate approve <id>")
    print()


def cmd_schedule(args):
    """Content scheduling."""
    db = FactoryDB()

    if args.action == "calendar":
        today = datetime.now().strftime("%Y-%m-%d")
        rows = db.query("""
            SELECT s.id, s.scheduled_at, s.status, c.content_id, c.type, c.topic
            FROM schedule s JOIN content c ON s.content_id = c.content_id
            WHERE date(s.scheduled_at) >= ?
            ORDER BY s.scheduled_at
        """, [today])
        if not rows:
            print("Tidak ada jadwal mendatang. Jalankan: factory schedule plan")
            return
        print(f"\n{'='*70}")
        print(f"  CONTENT CALENDAR")
        print(f"{'='*70}")
        print(f"  {'Date':<12} {'Time':<8} {'Status':<12} {'Type':<12} {'Topic'}")
        print(f"  {'-'*62}")
        for r in rows:
            dt = r["scheduled_at"][:16] if r["scheduled_at"] else "N/A"
            print(f"  {dt:<20} {r['status']:<12} {r['type']:<12} {r['topic'][:35]}")
        print()

    elif args.action == "add":
        content_id = args.id
        day = args.day or "tomorrow"
        time_val = args.time or "19:00"
        if day == "tomorrow":
            dt = datetime.now() + timedelta(days=1)
        else:
            day_map = {"senin": 0, "selasa": 1, "rabu": 2, "kamis": 3, "jumat": 4, "sabtu": 5, "minggu": 6}
            target = day_map.get(day.lower(), 0)
            today_w = datetime.now().weekday()
            diff = (target - today_w) % 7
            dt = datetime.now() + timedelta(days=diff)
        scheduled = dt.strftime(f"%Y-%m-%d {time_val}:00")
        row = db.query("SELECT * FROM content WHERE content_id = ?", [content_id])
        if not row:
            print(f"Content '{content_id}' tidak ditemukan.")
            return
        db.execute("INSERT INTO schedule (content_id, scheduled_at, platform) VALUES (?, ?, ?)",
                    (content_id, scheduled, "instagram"))
        print(f"✓ Scheduled: {row[0]['topic']} → {scheduled}")

    elif args.action == "plan":
        days = args.days or 7
        approved = db.query("SELECT * FROM content WHERE status = 'approved' ORDER BY updated_at DESC LIMIT ?", [days * 2])
        available = db.query("SELECT * FROM content WHERE status = 'draft' ORDER BY created_at DESC LIMIT ?", [days])
        pool = approved + available
        if not pool:
            print("Tidak ada content available. Generate dulu dengan factory generate atau factory batch.")
            return

        print(f"\n{'='*60}")
        print(f"  AUTO SCHEDULE PLAN — {days} HARI KE DEPAN")
        print(f"{'='*60}\n")
        slots = ["07:00", "12:00", "19:00"]
        content_idx = 0
        for d_offset in range(days):
            date = datetime.now() + timedelta(days=d_offset)
            day_name = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][date.weekday()]
            print(f"  📅 {day_name}, {date.strftime('%d %b %Y')}")
            for t in slots:
                if content_idx < len(pool):
                    c = pool[content_idx]
                    print(f"     {t}  →  [{c['type']:<14}] {c['topic'][:40]}")
                    content_idx += 1
                else:
                    print(f"     {t}  →  (kosong)")
            print()


def cmd_analytics(args):
    """Instagram analytics via Apify."""
    if args.action == "pull":
        print("  Pulling Instagram data via Apify...")
        from modules.analytics.tracker import AnalyticsTracker
        tracker = AnalyticsTracker()
        data = tracker.pull_data(username="nevgoinstitute", results_limit=50)
        db = FactoryDB()
        db.execute("""INSERT INTO analytics (date, followers, following, posts_count, avg_likes, avg_comments, engagement_rate)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (datetime.now().strftime("%Y-%m-%d"),
                     data.get("followers", 0), data.get("following", 0), data.get("posts_count", 0),
                     data.get("avg_likes", 0), data.get("avg_comments", 0), data.get("engagement_rate", 0)))
        for p in data.get("posts", []):
            db.execute("""INSERT INTO post_analytics (post_shortcode, likes, comments, post_type, timestamp)
                           VALUES (?, ?, ?, ?, ?)""",
                        (p.get("shortcode", ""), p.get("likes", 0), p.get("comments", 0),
                         p.get("type", ""), p.get("timestamp", "")))
        print(f"  ✓ Data berhasil disimpan ke database.")
        print(f"  Followers: {data.get('followers', 0)} | Posts: {data.get('posts_count', 0)}")
        print(f"  Avg Likes: {data.get('avg_likes', 0):.1f} | Avg Comments: {data.get('avg_comments', 0):.1f}")

    elif args.action == "report":
        db = FactoryDB()
        rows = db.query("""
            SELECT * FROM analytics ORDER BY date DESC LIMIT 1""")
        if not rows:
            print("Belum ada data analytics. Jalankan: factory analytics pull")
            return
        snap = rows[0]
        recent = db.query("""SELECT * FROM post_analytics ORDER BY captured_at DESC LIMIT 10""")
        print(f"\n{'='*55}")
        print(f"  ANALYTICS REPORT — {snap.get('date', 'N/A')}")
        print(f"{'='*55}")
        print(f"  Followers:        {snap.get('followers', 0)}")
        print(f"  Following:        {snap.get('following', 0)}")
        print(f"  Posts:            {snap.get('posts_count', 0)}")
        print(f"  Avg Likes:        {snap.get('avg_likes', 0):.1f}")
        print(f"  Avg Comments:     {snap.get('avg_comments', 0):.1f}")
        print(f"  Engagement Rate:  {snap.get('engagement_rate', 0):.2f}%")
        if recent:
            print(f"\n  RECENT POSTS (top 5 by likes):")
            top = sorted(recent, key=lambda x: x.get("likes") or 0, reverse=True)[:5]
            for i, p in enumerate(top, 1):
                print(f"    {i}. {p.get('post_shortcode', '?'):<14} {p.get('type', '?'):<10} ❤️{p.get('likes', 0)} 💬{p.get('comments', 0)}")
        print()

    elif args.action == "insights":
        from modules.analytics.insights import InsightsEngine
        engine = InsightsEngine()
        insights = engine.analyze()
        if not insights:
            print("Belum cukup data. Pull beberapa kali dulu: factory analytics pull")
            return
        print(f"\n{'='*55}")
        print(f"  CONTENT INSIGHTS")
        print(f"{'='*55}")
        print(f"\n  🏆 Top topics yang paling engaged:")
        for i, item in enumerate(insights.get("top_topics", [])[:5], 1):
            print(f"     {i}. {item['topic']:<35} avg ❤️{item['avg_likes']:.1f}")
        print(f"\n  📊 Format yang paling works:")
        for i, item in enumerate(insights.get("best_formats", [])[:3], 1):
            print(f"     {i}. {item['format']:<15} avg ❤️{item['avg_likes']:.1f}")
        print(f"\n  ⏰ Best slot kosong untuk feed back:")
        for f in insights.get("feedback_actions", []):
            print(f"     → {f}")
        print()


def cmd_list(args):
    """List all content."""
    db = FactoryDB()
    status_filter = args.status if args.status else None
    if status_filter:
        rows = db.query("SELECT content_id, type, topic, status, created_at FROM content WHERE status = ? ORDER BY created_at DESC", [status_filter])
    else:
        rows = db.query("SELECT content_id, type, topic, status, created_at FROM content ORDER BY created_at DESC LIMIT 30")

    if not rows:
        print("Belum ada content. Generate dengan: factory generate --topic <topik>")
        return

    print(f"\n{'='*75}")
    print(f"  ALL CONTENT ({len(rows)} items)")
    print(f"{'='*75}")
    print(f"  {'ID':<14} {'Type':<14} {'Status':<12} {'Topic':<30} {'Date'}")
    print(f"  {'-'*71}")
    for r in rows:
        date = r["created_at"][:10] if r["created_at"] else "N/A"
        print(f"  {r['content_id']:<14} {r['type']:<14} {r['status']:<12} {r['topic'][:28]:<30} {date}")
    print()


def main():
    parser = argparse.ArgumentParser(prog="factory", description="Neville Goddard Content Factory v1.0")
    sub = parser.add_subparsers(dest="command")

    # source
    p_source = sub.add_parser("source", help="Content sourcing")
    source_sub = p_source.add_subparsers(dest="source_action")
    source_sub.add_parser("list", help="List content pool")
    source_sub.add_parser("seed", help="Seed content pool from Neville Goddard materials")

    # generate
    p_gen = sub.add_parser("generate", help="Generate content")
    p_gen.add_argument("--topic", "-t", required=True, help="Content topic")
    p_gen.add_argument("--tone", default="edukatif", help="Tone: edukatif, motivational, conversational, authority, soft_sell")
    p_gen.add_argument("--platform", default="instagram", help="Platform: instagram, tiktok")
    p_gen.add_argument("--type", default="carousel", help="Type: carousel, quote, reels, caption, email")
    p_gen.add_argument("--slides", type=int, default=7, help="Number of carousel slides")
    p_gen.add_argument("--duration", type=int, default=60, help="Reels duration in seconds")
    p_gen.add_argument("--day", type=int, default=1, help="Email nurture day (1-7)")

    # batch
    p_batch = sub.add_parser("batch", help="Batch generation")
    p_batch.add_argument("--brief", "-b", help="Content brief (e.g. 'Jumat: edukasi manifestasi')")
    p_batch.add_argument("--count", "-c", type=int, default=5, help="Number of content to generate")

    # curate
    p_curate = sub.add_parser("curate", help="Curation & review")
    curate_sub = p_curate.add_subparsers(dest="action")
    p_preview = curate_sub.add_parser("preview", help="Preview pending content")
    p_preview.add_argument("--status", default="draft")
    p_approve = curate_sub.add_parser("approve", help="Approve content")
    p_approve.add_argument("id", help="Content ID")
    p_reject = curate_sub.add_parser("reject", help="Reject content")
    p_reject.add_argument("id", help="Content ID")
    p_edit = curate_sub.add_parser("edit", help="Edit content")
    p_edit.add_argument("id", help="Content ID")
    p_edit.add_argument("--field", default="caption")
    p_edit.add_argument("--value", help="New value")

    # schedule
    p_sched = sub.add_parser("schedule", help="Scheduling")
    sched_sub = p_sched.add_subparsers(dest="action")
    sched_sub.add_parser("calendar", help="View content calendar")
    p_add = sched_sub.add_parser("add", help="Add content to schedule")
    p_add.add_argument("id", help="Content ID")
    p_add.add_argument("--day", help="Day: senin-sabtu, atau tomorrow")
    p_add.add_argument("--time", default="19:00", help="Time HH:MM")
    p_plan = sched_sub.add_parser("plan", help="Auto plan upcoming days")
    p_plan.add_argument("--days", type=int, default=7)

    # analytics
    p_analytics = sub.add_parser("analytics", help="Instagram analytics")
    analytics_sub = p_analytics.add_subparsers(dest="action")
    analytics_sub.add_parser("pull", help="Pull Instagram data via Apify")
    analytics_sub.add_parser("report", help="Generate report")
    analytics_sub.add_parser("insights", help="Content insights & feedback")

    # list
    p_list = sub.add_parser("list", help="List all content")
    p_list.add_argument("--status", help="Filter by status")

    args = parser.parse_args()

    cmd_map = {
        "source": lambda a=args: cmd_source_list(a) if a.source_action == "list"
                         else cmd_source_seed(a) if a.source_action == "seed"
                         else p_source.print_help(),
        "generate": lambda a=args: cmd_generate(a),
        "batch": lambda a=args: cmd_batch(a),
        "curate": lambda a=args: cmd_curate(a),
        "schedule": lambda a=args: cmd_schedule(a),
        "analytics": lambda a=args: cmd_analytics(a),
        "list": lambda a=args: cmd_list(a),
    }

    if args.command in cmd_map:
        cmd_map[args.command]()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
