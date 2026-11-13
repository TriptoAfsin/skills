---
name: design-flow
description: Run a UI design from brief to shipped code in a fixed order - ask the intake questions one at a time, mock up two or three distinct directions as a live Artifact, let the user choose, lock the chosen system into DESIGN.md, then build, polish and verify. Orchestrates hallmark first (direction, anti-slop, DESIGN.md; installed automatically if missing), frontend-design (implementation), emil-design-eng and make-interfaces-feel-better (polish and motion). Use when designing or redesigning a page, screen, flow, landing page, dashboard or component, when the user says "design", "mock up", "prototype", "redesign" or "make it look good", or before writing any new UI.
---

# design-flow

Nothing reaches the codebase until the user has seen it and picked it. The order is fixed:

| # | Step | Uses | Details |
|---|---|---|---|
| 0 | Pre-flight: what already exists | the repo | below |
| 1 | Intake, **one question at a time** | question UI | [references/intake.md](references/intake.md) |
| 2 | Two or three distinct directions | `hallmark` (+ `hallmark study` for references) | below |
| 3 | Mock-ups as one live Artifact | Artifact tool | [references/artifact-mockups.md](references/artifact-mockups.md) |
| 4 | The user chooses, then iterate on the same Artifact | question UI | below |
| 5 | Lock the system into `DESIGN.md` | `hallmark` "lock the system" | below |
| 6–8 | Build → polish → verify | `frontend-design`, `emil-design-eng`, `make-interfaces-feel-better`, `lean-flow` | [references/handoff.md](references/handoff.md) |

## Skills it hands off to: check, install if missing

**`hallmark` is the first choice** for directions, the slop test, `study`, `redesign`, `audit` and locking
`DESIGN.md`. Prefer it over any other design skill that's installed. Before step 2, check that each handoff skill is
installed (`npx skills ls -g`, or look in the agent's skills folder). If one is missing, install it from its official
source before using it, and say so in one line:

| Skill | Step | Install |
|---|---|---|
| `hallmark` (required) | 2, 5, 8 | `npx skills add nutlope/hallmark -g -y` |
| `frontend-design` | 6 | `npx skills add anthropics/skills --skill frontend-design -g -y` |
| `emil-design-eng` | 7 | `npx skills add emilkowalski/skill -g -y` |
| `make-interfaces-feel-better` | 7 | `npx skills add jakubkrehel/make-interfaces-feel-better -g -y` |
| `lean-flow` | 8 | `npx skills add TriptoAfsin/skills --skill lean-flow -g -y` |

A skill installed in the middle of a session may only load in the next one. If it isn't available yet, read its
`SKILL.md` from the install folder and follow it directly. If an install fails (offline, blocked), say so and carry
on with the step by hand, but never skip hallmark's slop test.

## 0. Pre-flight

Look before asking: `DESIGN.md` / `design.md`, a tokens or theme file, `components.json` (shadcn), existing pages, brand assets.
- **An established product with a design system:** that system is fixed. Directions differ in layout, hierarchy and
  motion, not in palette or fonts, and the work counts as a `hallmark redesign` within the existing implementation.
- **Greenfield:** everything is open.
Tell the user in one line what you found, so they don't get asked about things the repo already answers.

## 2. Directions

Follow hallmark's design flow (genre → macrostructure → theme → slop test) to produce **two or three directions that
differ on at least two axes** (macrostructure, tone, palette, type). Three near-identical variants waste the step.
If the user gave a URL or screenshot, run `hallmark study` on it first and make one direction from its DNA.
Label each direction with hallmark's preview bullets (macrostructure, theme, sections, motion).

## 4. Choose

Ask with the question UI: one option per direction (recommended first, with the reason), plus "Mix: …" as an option
when two directions have parts worth combining. The user's notes on an option are instructions: apply them, republish
the **same** Artifact URL, and ask again. Stop iterating after two rounds without convergence and ask which single thing is still wrong.

## 5. Lock

Write the chosen system to `DESIGN.md` (hallmark's `design-md.md` format: tokens, type scale, voice, components,
do/don't). If `DESIGN.md` already exists, propose the diff and apply it only on a yes.

## Rules

- **Intake questions: one per question-UI call, recommended option first. Never bundle them**, even though hallmark's
  own gate bundles three. Skip any question the repo or brief already answers. "Go ahead" means infer the rest and say what you picked.
- Mock-ups use **real content** from the brief or repo, never lorem ipsum.
- Never edit code before step 4 has a choice. Before editing, list the files you'll create or modify (hallmark's safety rail). Deletions need a yes.
- For established products, finish with a `before-after` image.
