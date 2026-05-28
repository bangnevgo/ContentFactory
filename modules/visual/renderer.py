"""Visual image generation — render HTML templates to JPG via Playwright."""

import os
import sys
import json
import textwrap
import tempfile
from datetime import datetime
from pathlib import Path


class VisualGenerator:
    """Generate branded images (quote cards, carousel slides, stories) as JPG."""

    BRAND = {
        "name": "NEVGO Institute",
        "username": "@nevgoinstitute",
        "primary_color": "#1a1a2e",
        "accent_color": "#e94560",
        "website": "nevgoinstitute.com",
    }

    SIZES = {
        "quote_card": (1080, 1080),
        "carousel": (1080, 1080),
        "story": (1080, 1920),
    }

    def __init__(self, brand_cfg=None, output_dir=None):
        cfg = brand_cfg or {}
        merged = {**self._brand}
        for k, v in cfg.items():
            if k in merged:
                merged[k] = v
        self._brand = merged
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parent.parent.parent / "output" / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        tpl_dir = Path(__file__).resolve().parent / "templates"
        _ensure_templates(tpl_dir)
        self.tpl_dir = tpl_dir

    # ------------------------------------------------------------------ API ---

    def render_quote_card(self, quote_text, topic, bg_color=None, content_id=None):
        """Render a single quote card JPG. Returns path."""
        cid = content_id or _new_id()
        size = self.SIZES["quote_card"]
        rendered = _render_quote_html(
            tpl_dir=self.tpl_dir,
            quote_text=quote_text,
            topic=topic,
            bg_color=bg_color or self._brand["primary_color"],
            brand=self._brand,
        )
        out = str(self.output_dir / f"{cid}_quote_card.jpg")
        _playwright_screenshot(rendered, out, out_w=size[0], out_h=size[1])
        return out

    def render_carousel_slides(self, slides, topic="", content_id=None):
        """Render each slide in *slides* as a separate JPG. Returns [paths]."""
        cid = content_id or _new_id()
        paths = []
        for i, slide in enumerate(slides, 1):
            rendered = _render_carousel_html(
                tpl_dir=self.tpl_dir,
                slide_number=i,
                total=len(slides),
                title=slide.get("title", ""),
                body=slide.get("body", ""),
                topic=topic,
                brand=self._brand,
            )
            out = str(self.output_dir / f"{cid}_carousel_{i:02d}.jpg")
            _playwright_screenshot(rendered, out, **dict(zip(("out_w", "out_h"), self.SIZES["carousel"])))
            paths.append(out)
        return paths

    def render_story(self, headline, subtext, cta, content_id=None):
        """Render a Story-sized image. Returns path."""
        cid = content_id or _new_id()
        rendered = _render_story_html(
            tpl_dir=self.tpl_dir,
            headline=headline,
            subtext=subtext,
            cta=cta,
            brand=self._brand,
        )
        out = str(self.output_dir / f"{cid}_story.jpg")
        _playwright_screenshot(rendered, out, **dict(zip(("out_w", "out_h"), self.SIZES["story"])))
        return out


# ------------------------------------------------------------- templates ---

def _ensure_templates(tpl_dir):
    tpl_dir.mkdir(parents=True, exist_ok=True)
    _write_if_missing(tpl_dir / "quote_card.html", _QUOTE_CARD_TPL)
    _write_if_missing(tpl_dir / "carousel_slide.html", _CAROUSEL_TPL)
    _write_if_missing(tpl_dir / "story.html", _STORY_TPL)


def _write_if_missing(path, content):
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def _render_quote_html(tpl_dir, quote_text, topic, bg_color, brand):
    html = (tpl_dir / "quote_card.html").read_text(encoding="utf-8")
    html = (html
            .replace("{{BG_COLOR}}", bg_color)
            .replace("{{PRIMARY_COLOR}}", brand.get("primary_color", "#1a1a2e"))
            .replace("{{ACCENT_COLOR}}", brand.get("accent_color", "#e94560"))
            .replace("{{QUOTE}}", _esc(quote_text))
            .replace("{{TOPIC}}", _esc(topic))
            .replace("{{USERNAME}}", _esc(brand.get("username", "")))
            .replace("{{BRAND_NAME}}", _esc(brand.get("name", ""))))
    return html


