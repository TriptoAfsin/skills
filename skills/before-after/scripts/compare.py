#!/usr/bin/env python3
"""Render labeled before/after screenshots with numbered annotations into one PNG.

    python compare.py spec.json            # writes spec's "out" (default: compare.png next to the spec)
    python compare.py spec.json --out x.png

Spec (paths are relative to the spec file; box coordinates are in the ORIGINAL image's pixels):
{
  "title": "Rules: pay tied to violations is now a switch",
  "subtitle": "Acme Dashboard - Settings > Rules - 2026-11-13",
  "layout": "side",                       # "side" (default) or "stack"
  "width": 760,                           # each panel's width in the output (default: auto)
  "panels": [
    {"label": "Before", "image": "before.png", "crop": [0, 120, 1440, 700],
     "marks": [{"box": [40, 300, 600, 180], "kind": "removed", "note": "Tier table always shown"}]},
    {"label": "After", "image": "after.png",
     "marks": [{"box": [40, 300, 600, 60], "kind": "added", "note": "New switch"},
               {"box": [40, 380, 600, 200], "kind": "changed", "note": "Tiers only when it's on"}]}
  ]
}
kind: added (green), changed (amber), removed (red), note (blue, default).
Numbers run 1, 2, 3... across the whole image unless a mark sets "n" itself.

Mark shapes ("shape", default "box"):
  box        rounded outline + light fill, numbered          {"box": [x, y, w, h]}
  circle     ellipse around the box, numbered                {"box": [...]}
  highlight  marker-pen fill, no outline, numbered           {"box": [...]}
  arrow      arrow from one point to another, numbered at the tail   {"from": [x, y], "to": [x, y]}
  redact     pixelates the area; no number, not in the legend        {"box": [...]}
Optional on any numbered mark: "label": short text drawn on the image next to it (callout).
One panel only = a single annotated screenshot (pill hidden unless "label" is set).
"""
import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

KINDS = {
    "added": ((22, 163, 74), "Added"),
    "changed": ((217, 119, 6), "Changed"),
    "removed": ((220, 38, 38), "Removed"),
    "note": ((37, 99, 235), "Note"),
}
BG, INK, INK2, LINE = (247, 247, 245), (24, 24, 27), (100, 100, 110), (214, 214, 210)
PILL = {"before": ((228, 228, 231), INK), "after": ((22, 101, 52), (255, 255, 255))}
PAD, GAP, SCALE_UP = 40, 36, 2  # SCALE_UP renders at 2x for crisp text


