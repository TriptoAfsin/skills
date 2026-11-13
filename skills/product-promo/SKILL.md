---
name: product-promo
description: Make a short product promo video (20-45 s, music-led) from real captures of the product, in one or several aspect ratios - 16x9, 9x16, 1x1, 4x5 or custom - that all keep the same feel. Brief one question at a time, three storylines to pick from, a locked SPEC, live footage with a camera and cursor that follow the recorded clicks, a title plate per shot, brand-colour reveal, claim and end card, then each format recomposed rather than cropped. Built on HyperFrames. Use when the user wants a promo, launch, teaser or social video for an app, site, CLI or product, or wants an existing promo cut for another platform or aspect ratio.
---

# product-promo

A 20–45 s promo built from the **real product**, never a drawn mock-up of it. The same storyline and feel are cut
once per format, and each format is recomposed for its frame.

**Engine:** HyperFrames (HTML + GSAP rendered to MP4). Load the `hyperframes` skill first, since it holds the render
contract, and `hyperframes-cli` for commands. If it's missing, tell the user to install it (`npx hyperframes skills update`)
and wait. `product-launch-video` covers URL-to-promo work in general. This skill is the house recipe on top of it.

## Steps

| # | Step | Details |
|---|---|---|
| 1 | **Brief, one question at a time** (question UI, recommended first): product and the one thing to remember · where it will be posted (this sets the formats) · length · call to action (store badge, URL) · music only, or a voiceover | [references/brief-and-story.md](references/brief-and-story.md) |
| 2 | **Capture the real product** while logging every click to `events.json` | [references/capture.md](references/capture.md) |
| 3 | **Three storylines** in `STORYLINES.md`, shown to the user (an Artifact, or the question UI), one picked or mixed | [references/brief-and-story.md](references/brief-and-story.md) |
| 4 | **Lock `SPEC.md`**: GOAL, OUTPUT, TIME, LOOK, SHOTS with times, BANNED, QA times, MUSIC | [references/brief-and-story.md](references/brief-and-story.md) |
| 5 | **Build the master format** from `templates/` and the house look | [references/look.md](references/look.md) |
| 6 | **Recompose each extra format**: same beats and timing, new layout | [references/formats.md](references/formats.md) |
| 7 | **Check, look, render**: `npm run check`, snapshots at the QA times (read them), render, stop the preview | `hyperframes` review |

## Project layout

```
promo/
├── STORYLINES.md  SPEC.md
├── recordings/    session.mp4 + events.json   (shared by every format)
├── 16x9/          one HyperFrames project per format: index.html, compositions/, assets/ (copied or linked)
├── 9x16/
└── <product>-promo-<format>-<storyline>.mp4    renders
```

## Kit

- `templates/shot.html`: live footage + camera + cursor + title plate
- `templates/reveal.html`, `claim.html`, `endcard.html`: adapt to any aspect ratio (container units and an
  `aspect-ratio` container query), so the same file works in 16:9, 9:16, 1:1 and 4:5
- `scripts/scene_motion.py events.json --id <shot> --media-start <s> --duration <s> --rate <x> --frame WxH`: prints
  the camera and cursor timeline for a shot, framed for that format (`--zoom` to push in)

## Rules

- **Every product frame is real**: recorded footage or real screenshots. Never invent UI, numbers or features.
  Numbers on screen are the ones in the capture.
- Anything destructive in the recording runs on demo data only (a throwaway folder, a dummy server), never on real data.
- One accent word per title. Titles land and stay; they don't drift.
- The music decides the cut: changes land on beats, and every format keeps the same timing so one mix works for all.
- No voiceover unless asked. Music, clicks on real clicks, a whoosh on the reveal and the end card, one riser into the payoff.
- Snapshot and look at each format before rendering. A passing `check` doesn't show how it looks.
- Stop the preview server when finished, and don't commit renders or recordings unless asked.
