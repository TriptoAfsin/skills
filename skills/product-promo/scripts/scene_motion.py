#!/usr/bin/env python3
"""Generate GSAP camera + cursor lines for one live-footage shot from a recorded events log.

    python scene_motion.py events.json --id scan --media-start 12.0 --duration 4.0 --rate 1.5 \
        --frame 1080x1920 [--zoom 1.6] [--lead 0.35] [--labels click-memory-card,click-free-memory]

events.json (written while recording the real product):
  {"window": {"w": 1882, "h": 1212}, "events": [{"t": 12.32, "label": "click-x", "x": 1079, "y": 279, "click": true}, ...]}
  t is seconds into the recording, x/y are pixels in the recording.

Prints lines to paste into the shot's timeline (`tl`), for elements #<id>-stage (the footage wrapper, transform-origin
0 0, sized to the recording) and #<id>-cur (the cursor, inside the stage). The camera frames each click so it stays
on screen in any aspect ratio: wide frames show most of the window, tall frames zoom in on the clicked area.
"""
import argparse
import json


def fit_scale(frame_w, frame_h, src_w, src_h, zoom):
    # Base: the window fills the frame's width (landscape) or most of its height band (portrait), then zoom.
    base = frame_w / src_w if frame_w >= frame_h else (frame_w / src_w) * 1.9
    return base * zoom


def framed(px, py, s, frame_w, frame_h, src_w, src_h, focus_y=0.45):
    """Stage x/y so that recording point (px, py) sits near the frame centre, clamped to the recording's edges."""
    sw, sh = src_w * s, src_h * s
    x = frame_w / 2 - px * s
    y = frame_h * focus_y - py * s
    x = (frame_w - sw) / 2 if sw <= frame_w else min(0, max(frame_w - sw, x))
    y = (frame_h - sh) / 2 if sh <= frame_h else min(0, max(frame_h - sh, y))
    return round(x, 1), round(y, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("events")
    ap.add_argument("--id", required=True)
    ap.add_argument("--media-start", type=float, required=True, help="data-media-start of the shot's video")
    ap.add_argument("--duration", type=float, required=True, help="shot length in seconds (timeline time)")
    ap.add_argument("--rate", type=float, default=1.0, help="data-playback-rate of the shot's video")
    ap.add_argument("--frame", default="1920x1080")
    ap.add_argument("--zoom", type=float, default=1.0, help="extra zoom on top of the format's base framing")
    ap.add_argument("--lead", type=float, default=0.35, help="seconds the cursor arrives before each click")
    ap.add_argument("--labels", help="comma-separated event labels to use (default: every click in the shot)")
    a = ap.parse_args()

    log = json.load(open(a.events, encoding="utf-8"))
    src_w, src_h = log["window"]["w"], log["window"]["h"]
    fw, fh = (int(v) for v in a.frame.lower().split("x"))
    wanted = set(a.labels.split(",")) if a.labels else None

    def scene_t(t):
        return (t - a.media_start) / a.rate

    clicks = [e for e in log["events"] if e.get("click") and "x" in e
              and (wanted is None or e["label"] in wanted)
              and 0 <= scene_t(e["t"]) <= a.duration]
    s = round(fit_scale(fw, fh, src_w, src_h, a.zoom), 3)
    sid, cid = "#%s-stage" % a.id, "#%s-cur" % a.id
    out = []

    if not clicks:
        x, y = framed(src_w / 2, src_h / 2, s, fw, fh, src_w, src_h)
        out.append('tl.set("%s", { x: %s, y: %s, scale: %s }, 0);' % (sid, x, y, s))
        print("\n".join(out))
        return

    first = clicks[0]
    x, y = framed(first["x"], first["y"], s, fw, fh, src_w, src_h)
    out.append('tl.set("%s", { x: %s, y: %s, scale: %s }, 0);' % (sid, x, y, s))
    start_x, start_y = first["x"] + 220, first["y"] + 160
    prev_t = 0.0
    for i, e in enumerate(clicks):
        t = round(scene_t(e["t"]), 3)
        arrive = max(prev_t + 0.05, t - a.lead)
        if i == 0:
            out.append('tl.fromTo("%s", { x: %d, y: %d, opacity: 0 }, { x: %d, y: %d, opacity: 1, duration: %.3f, ease: "power3.out" }, %.3f);'
                       % (cid, start_x, start_y, e["x"], e["y"], max(0.15, t - arrive), arrive))
        else:
            out.append('tl.to("%s", { x: %d, y: %d, duration: %.3f, ease: "power3.inOut" }, %.3f);'
                       % (cid, e["x"], e["y"], max(0.12, t - arrive), arrive))
            nx, ny = framed(e["x"], e["y"], s, fw, fh, src_w, src_h)
            if (nx, ny) != (x, y):
                out.append('tl.to("%s", { x: %s, y: %s, duration: %.3f, ease: "power2.inOut" }, %.3f);'
                           % (sid, nx, ny, max(0.3, t - arrive + 0.1), max(0, arrive - 0.1)))
                x, y = nx, ny
        out.append('tl.to("%s", { scale: 0.82, duration: 0.05, yoyo: true, repeat: 1, ease: "none" }, %.3f);' % (cid, t))
        prev_t = t
    print("\n".join(out))


if __name__ == "__main__":
    main()
