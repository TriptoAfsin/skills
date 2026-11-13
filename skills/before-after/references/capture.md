# Capturing the two states

## Pick the tool

Use whatever the user or repo already uses. Check in this order: what the user said, the repo's config and scripts,
then what's installed. Ask once only if there's still a real choice (the `lean-flow` skill's `references/cli.md` §0
works through this). Common ones:

| Tool | Screenshot | Resize |
|---|---|---|
| `playwright-cli` | `playwright-cli screenshot --filename=before.png` | `playwright-cli resize 1440 900` |
| `agent-browser` | `agent-browser screenshot before.png` | `agent-browser set viewport 1440 900` |
| Claude in Chrome / DevTools MCP | its screenshot tool | its resize tool |
| Mobile (`agent-device`, `adb`, simulator) | the device screenshot command | use the device's own size |
| None (the user sent images) | use them as they are | — |

These commands change between versions. Check the tool's own skill or `--help` before running them.

## Where Before comes from

In order of preference:
1. **Before you change the code:** screenshot the current app first, then build the change.
2. **Production**, if the change isn't live yet: same page, same viewport, a test account.
3. **The previous commit in a worktree:**
   ```bash
   git worktree add ../<repo>-before <commit-before-the-change>
   # install, run it on other ports so it doesn't clash with the current dev server, screenshot, stop it
   git worktree remove ../<repo>-before
   ```
   Share the local database only if the schema didn't change between the two commits. Otherwise use seed data.

After is the local build, or the deployed site once it's live.

## Making the shots match

- Wait for data to load (no skeletons or spinners), close toasts and cookie banners, and scroll to the same place in both.
- Same theme, zoom and window size on both sides. Same account and data where possible.
- Several screens: `before-1.png` / `after-1.png`, and so on, with one spec and one image per screen.

## Boxes

Coordinates are `[x, y, width, height]` in the screenshot's pixels. Take them from the page, not by eye:

```js
// run in the page (the tool's eval/evaluate command) on the element
const r = el.getBoundingClientRect();
[r.x, r.y, r.width, r.height].map(v => Math.round(v * devicePixelRatio))
```

- Pad about 8 px on each side so the outline doesn't sit on the element's edge.
- In a full-page screenshot, add `window.scrollY` to `y` (times `devicePixelRatio`).
- Arrows use points: `from` (the tail, where the number goes) and `to` (the head).
- For a screenshot someone sent you: open the image, estimate the box, render it, look at the result and adjust.