def font(size, bold=False):
    names = (["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf", "Helvetica-Bold.ttf"] if bold
             else ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf", "Helvetica.ttf"])
    dirs = ["", "C:/Windows/Fonts/", "/usr/share/fonts/truetype/dejavu/", "/Library/Fonts/", "/System/Library/Fonts/"]
    for n in names:
        for d in dirs:
            try:
                return ImageFont.truetype(d + n, size)
            except OSError:
                pass
    return ImageFont.load_default(size)


def wrap(draw, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + ([cur] if cur else [])


def badge(draw, cx, cy, n, color, s):
    r = 15 * s
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color, outline=(255, 255, 255), width=3 * s)
    draw.text((cx, cy), str(n), font=font(16 * s, True), fill=(255, 255, 255), anchor="mm")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out")
    a = ap.parse_args()
    spec_path = Path(a.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base = spec_path.parent
    s = SCALE_UP
    stack = spec.get("layout", "side") == "stack"

    # Load, crop and normalize panels to one width.
    panels, n = [], 0
    for p in spec["panels"]:
        img = Image.open(base / p["image"]).convert("RGB")
        cx, cy = 0, 0
        if p.get("crop"):
            x, y, w, h = p["crop"]
            img, cx, cy = img.crop((x, y, x + w, y + h)), x, y
        marks = []
        for m in p.get("marks", []):
            mm = dict(m)
            if m.get("shape") != "redact":
                n = m.get("n", n + 1)
                mm["n"] = n
            if "box" in m:
                mm["box"] = [m["box"][0] - cx, m["box"][1] - cy, m["box"][2], m["box"][3]]
            for key in ("from", "to"):
                if key in m:
                    mm[key] = [m[key][0] - cx, m[key][1] - cy]
            marks.append(mm)
        # Redact before resizing so the pixelation scales with the image.
        for mm in marks:
            if mm.get("shape") == "redact":
                bx, by, bw, bh = [int(v) for v in mm["box"]]
                region = img.crop((bx, by, bx + bw, by + bh))
                small = region.resize((max(1, bw // 14), max(1, bh // 14)), Image.BILINEAR)
                img.paste(small.resize(region.size, Image.NEAREST), (bx, by))
        marks = [mm for mm in marks if mm.get("shape") != "redact"]
        panels.append({"label": p.get("label", ""), "img": img, "marks": marks})

    width = spec.get("width") or (1100 if stack else min(820, max(pp["img"].width for pp in panels)))
    pw = width * s
    for pp in panels:
        k = pw / pp["img"].width
        pp["k"] = k
        pp["img"] = pp["img"].resize((pw, round(pp["img"].height * k)), Image.LANCZOS)

    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f_title, f_sub = font(30 * s, True), font(17 * s)
    f_pill, f_note = font(15 * s, True), font(16 * s)

    # Legend lines per panel.
    for pp in panels:
        rows = []
        for m in pp["marks"]:
            color, kind_label = KINDS.get(m.get("kind", "note"), KINDS["note"])
            text = m.get("note") or kind_label
            lines = wrap(probe, text, f_note, pw - 44 * s)
            rows.append((m["n"], color, lines))
        pp["legend"] = rows
        pp["legend_h"] = sum(max(1, len(r[2])) * 24 * s + 12 * s for r in rows) + (14 * s if rows else 0)

    title_lines = wrap(probe, spec.get("title", ""), f_title, (pw * (1 if stack else len(panels)) + GAP * s * (0 if stack else len(panels) - 1)))
    head_h = len(title_lines) * 40 * s + (30 * s if spec.get("subtitle") else 0) + (24 * s if title_lines else 0)
    pill_h = 40 * s

    blocks = [(pill_h if pp["label"] else 0) + pp["img"].height + pp["legend_h"] for pp in panels]
    if stack:
        W = pw + 2 * PAD * s
        H = head_h + sum(blocks) + GAP * s * (len(panels) - 1) + 2 * PAD * s
    else:
        W = pw * len(panels) + GAP * s * (len(panels) - 1) + 2 * PAD * s
        H = head_h + max(blocks) + 2 * PAD * s

    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas, "RGBA")
    y = PAD * s
    for line in title_lines:
        d.text((PAD * s, y), line, font=f_title, fill=INK)
        y += 40 * s
    if spec.get("subtitle"):
        d.text((PAD * s, y + 2 * s), spec["subtitle"], font=f_sub, fill=INK2)
        y += 30 * s
    if title_lines:
        y += 24 * s
    top = y

    for i, pp in enumerate(panels):
        x0 = PAD * s if stack else PAD * s + i * (pw + GAP * s)
        y0 = top + (sum(blocks[:i]) + GAP * s * i if stack else 0)
        # Label pill.
        label = pp["label"]
        if label:
            bg, fg = PILL.get(label.lower(), ((37, 99, 235), (255, 255, 255)))
            tw = d.textlength(label.upper(), font=f_pill)
            d.rounded_rectangle([x0, y0, x0 + tw + 28 * s, y0 + 28 * s], radius=14 * s, fill=bg)
            d.text((x0 + 14 * s, y0 + 14 * s), label.upper(), font=f_pill, fill=fg, anchor="lm")
        iy = y0 + (pill_h if label else 0)
        canvas.paste(pp["img"], (x0, iy))
        d.rectangle([x0 - 1, iy - 1, x0 + pw, iy + pp["img"].height], outline=LINE, width=2)
        # Marks.
        k = pp["k"]
        ih = pp["img"].height
        clampx = lambda v: min(max(v, x0 + 16 * s), x0 + pw - 16 * s)
        clampy = lambda v: min(max(v, iy + 16 * s), iy + ih - 16 * s)
        for m in pp["marks"]:
            color = KINDS.get(m.get("kind", "note"), KINDS["note"])[0]
            shape = m.get("shape", "box")
            if shape == "arrow":
                ax, ay = x0 + m["from"][0] * k, iy + m["from"][1] * k
                tx, ty = x0 + m["to"][0] * k, iy + m["to"][1] * k
                d.line([ax, ay, tx, ty], fill=color, width=5 * s)
                ang = math.atan2(ty - ay, tx - ax)
                hl = 22 * s
                d.polygon([(tx, ty),
                           (tx - hl * math.cos(ang - 0.45), ty - hl * math.sin(ang - 0.45)),
                           (tx - hl * math.cos(ang + 0.45), ty - hl * math.sin(ang + 0.45))], fill=color)
                bxc, byc, r = clampx(ax), clampy(ay), [ax, ay, ax, ay]
            else:
                bx, by, bw, bh = m["box"]
                r = [x0 + bx * k, iy + by * k, x0 + (bx + bw) * k, iy + (by + bh) * k]
                if shape == "circle":
                    d.ellipse([r[0] - 10 * s, r[1] - 10 * s, r[2] + 10 * s, r[3] + 10 * s], outline=color, width=5 * s)
                elif shape == "highlight":
                    d.rectangle(r, fill=color + (70,))
                else:
                    d.rounded_rectangle(r, radius=8 * s, fill=color + (28,), outline=color, width=4 * s)
                bxc, byc = clampx(r[0]), clampy(r[1])
            badge(d, bxc, byc, m["n"], color, s)
            if m.get("label"):
                f_lab = font(15 * s, True)
                tw2 = d.textlength(m["label"], font=f_lab)
                lx = min(max(r[2] + 10 * s, x0 + 8 * s), x0 + pw - tw2 - 26 * s)
                if r[2] + 10 * s + tw2 + 18 * s > x0 + pw:  # no room on the right: put it under
                    lx, ly0 = clampx(r[0]), r[3] + 8 * s
                else:
                    ly0 = r[1]
                ly0 = min(max(ly0, iy + 4 * s), iy + ih - 32 * s)
                d.rounded_rectangle([lx, ly0, lx + tw2 + 18 * s, ly0 + 28 * s], radius=6 * s, fill=color)
                d.text((lx + 9 * s, ly0 + 14 * s), m["label"], font=f_lab, fill=(255, 255, 255), anchor="lm")
        # Legend.
        ly = iy + pp["img"].height + 22 * s
        for num, color, lines in pp["legend"]:
            badge(d, x0 + 15 * s, ly + 12 * s, num, color, s)
            for j, line in enumerate(lines):
                d.text((x0 + 40 * s, ly + j * 24 * s), line, font=f_note, fill=INK)
            ly += max(1, len(lines)) * 24 * s + 12 * s

    out = Path(a.out) if a.out else base / spec.get("out", "compare.png")
    canvas = canvas.resize((W // s, H // s), Image.LANCZOS) if spec.get("scale", 1) == 1 else canvas
    canvas.save(out, optimize=True)
    print("%s  %dx%d" % (out, canvas.width, canvas.height))


if __name__ == "__main__":
    sys.exit(main())
