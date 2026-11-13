# Intake questions

Ask **one per call** with the agent's question UI (Claude Code: AskUserQuestion), in this order. Put the recommended
option first with "(Recommended)" and a one-line reason. Skip a question when the repo or brief already answers it, and
say which answer you took from where. Each answer can change or remove the next question, so read it before asking another.

| # | Ask | Example options (adapt to the brief) | Skip when |
|---|---|---|---|
| 1 | **What are we designing, and how big?** | Whole page · one section · a flow (several screens) · a single component | The brief names it exactly |
| 2 | **Who uses it, and what's the one action?** | Offer 2–3 concrete audience + action pairs inferred from the brief (e.g. "Landlords · book a call") | The product's docs or AGENTS.md say so |
| 3 | **Tone: pick an extreme** | hallmark's list: editorial · modern-minimal · atmospheric · playful (plus brutalist, luxury, technical, austere when they fit). "Clean and modern" is not a tone | An established design system fixes it |
| 4 | **Any references?** | "I'll paste a URL or screenshot" · "Use the existing site" · "No references, surprise me" | Already attached (then ask: study it, or treat it as loose inspiration?) |
| 5 | **Must-haves and no-gos** | Common ones for the brief (dark mode, Bangla support, a specific brand colour, no stock photos, must work at 390 px) | Nothing is likely to be ruled in or out |
| 6 | **How many directions?** | 3 directions (Recommended) · 2 directions · 1 refined direction (when the system is fixed) | The system is fixed: then default to 2 layout variants |

## "Go ahead" or no answer

Infer the remaining answers from the brief and the repo, list them in one line ("I picked: landlords → book a call,
editorial tone, no references"), and move on to the directions. Don't ask again.

## After intake

Write a five-line brief (what, who, action, tone, constraints) at the top of the Artifact so the user sees what the
directions are answering.
