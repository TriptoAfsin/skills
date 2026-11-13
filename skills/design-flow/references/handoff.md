# Build, polish, verify

Only after the user has picked a direction and `DESIGN.md` is locked.

## 6. Build: `frontend-design` + the repo

- Port the chosen mock-up into the repo's own stack, tokens and components (shadcn primitives, Tailwind theme, CSS
  variables). Don't paste the mock-up's HTML wholesale.
- Every colour, radius and font comes from the `DESIGN.md` tokens, never a raw hex in a component.
- Follow the repo's architecture playbook and AGENTS.md. A repo's own rules beat this skill.
- List the files you'll create or modify before editing. Deletions need a yes.

## 7. Polish: `emil-design-eng` + `make-interfaces-feel-better`

Go through these in order and fix what fails:
1. **Should it animate at all?** (emil's decision framework). Remove motion that has no purpose.
2. Motion that stays: purpose → easing → duration, interruptible (CSS transitions over keyframes), `prefers-reduced-motion` respected, never animating from `scale(0)`.
3. The make-interfaces-feel-better checklist: concentric radius, optical alignment, shadows over borders, tabular
   numbers, `text-wrap: balance`, hit areas ≥ 40 px, no `transition: all`, scale on press.
4. Report using emil's review format: what changed and why, in a short list.

## 8. Verify: `lean-flow`

- `lean-flow` → `references/verify-e2e.md`: build, browser at 1440 and 390, no horizontal scroll, no console or hydration errors.
- `hallmark audit` on the result: the slop test must still pass after the port.
- Compare against the chosen Artifact. Note any intentional differences.
- For an established product: run `before-after` and attach the image to the PR or message.
- Clean up servers and browsers (`lean-flow` → cleanup).
