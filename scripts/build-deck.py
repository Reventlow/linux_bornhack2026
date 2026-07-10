#!/usr/bin/env python3
"""Build the self-contained deck bundle: deck/index.html.

Takes the design-tool source (source/Linux for the Curious.dc.html) and
produces a single offline-capable HTML file:

  * the 28 <section> slides, extracted from the <x-import> mount
  * the helmet <style> block (design tokens + blink keyframes)
  * deck-stage.js inlined (the web component that provides the 1920x1080
    stage, keyboard/tap navigation, thumbnail rail and print-to-PDF)
  * Google Fonts (JetBrains Mono, IBM Plex Sans) downloaded and embedded
    as base64 @font-face rules so the deck works with no network
  * tab title, favicon and an "f" fullscreen toggle wired to the stage's
    presenting mode (mirrors scripts/patch-deck.sh in the sibling repo
    Reventlow/docker_bornhack2026 — here we control the shell, so the
    extras are simply authored into the page)

Usage:  python3 scripts/build-deck.py
Requires network access the first time fonts are fetched; they are cached
in scripts/.fontcache/ afterwards.
"""

import base64
import hashlib
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source" / "Linux for the Curious.dc.html"
STAGE_JS = ROOT / "source" / "deck-stage.js"
OUT = ROOT / "deck" / "index.html"
FONT_CACHE = ROOT / "scripts" / ".fontcache"

TITLE = "Linux for the Curious — BornHack 2026"

GOOGLE_CSS_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=JetBrains+Mono:wght@400;500;700;800"
    "&family=IBM+Plex+Sans:wght@400;500;600"
    "&display=swap"
)
# A modern-browser UA makes Google Fonts serve woff2 with unicode-range
# subsets; we keep only the latin/latin-ext blocks the deck needs.
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
KEEP_SUBSETS = ("latin", "latin-ext")

# Tux-penguin favicon in the deck's matcha palette: green tile (--green),
# ink body, cream belly (--bg), amber beak and feet (--amber). Reads
# clearly down to 16px.
FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<rect width="64" height="64" rx="12" fill="#6b8054"/>'
    '<ellipse cx="32" cy="38" rx="17" ry="20" fill="#2b2b28"/>'
    '<ellipse cx="32" cy="22" rx="12" ry="11" fill="#2b2b28"/>'
    '<ellipse cx="32" cy="42" rx="11" ry="14" fill="#f4f1e8"/>'
    '<circle cx="27.5" cy="20" r="3.4" fill="#f4f1e8"/>'
    '<circle cx="36.5" cy="20" r="3.4" fill="#f4f1e8"/>'
    '<circle cx="28.2" cy="20.6" r="1.6" fill="#2b2b28"/>'
    '<circle cx="35.8" cy="20.6" r="1.6" fill="#2b2b28"/>'
    '<path d="M27 26 L37 26 L32 31 Z" fill="#DE6A41"/>'
    '<ellipse cx="24" cy="57" rx="6.5" ry="3.5" fill="#DE6A41"/>'
    '<ellipse cx="40" cy="57" rx="6.5" ry="3.5" fill="#DE6A41"/></svg>'
)

EXTRAS_JS = """\
    /* Fullscreen <-> presenting mode. deck-stage listens for
       __omelette_presenting on window and hides the thumbnail rail,
       suppresses the nav footer and refits the stage itself. */
    (function () {
      function syncPresenting() {
        window.postMessage(
          { __omelette_presenting: !!document.fullscreenElement }, '*');
      }
      document.addEventListener('fullscreenchange', syncPresenting);

      addEventListener('keydown', function (e) {
        if (e.key !== 'f' && e.key !== 'F') return;
        if (e.ctrlKey || e.metaKey || e.altKey) return;
        /* Don't steal "f" while typing in a form field. */
        var t = e.composedPath ? e.composedPath()[0] : e.target;
        if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA'
                  || t.isContentEditable)) return;
        if (document.fullscreenElement) document.exitFullscreen();
        else document.documentElement.requestFullscreen();
      });
    })();
"""


def fetch(url: str) -> bytes:
    """GET a URL, caching by URL hash so rebuilds work offline."""
    FONT_CACHE.mkdir(exist_ok=True)
    cached = FONT_CACHE / hashlib.sha256(url.encode()).hexdigest()
    if cached.exists():
        return cached.read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=30).read()
    cached.write_bytes(data)
    return data


def inline_fonts() -> str:
    """Download the Google Fonts CSS and embed each woff2 as base64."""
    css = fetch(GOOGLE_CSS_URL).decode()
    blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})", css)
    if not blocks:
        sys.exit("error: no @font-face blocks in Google Fonts response")
    out = []
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        url = re.search(r"url\((https://[^)]+\.woff2)\)", block)
        if not url:
            continue
        b64 = base64.b64encode(fetch(url.group(1))).decode()
        out.append(block.replace(
            url.group(1), f"data:font/woff2;base64,{b64}"))
    print(f"fonts: embedded {len(out)} @font-face blocks "
          f"({', '.join(KEEP_SUBSETS)})")
    return "\n".join(out)


def extract(pattern: str, text: str, what: str) -> str:
    m = re.search(pattern, text, re.S)
    if not m:
        sys.exit(f"error: could not extract {what} from {SOURCE.name}")
    return m.group(1)


def main() -> None:
    src = SOURCE.read_text()
    helmet_css = extract(r"<helmet>.*?<style>(.*?)</style>", src,
                         "helmet <style>")
    sections = extract(r"<x-import[^>]*>(.*)</x-import>", src,
                       "slide sections")
    n = len(re.findall(r"<section\b", sections))
    print(f"slides: {n}")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<link rel="icon" href="data:image/svg+xml,{FAVICON.replace('#', '%23').replace('"', "'")}">
<style>
{inline_fonts()}
</style>
<style>
{helmet_css}
</style>
<script>
{STAGE_JS.read_text().replace("</script", "<\\/script")}
</script>
<script>
{EXTRAS_JS}
</script>
</head>
<body>
<deck-stage width="1920" height="1080">
{sections}
</deck-stage>
</body>
</html>
"""
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print(f"wrote {OUT.relative_to(ROOT)} "
          f"({OUT.stat().st_size / 1024:.0f} KiB)")


if __name__ == "__main__":
    main()
