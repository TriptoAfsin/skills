---
name: before-after
description: Before/after screenshots with annotations and markup - capture both states the same way with whatever browser or device tool is available, then render one clean PNG with numbered, color-coded boxes, circles, arrows, highlights, callout labels, redaction of private data and a plain-words legend. Also annotates a single screenshot ("where to click"). Use when the user asks for before/after screenshots, a visual changelog, "show what changed", an annotated or marked-up screenshot, or when reporting a visible UI change to a client, the team or a PR.
---

# Before/after screenshots

One image per change: **Before** and **After** side by side (or stacked for wide pages), every change marked and
numbered, with a plain-words legend under each side. The message that goes with it refers to the numbers ("see 2").
A single panel gives one annotated screenshot instead.

## Steps

1. **Capture both states the same way:** same page, account, data, viewport (desktop `1440x900`, phone `390x844`),
   theme and scroll position. Use the browser or device tool the user or repo prefers (playwright-cli, agent-browser,
   Chrome tools, agent-device, a screenshot they sent). Where Before comes from and how to get exact boxes:
   [references/capture.md](references/capture.md).
2. **Write `spec.json`** next to the shots and render (needs Python 3 with Pillow):
   ```bash
   python <this skill's folder>/scripts/compare.py spec.json      # -> compare.png
   ```
   ```json
   {"title": "Settings: Save moved to the header",
    "subtitle": "Acme Dashboard · Settings · 2026-11-13",
    "panels": [
      {"label": "Before", "image": "before.png",
       "marks": [{"box": [40, 600, 220, 56], "kind": "removed", "note": "Save sat at the bottom of a long form"}]},
      {"label": "After", "image": "after.png",
       "marks": [{"box": [1180, 20, 200, 56], "kind": "added", "shape": "circle", "note": "Save is always visible now"},
                 {"box": [40, 210, 380, 40], "shape": "redact"}]}]}
   ```
   Every field, shape and layout: [references/spec.md](references/spec.md).
3. **Look at the PNG** before handing it over: marks on the right element, text readable, nothing private showing.

## Markup at a glance

| Kind (colour) | Use for | | Shape | Use for |
|---|---|---|---|---|
| `added` green | new things | | `box` (default) | an element |
| `changed` amber | moved or reworded | | `circle` | a small target (icon, button) |
| `removed` red | gone (mark it on Before) | | `highlight` | text or a row |
| `note` blue | context, "click here" | | `arrow` | a move, or "look here" |
| | | | `redact` | private data: pixelated, no number |

Any numbered mark can also carry a `label`, a short callout drawn on the image itself.

## Rules

- One change per image, at most 3 marks per panel. Otherwise crop or split it into several images.
- Crop to the area that changed, with enough around it to show where it is.
- Mark the Before side too, so the two sides match up. Give the same element the same `n` on both sides.
- Legend notes are plain words for the reader, in the tone of the message they go with (`team-reply` skill).
- **Redact** emails, names, phone numbers, addresses, tokens and customer data unless the recipient owns them.
- Keep the shots out of git unless asked: a drafts folder (for example `.messages/shots/YYYY-MM-DD-<slug>/`,
  git-ignored) or the scratchpad.
