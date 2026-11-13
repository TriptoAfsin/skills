# The house look

The feel stays the same across products and formats. The tokens change per product: take them from the product's
`DESIGN.md`, its theme file or its own screenshots.

## Two worlds

- **Pain world** (the hook): the native OS look where the problem happens (a desktop warning, a terminal error, a
  browser tab), with one red for the problem.
- **Product world** (from the reveal on): the product's own theme. Its ground colour, its fonts, its real UI.

## Tokens (set per product as CSS variables at the top of each composition)

| Token | Use | Dev Cleaner example |
|---|---|---|
| `--ground` | plates, claim, end card | `#0e1014` |
| `--stage-ground` | behind footage | `#0b0d11` |
| `--accent` | reveal flood only, and the end card | `#1d4ed8` |
| `--text-accent` | **one** word per title, the claim's second line, the URL | `#8fb0ff` |
| `--text`, `--muted`, `--line` | text, meta line, plate border | `#eceef2`, `#a3a9b4`, `#2a2f38` |
| Display font | titles, name, claim (`assets/fonts/display.woff2`) | Geist |
| Mono font | numbers, URLs (`assets/fonts/mono.woff2`) | Geist Mono |

## Elements

| Element | How it looks and moves |
|---|---|
| Title plate | Solid `--ground` plate, 1px `--line` border, radius ~1.7% of the short side, soft shadow. Display 700 at ~5.6% of the short side (landscape) or ~7.4% of the width (portrait). Words blur in one by one: 0.13 s each, 0.067 s stagger, `power2.out`. Stays put once it has landed |
| Footage stage | The recording at its own size, radius 14, 1px line plus a deep shadow. Camera moves `power2.inOut`, following the clicks (`scene_motion.py`) |
| Cursor | A white arrow with a dark outline, 72 px. It arrives 0.35 s before each click and presses (scale 0.82, 0.1 s) on the click |
| Reveal | `--accent` flood wipes up (clip-path, 0.4 s `power2.inOut`); icon pops (`back.out(1.6)`); name resolves letter by letter (blur 10 → 0, 0.06 s stagger); one-line sub |
| Claim | Two short lines, the second in `--text-accent`, word by word (0.15 s, 0.08 s stagger) |
| End card | Icon carried in from below (`back.out(1.4)`), wordmark wipes in left to right, badge, URL and meta blur in. Holds ≥ 2.5 s |

## Sound

One music bed, 110–128 BPM, its energy dropping in clean at the reveal and fading out over the end card. A click on every
real click (from `events.json`), a whoosh on the reveal and on the end card, and one riser into the payoff. Music only
by default. Keep a second bed as an alternative and render both if the user can't decide.

## Banned

A dark void with small floating UI · glow, particles, lens flares · three cards in a row · a docked logo in a corner ·
titles that drift after landing · invented UI or numbers · naming competitors · speed claims nobody measured ·
more than one accent word per title.
