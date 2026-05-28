#!/usr/bin/env python3
"""NEVGO Content Factory — Flask Web Dashboard v2.0."""

import os
import sys
import json
from pathlib import Path
from functools import wraps

from flask import Flask, render_template, request, redirect, flash, url_for, send_file, abort
import yaml

sys.path.insert(0, str(Path(__file__).parent))

from core.db import FactoryDB
from core.schemas import ContentItem, ContentType, Tone
from modules.generation.caption_gen import CaptionGenerator


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "nevgoinstitute-dev-secret-change-in-prod")

OUTPUT_DIR = Path(__file__).parent / "output" / "images"


def load_cfg():
    base = Path(__file__).parent
    for name in ("config.local.yaml", "config.yaml"):
        p = base / name
        if p.exists():
            with open(p) as f:
                return yaml.safe_load(f) or {}
    return {}


def _db():
    db_path = Path(__file__).parent / "data" / "factory.db"
    return FactoryDB(str(db_path))


# ---------------------------------------------------------------- routes ---

@app.route("/")
def dashboard():
    db = _db()
    funnel = db.query("SELECT status, COUNT(*) as count FROM content GROUP BY status ORDER BY status")
    recent = db.query("SELECT content_id, type, topic, status, created_at FROM content ORDER BY created_at DESC LIMIT 10")
    schedule = db.query("""
        SELECT s.scheduled_at, s.status, c.content_id, c.topic, c.type
        FROM schedule s JOIN content c ON s.content_id = c.content_id
        WHERE date(s.scheduled_at) >= date('now')
        ORDER BY s.scheduled_at LIMIT 10
    """)
    analytic = db.query("SELECT * FROM analytics ORDER BY date DESC LIMIT 1")
    return render_template("dashboard.html",
                           funnel=funnel,
                           recent=recent,
                           schedule=schedule,
                           analytics=analytic[0] if analytic else None)


@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        tone = request.form.get("tone", "edukatif")
        fmt = request.form.get("type", "carousel")
        platform = request.form.get("platform", "instagram")
        with_image = request.form.get("with_image") == "1"
        if not topic:
            flash("Topic is required", "error")
            return render_template("generate.html")

        gen = CaptionGenerator(topic=topic, tone=tone, platform=platform)
        dispatch = {
            "caption": gen.caption,
            "quote": gen.quote_caption,
            "carousel": lambda: gen.carousel_caption(slides=7),
            "reels": lambda: gen.reels_script(duration=60),
            "email": lambda: gen.email(day=1),
        }
        fn = dispatch.get(fmt, gen.caption)
        result = fn()

        db = _db()
        item = ContentItem(
            type=ContentType(fmt) if fmt != "quote" else ContentType.QUOTE_CARD,
            topic=topic,
            tone=Tone(tone),
            caption=result.get("caption", ""),
            hashtags=result.get("hashtags", []),
            title=result.get("title", ""),
            body=result.get("slides", []),
        )
        db.insert_content(item.db_row())
        image_path = None

        if with_image:
            from modules.visual.renderer import VisualGenerator
            vg = VisualGenerator(brand_cfg=load_cfg().get("brand", {}))
            try:
                if fmt in ("quote",):
                    image_path = vg.render_quote_card(
                        quote_text=result.get("title", topic),
                        topic=topic,
                        content_id=item.content_id,
                    )
                elif fmt == "carousel" and result.get("slides"):
                    slides = [{"title": s, "body": ""} for s in result["slides"]]
                    paths = vg.render_carousel_slides(
                        slides=slides, topic=topic, content_id=item.content_id
                    )
                    image_path = paths[0] if paths else None
                else:
                    image_path = vg.render_story(
                        headline=topic, subtext=result.get("caption", "")[:200],
                        cta="Follow @nevgoinstitute", content_id=item.content_id
                    )
                flash(f"✓ Content generated: {item.content_id}", "success")
                if image_path:
                    flash(f"✓ Image: {Path(image_path).name}", "success")
            except Exception as e:
                flash(f"Image generation failed: {e}", "error")

        return render_template("generate.html", result=result, image_path=image_path, topic=topic)
    return render_template("generate.html")


