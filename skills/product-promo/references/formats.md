# Formats: recompose, don't crop

Build the master (usually 16:9) first. Then each extra format gets its own project folder with **the same shots,
timing and music**, laid out again for its frame. Cropping a 16:9 render to 9:16 loses the product and the type.

| Format | Size | Init preset | Where it goes |
|---|---|---|---|
| 16:9 | 1920×1080 | `--resolution landscape` | Website, YouTube, X, launch posts |
| 9:16 | 1080×1920 | `--resolution portrait` | Reels, Shorts, TikTok, Stories |
| 1:1 | 1080×1080 | `--resolution square` | Feeds, Product Hunt gallery |
| 4:5 | 1080×1350 | no preset: set `data-width`/`data-height` and the viewport by hand | Instagram and LinkedIn feed |
| Custom (2:1, 4:3, 21:9) | any | by hand | Banners, embeds |

`npx hyperframes init <dir> --resolution <preset>` sets the canvas. Every `data-width`/`data-height` in `index.html`
and the `<meta name="viewport">` must match the format.

## What changes per format

| | 16:9 | 1:1 and 4:5 | 9:16 |
|---|---|---|---|
| Footage | Fills the width, gentle push-ins | Zoomed about 1.4×, the camera follows each click | Zoomed about 1.9× on the clicked area, in a band in the upper middle |
| Title plate | Bottom left, over the footage | Under the footage | In the band under the footage, bigger type (~7.4% of width) |
| Reveal and end card | Icon and name side by side | Stacked | Stacked, name may wrap to two lines |
| Cuts | As in the SPEC | Same | Same times. Shorter shots can hold one beat longer if a plate needs reading time |
| Safe area | 5% margins | 6% | Keep text out of the top ~14% and the bottom ~20% (platform UI) |

The templates handle the reveal, claim, end card and plate placement on their own (container units plus
`@container (aspect-ratio < 1.2)`). For footage shots, re-run `scene_motion.py` with the new `--frame` (and a `--zoom`
if needed), and paste its lines into that format's shot.

## Steps for each extra format

1. `npx hyperframes init <promo>/<WxH-name> --resolution <preset>` (or copy the master's folder and change the sizes).
2. Copy `compositions/` and `assets/` from the master (or link `assets/` to save space).
3. Update the sizes in `index.html`. Re-run `scene_motion.py` for each footage shot with `--frame WxH`.
4. `npm run check`, then `npx hyperframes snapshot --at <QA times>`, and look at every frame: is the clicked thing
   on screen, can the plate be read, is any text inside the platform's UI area?
5. Render. Name it `<product>-promo-<format>-<storyline>.mp4`.