def _render_carousel_html(tpl_dir, slide_number, total, title, body, topic, brand):
    html = (tpl_dir / "carousel_slide.html").read_text(encoding="utf-8")
    body_html = "".join(
        f"<p>{_esc(line)}</p>" for line in body.splitlines() if line.strip()
    ) or f"<p>{_esc(body)}</p>"
    html = (html
            .replace("{{PRIMARY_COLOR}}", brand.get("primary_color", "#1a1a2e"))
            .replace("{{ACCENT_COLOR}}", brand.get("accent_color", "#e94560"))
            .replace("{{TITLE}}", _esc(title))
            .replace("{{BODY_HTML}}", body_html)
            .replace("{{TOPIC}}", _esc(topic))
            .replace("{{SLIDE_NUM}}", str(slide_number))
            .replace("{{TOTAL}}", str(total))
            .replace("{{USERNAME}}", _esc(brand.get("username", "")))
            .replace("{{BRAND_NAME}}", _esc(brand.get("name", ""))))
    return html


def _render_story_html(tpl_dir, headline, subtext, cta, brand):
    html = (tpl_dir / "story.html").read_text(encoding="utf-8")
    html = (html
            .replace("{{PRIMARY_COLOR}}", brand.get("primary_color", "#1a1a2e"))
            .replace("{{ACCENT_COLOR}}", brand.get("accent_color", "#e94560"))
            .replace("{{HEADLINE}}", _esc(headline))
            .replace("{{SUBTEXT}}", _esc(subtext))
            .replace("{{CTA}}", _esc(cta))
            .replace("{{USERNAME}}", _esc(brand.get("username", "")))
            .replace("{{BRAND_NAME}}", _esc(brand.get("name", ""))))
    return html