@app.route("/content")
def content_list():
    db = _db()
    status = request.args.get("status")
    if status:
        rows = db.query("SELECT * FROM content WHERE status = ? ORDER BY created_at DESC LIMIT 50", [status])
    else:
        rows = db.query("SELECT * FROM content ORDER BY created_at DESC LIMIT 50")
    return render_template("content_list.html", items=rows)


@app.route("/content/<cid>/approve", methods=["POST"])
def approve(cid):
    db = _db()
    db.update_content(cid, {"status": "approved"})
    flash(f"✓ {cid[:8]} approved", "success")
    return redirect(url_for("content_list"))


@app.route("/content/<cid>/reject", methods=["POST"])
def reject(cid):
    db = _db()
    db.update_content(cid, {"status": "draft"})
    flash(f"↺ {cid[:8]} rejected (back to draft)", "success")
    return redirect(url_for("content_list"))


@app.route("/repurpose/<cid>", methods=["GET", "POST"])
def repurpose(cid):
    db = _db()
    row = db.query("SELECT * FROM content WHERE content_id = ?", [cid])
    if not row:
        abort(404)
    content = row[0]
    result = None
    result_text = ""

    if request.method == "POST":
        from modules.repurpose.adapter import Repurposer
        rep = Repurposer(content)
        fmt = request.form.get("format", "all")
        dispatch = {
            "all": rep.to_all,
            "quote_cards": rep.to_quote_cards,
            "reels": rep.to_reels_script,
            "blog": rep.to_blog,
            "email": rep.to_email,
            "twitter": rep.to_thread,
            "story": rep.to_story_series,
        }
        fn = dispatch.get(fmt)
        if fn:
            result = fn()
            result_text = json.dumps(result, indent=2, ensure_ascii=False) if isinstance(result, (dict, list)) else str(result)
            flash(f"✓ Content adapted to {fmt}", "success")
    return render_template("repurpose.html", content=content, result=result, result_text=result_text)


@app.route("/schedule", methods=["GET", "POST"])
def schedule_view():
    db = _db()
    scheduled = db.query("""
        SELECT s.scheduled_at, s.status, c.content_id, c.topic, c.type
        FROM schedule s JOIN content c ON s.content_id = c.content_id
        WHERE date(s.scheduled_at) >= date('now')
        ORDER BY s.scheduled_at
    """)
    pending = db.query("SELECT content_id, topic, tone, status FROM content WHERE status IN ('approved','draft') ORDER BY updated_at DESC LIMIT 20")
    return render_template("schedule.html", schedule=scheduled, pending=pending)


@app.route("/schedule/add", methods=["POST"])
def schedule_add():
    db = _db()
    cid = request.form.get("content_id", "").strip()
    date_str = request.form.get("date", "").strip()
    time_str = request.form.get("time", "19:00").strip()
    if not cid or not date_str:
        flash("Content ID and date required", "error")
        return redirect(url_for("schedule_view"))
    scheduled_at = f"{date_str} {time_str}:00"
    db.execute("INSERT INTO schedule (content_id, scheduled_at, platform) VALUES (?, ?, ?)",
               (cid, scheduled_at, "instagram"))
    flash(f"✓ {cid[:8]} scheduled for {scheduled_at}", "success")
    return redirect(url_for("schedule_view"))


@app.route("/analytics")
def analytics_view():
    db = _db()
    rows = db.query("SELECT * FROM analytics ORDER BY date DESC LIMIT 1")
    latest = rows[0] if rows else None
    recent_posts = db.query("SELECT * FROM post_analytics ORDER BY captured_at DESC LIMIT 20")
    return render_template("analytics.html", latest=latest, recent_posts=recent_posts)


@app.route("/images")
def images_gallery():
    images = []
    if OUTPUT_DIR.exists():
        for p in sorted(OUTPUT_DIR.iterdir()):
            if p.suffix.lower() in (".jpg", "jpeg", "png", "webp"):
                images.append({
                    "path": str(p),
                    "name": p.name,
                    "size": f"{p.stat().st_size // 1024} KB",
                })
    return render_template("images.html", images=images)


@app.route("/images/file")
def images_file():
    path = request.args.get("path", "")
    if not path:
        abort(404)
    safe = Path(path).resolve()
    if not str(safe).startswith(str(OUTPUT_DIR.resolve())):
        abort(403)
    if not safe.exists():
        abort(404)
    return send_file(str(safe), mimetype="image/jpeg")


# ------------------------------------------------------------- main ---

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
