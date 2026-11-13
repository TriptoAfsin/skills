# Capturing the real product

One continuous recording of a scripted session, plus a log of every click. The camera, the cursor and the shot
timings are all derived from that log, so it's worth getting right.

## Pick the tool

Use whatever the user or repo already uses (check: what they said → the repo → what's installed → ask once). Common choices:

| Product | Recording |
|---|---|
| Web app | `playwright-cli video-start` / `video-stop`, `agent-browser record start <path>` / `record stop`, or a Playwright script with `recordVideo` |
| Desktop app | Drive it with a script (Playwright for Electron/Tauri webviews, or the OS automation tool), record the window with `ffmpeg` (Windows `-f gdigrab`, macOS `-f avfoundation`, Linux `-f x11grab`) or OBS |
| Mobile | `agent-device`, `adb shell screenrecord`, `xcrun simctl io booted recordVideo` |
| CLI | A real terminal recording (asciinema or a screen recording) with a large font |

Commands change between versions. Check the tool's skill or `--help` first.

## Record

- **Script the session** rather than clicking by hand, so it can be re-recorded when the product changes. Keep the script in
  the promo folder (`recordings/record.*`).
- **Fix the window size** (for example 1880×1210) and the theme. Hide personal data, notifications and the bookmarks bar.
- **Seed demo data** for anything destructive: a throwaway folder to delete, a dummy server on the port you free.
- Pause about 0.6 s before and after each click, so every shot has room for the camera to settle.
- Record at least 30 fps. Re-encode to H.264 MP4 (`ffmpeg -i in.webm -c:v libx264 -crf 18 -pix_fmt yuv420p session.mp4`).

## events.json

Write it from the same script, using the recording's clock:

```json
{"window": {"w": 1882, "h": 1212},
 "events": [
   {"t": 1.53, "label": "sync"},
   {"t": 12.32, "label": "click-memory-card", "x": 1079, "y": 279, "click": true},
   {"t": 14.17, "label": "memory-page"}]}
```

- `t` is seconds from the start of the recording, `x`/`y` are pixels in the recording (multiply by the device pixel ratio if needed).
- Log page changes and finished states too (`scan-done`), since shots start and end on them.
- A `sync` event at a visible moment (the first frame that changes) lets you check the clock against the video.

## Stills

When a state can't be recorded live, use a real screenshot of it at the same window size. Real screenshots are fine;
drawn ones never are.