def _esc(text):
    text = str(text)
    for old, new in [("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ('"', "&quot;")]:
        text = text.replace(old, new)
    return text


# ---------------------------------------------------------- playwright ---

def _playwright_screenshot(html_content, out_path, out_w=1080, out_h=1080):
    """Render HTML string via Playwright headless Chromium → JPG."""
    from playwright.sync_api import sync_playwright
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fp:
        fp.write(html_content)
        tmp_path = fp.name
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": out_w, "height": out_h})
            page.goto(f"file://{tmp_path}", wait_until="networkidle")
            page.screenshot(path=out_path, type="jpeg", quality=90)
            browser.close()
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------- utils ---

def _new_id():
    from datetime import timezone
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    import random
    return f"{ts}{random.randint(1000, 9999)}"


# --------------------------------------------------------- HTML templates ---

_QUOTE_CARD_TPL = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1080px; height: 1080px;
    background: linear-gradient(135deg, {{BG_COLOR}} 0%, #16213e 50%, {{ACCENT_COLOR}}33 100%);
    font-family: 'Georgia', 'Times New Roman', serif;
    color: #ffffff;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 80px;
    position: relative;
  }
  .quote-mark {
    font-size: 120px; line-height: 1;
    color: {{ACCENT_COLOR}}; opacity: 0.7;
    font-family: Georgia, serif;
    margin-bottom: -30px;
  }
  .quote {
    font-size: 42px; line-height: 1.5; text-align: center;
    max-width: 900px; margin: 30px 0;
    font-style: italic;
  }
  .divider {
    width: 120px; height: 3px;
    background: {{ACCENT_COLOR}}; margin: 30px auto;
    border-radius: 2px;
  }
  .topic {
    font-size: 24px; letter-spacing: 2px;
    color: {{ACCENT_COLOR}}; text-transform: uppercase;
    margin-bottom: 10px;
  }
  .brand {
    position: absolute; bottom: 40px; right: 60px;
    font-size: 22px; color: rgba(255,255,255,0.8);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 1px;
  }
  .brand small { display: block; font-size: 14px; opacity: 0.6; text-align: right; }
</style>
</head>
<body>
  <div class="topic">{{TOPIC}}</div>
  <div class="quote-mark">"</div>
  <div class="quote">{{QUOTE}}</div>
  <div class="divider"></div>
  <div class="brand">
    {{USERNAME}}
    <small>{{BRAND_NAME}}</small>
  </div>
</body>
</html>"""


_CAROUSEL_TPL = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1080px; height: 1080px;
    background: linear-gradient(160deg, #0f0f23 0%, {{PRIMARY_COLOR}} 100%);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #ffffff;
    display: flex; flex-direction: column;
    justify-content: center;
    padding: 80px 90px;
    position: relative;
  }
  .slide-badge {
    position: absolute; top: 40px; right: 50px;
    background: {{ACCENT_COLOR}}; color: #fff;
    padding: 8px 22px; border-radius: 30px;
    font-size: 20px; font-weight: bold; letter-spacing: 1px;
  }
  .topic {
    font-size: 22px; letter-spacing: 2px;
    color: {{ACCENT_COLOR}}; text-transform: uppercase;
    margin-bottom: 20px;
  }
  h1 {
    font-size: 60px; line-height: 1.2;
    margin-bottom: 35px;
    background: linear-gradient(90deg, #fff 0%, {{ACCENT_COLOR}} 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .body p {
    font-size: 30px; line-height: 1.7; margin-bottom: 20px;
    color: rgba(255,255,255,0.88);
  }
  .brand {
    position: absolute; bottom: 40px; right: 60px;
    font-size: 22px; color: rgba(255,255,255,0.7);
    font-weight: bold; letter-spacing: 1px;
  }
  .brand small { display: block; font-size: 14px; opacity: 0.5; text-align: right; }
</style>
</head>
<body>
  <div class="slide-badge">{{SLIDE_NUM}} / {{TOTAL}}</div>
  <div class="topic">{{TOPIC}}</div>
  <h1>{{TITLE}}</h1>
  <div class="body">
    {{BODY_HTML}}
  </div>
  <div class="brand">
    {{USERNAME}}
    <small>{{BRAND_NAME}}</small>
  </div>
</body>
</html>"""


_STORY_TPL = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1080px; height: 1920px;
    background: linear-gradient(180deg, {{ACCENT_COLOR}} 0%, {{PRIMARY_COLOR}} 40%, #0a0a1a 100%);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #ffffff;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 120px 80px;
    text-align: center;
    position: relative;
  }
  .accent-bar {
    width: 80px; height: 5px; background: #fff;
    border-radius: 3px; margin-bottom: 50px;
  }
  h1 {
    font-size: 88px; line-height: 1.15;
    margin-bottom: 40px;
    text-shadow: 0 4px 30px rgba(0,0,0,0.4);
  }
  .sub {
    font-size: 40px; line-height: 1.6; max-width: 860px;
    color: rgba(255,255,255,0.85); margin-bottom: 80px;
  }
  .cta {
    background: {{ACCENT_COLOR}}; color: #fff;
    padding: 24px 60px; border-radius: 60px;
    font-size: 28px; font-weight: bold; letter-spacing: 2px;
    display: inline-block;
    box-shadow: 0 8px 30px rgba(233,69,96,0.4);
  }
  .brand {
    position: absolute; bottom: 60px; left: 0; right: 0;
    text-align: center;
    font-size: 28px; font-weight: bold;
    color: rgba(255,255,255,0.75); letter-spacing: 2px;
  }
  .brand small { display: block; font-size: 16px; opacity: 0.5; margin-top: 4px; font-weight: normal; }
</style>
</head>
<body>
  <div class="accent-bar"></div>
  <h1>{{HEADLINE}}</h1>
  <div class="sub">{{SUBTEXT}}</div>
  <div class="cta">{{CTA}}</div>
  <div class="brand">
    {{USERNAME}}
    <small>{{BRAND_NAME}}</small>
  </div>
</body>
</html>"""
