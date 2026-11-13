#!/usr/bin/env python3
"""Rebuild the README's before/after images with the before-after skill's own renderer.

    python docs/make-images.py

Text cards (terminal or chat style) are drawn here, then skills/before-after/scripts/compare.py composes each pair
with numbered marks. Line colours: a prefix "g|" green, "r|" red, "m|" muted, "b|" blue, "y|" amber, "w|" bold white.
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "images"
WORK = ROOT / "images" / "_src"
COMPARE = ROOT.parent / "skills" / "before-after" / "scripts" / "compare.py"
COL = {"g": (74, 222, 128), "r": (248, 113, 113), "m": (139, 146, 160), "b": (143, 176, 255), "y": (251, 191, 36),
       "w": (240, 242, 246), "": (214, 218, 226)}
BG, BAR = (14, 16, 20), (28, 31, 38)
W, PAD, LH, TOP = 1100, 36, 40, 74


def font(names, size):
    for n in names:
        for d in ("", "C:/Windows/Fonts/", "/usr/share/fonts/truetype/dejavu/", "/Library/Fonts/", "/System/Library/Fonts/"):
            try:
                return ImageFont.truetype(d + n, size)
            except OSError:
                pass
    return ImageFont.load_default(size)


MONO = font(["consola.ttf", "DejaVuSansMono.ttf", "Menlo.ttc"], 25)
MONO_B = font(["consolab.ttf", "DejaVuSansMono-Bold.ttf", "Menlo.ttc"], 25)
SANS_B = font(["segoeuib.ttf", "DejaVuSans-Bold.ttf", "Helvetica.ttc"], 22)


def card(name, title, lines):
    """Draw a terminal-style card; returns the path and a function giving a box for a line range."""
    h = TOP + PAD + len(lines) * LH + PAD
    im = Image.new("RGB", (W, h), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 54], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([22 + i * 26, 19, 38 + i * 26, 35], fill=c)
    d.text((110, 27), title, font=SANS_B, fill=(200, 204, 212), anchor="lm")
    for i, raw in enumerate(lines):
        key, _, text = raw.partition("|") if "|" in raw[:2] else ("", "", raw)
        d.text((PAD + 30, TOP + PAD + i * LH), text, font=MONO_B if key == "w" else MONO, fill=COL.get(key, COL[""]))
    path = WORK / (name + ".png")
    im.save(path)

    def box(a, b=None, x0=PAD - 6, x1=W - PAD + 12):
        b = a if b is None else b
        return [x0, TOP + PAD + a * LH - 5, x1 - x0, (b - a + 1) * LH - 2]
    return path.name, box


def render(name, title, subtitle, panels, layout="side"):
    spec = {"title": title, "subtitle": subtitle, "layout": layout, "out": "../" + name + ".png", "panels": panels}
    p = WORK / (name + ".json")
    p.write_text(json.dumps(spec, indent=1), encoding="utf-8")
    subprocess.run([sys.executable, str(COMPARE), str(p)], check=True)


def main():
    WORK.mkdir(parents=True, exist_ok=True)

    # lean-flow
    b, bb = card("lean-before", "terminal: without lean-flow", [
        "$ railway up",
        "r|  Deployed to service \"landing\"",
        "m|# \"done\", nothing checked",
        "",
        "$ # an hour later, still running:",
        "r|  :3000  node  next dev",
        "r|  :9222  chrome --headless",
        "r|  pg-test  postgres:16",
    ])
    a, ab = card("lean-after", "terminal: with lean-flow", [
        "$ railway status",
        "b|  project acme · env production",
        "y|  deploy to \"docs\"? waiting for your yes",
        "$ npm run build && browser check 1440 + 390",
        "g|  build ok · no console errors · no h-scroll",
        "$ sh dev-leftovers.sh",
        "g|  dev servers: none · browsers: none",
        "g|  containers: none",
    ])
    render("lean-flow", "lean-flow: check it, ship it, leave the machine tidy", "Same task, two agents", [
        {"label": "Before", "image": b, "marks": [
            {"box": bb(1), "kind": "removed", "note": "Deployed to the linked default, which was the wrong service"},
            {"box": bb(5, 7), "kind": "removed", "note": "Dev server, browser and container left running"}]},
        {"label": "After", "image": a, "marks": [
            {"box": ab(0, 2), "kind": "added", "note": "Target checked, and the deploy waits for a yes"},
            {"box": ab(3, 4), "kind": "added", "note": "Verified before saying done"},
            {"box": ab(5, 7), "kind": "added", "note": "Leftover snapshot comes back clean"}]}])

    # design-flow
    b, bb = card("design-before", "chat: without design-flow", [
        "w|you: make the settings page look good",
        "",
        "m|agent: Editing 6 files...",
        "r|  + hero with purple-to-blue gradient",
        "r|  + three feature cards in a row",
        "r|  + glassmorphism panels",
        "m|  Done! It looks modern now.",
    ])
    a, ab = card("design-after", "chat: with design-flow", [
        "w|you: make the settings page look good",
        "b|Q1 of 5  Who uses this page most?",
        "    > Admins, weekly (recommended)",
        "b|Artifact: 3 directions  A  B  C",
        "    desktop + 390 px · why · trade-off",
        "g|you picked B -> DESIGN.md locked",
        "g|build -> polish -> verify -> before/after",
    ])
    render("design-flow", "design-flow: nothing reaches the code until you've picked it", "Same request, two agents", [
        {"label": "Before", "image": b, "marks": [
            {"box": bb(2, 5), "kind": "removed", "note": "Code changes straight away, with generic AI-looking choices"}]},
        {"label": "After", "image": a, "marks": [
            {"box": ab(1, 2), "kind": "added", "note": "One question at a time, recommended answer first"},
            {"box": ab(3, 4), "kind": "added", "note": "Directions mocked up as a live Artifact"},
            {"box": ab(5, 6), "kind": "added", "note": "Built only after the pick, then checked"}]}])

    # team-reply
    b, bb = card("reply-before", "draft: without team-reply", [
        "Hi Alex! Hope you're doing well :) So I looked",
        "into the export thing you mentioned yesterday",
        "and it turns out there were a few things going",
        "on, basically the CSV builder was skipping the",
        "status column because of how the mapping...",
        "r|(212 words, the answer is in paragraph 3)",
        "r|(your 2nd question isn't answered)",
    ])
    a, ab = card("reply-after", "Slack draft: with team-reply", [
        "w|Salam @Alex, both are sorted.",
        "",
        "- *Export:* CSV now has the *status* column.",
        "  Settings -> Export -> Download.",
        "- *Old files:* re-download them, they update too.",
        "",
        "Shout if anything looks off.",
        "g|[48 words, limit 80: OK] -> saved as Slack draft",
    ])
    render("team-reply", "team-reply: read the thread, answer every question, keep it short",
           "Same thread, two drafts", [
        {"label": "Before", "image": b, "marks": [
            {"box": bb(0, 4), "kind": "removed", "note": "Warm-up and backstory before the answer"},
            {"box": bb(5, 6), "kind": "removed", "note": "Too long, and one question missed"}]},
        {"label": "After", "image": a, "marks": [
            {"box": ab(2, 4), "kind": "added", "note": "Each of their questions answered, in their order"},
            {"box": ab(7), "kind": "added", "note": "Word budget checked; saved as a draft, not sent"}]}])

    print("text cards done; before-after and product-promo images come from real captures (see README)")


if __name__ == "__main__":
    main()
