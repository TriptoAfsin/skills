# spec.json reference

Paths are relative to the spec file. All coordinates are in the original image's pixels, even when the panel is cropped.

## Top level

| Field | Meaning |
|---|---|
| `title` | Headline, for example "Settings: Save moved to the header" |
| `subtitle` | Product · screen path · date |
| `layout` | `side` (default) or `stack` (After under Before, better for wide desktop pages) |
| `width` | Each panel's width in the output, in px (default auto: up to 820 side by side, 1100 stacked) |
| `out` | Output file name (default `compare.png`). `--out` on the command line overrides it |
| `panels[]` | Usually Before and After. A third works too ("After (phone)"). **One panel = a single annotated screenshot** |

## Panel

| Field | Meaning |
|---|---|
| `label` | Pill text: `Before` is grey, `After` green, anything else blue. Leave it out on a single screenshot for no pill |
| `image` | Screenshot path |
| `crop` | `[x, y, w, h]`: zoom into the area that changed |
| `marks[]` | The markup |

## Mark

| Field | Meaning |
|---|---|
| `shape` | `box` (default), `circle`, `highlight`, `arrow`, `redact` |
| `box` | `[x, y, w, h]`, used by every shape except `arrow` |
| `from`, `to` | `[x, y]` points for `arrow`. The number sits at `from` |
| `kind` | Colour: `added` green, `changed` amber, `removed` red, `note` blue (default) |
| `note` | Legend text, in plain words for the reader |
| `label` | Optional short callout drawn on the image next to the mark ("Moved here") |
| `n` | Pin the number. By default they run 1, 2, 3... across the whole image |

`redact` pixelates the area and is never numbered or listed in the legend. When the same element appears on both
sides (moved or changed), give both marks the same `n` so they read as one change.
