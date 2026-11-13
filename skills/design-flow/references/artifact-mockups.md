# Mock-ups as a live Artifact

One Artifact holds every direction, so the user compares them in one place and the same URL gets updated on each round.
(Agents without an Artifact tool: write one self-contained HTML file to a scratch folder and give its path.)

## Page structure

1. **Brief**: the five-line brief from intake.
2. **Direction switcher**: tabs or a segmented control (A / B / C) with each direction's name, plus a side-by-side "Compare" view on wide screens.
3. **For each direction**:
   - the mock-up itself at **desktop width (~1440)** and in a **390 px phone frame**, using real content
   - hallmark's preview bullets: macrostructure · theme (palette + type) · sections · motion
   - one line on why it fits the brief, and one line on what it trades away
4. **Light / dark toggle** if the product needs both.
5. **What happens next**: "Pick one, mix two, or tell me what to change."

## Rules

- Mock-ups are static HTML/CSS with only the motion that matters for choosing (a hover, a hero entrance). Full motion comes after the choice.
- Each direction defines its own tokens on a scoped root (`.dir-a { --paper: …; --accent: … }`), so the choices can't bleed into each other.
- Use real fonts (Google Fonts) and real copy. No lorem ipsum and no grey boxes standing in for content the brief already has.
- Run hallmark's slop test on each direction before publishing. Don't show a direction that fails it.
- After publishing, give the link and ask the choose question right away (SKILL.md, step 4).

## Iterating

- The user's notes go into the same file. Republish to the **same URL**, never a new one.
- Keep rejected directions in a collapsed "Earlier" section so the user can go back to one.
- Once a direction is chosen, add a "Chosen" badge and keep the page as the design record. Link to it from the PR.
