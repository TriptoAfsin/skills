# Report: the end-of-task summary, and how to change it

Every task ends with a short status summary, so the user can see at a glance what happened without reading the whole
answer. This also covers stopping partway: hitting a blocker, needing a decision, or running out of what can be done
without the user.

## Default

Put it at the end of the final message, after any evidence. Three sections, in this order, one line per item:

```markdown
✅ **Done**
- Fixed the login redirect; `npm test` passes (42/42), checked in the browser at 1440 and 390
- Opened PR #118

⏳ **Left**
- Add the E2E test for the logout flow

🚧 **Blocked**
- Deploy to Railway: needs your yes (rule 3)
- Stripe webhook test: needs the test-mode signing secret name, I don't know which one to use
```

- **✅ Done:** what was finished *and checked*. Something that wasn't verified goes under Left, not Done.
- **⏳ Left:** what still needs doing, which you (the agent) can pick up next.
- **🚧 Blocked:** what's waiting on the user or on missing information. Say **who or what** it's waiting on and
  **exactly what's needed** to unblock it.
- One plain line per item. No paragraphs, no repeating the explanation from above.
- Leave out an empty section. If everything is done, the summary is just ✅ Done.
- Skip the summary for a quick question or a one-line answer where there's nothing to track.

## Changing it

Create an override file. Only the lines you write replace the default; everything else stays as above.

- For yourself, everywhere: `~/.agents/lean-flow.md`
- For one repo: `.agents/lean-flow.md` at the repo root (wins over the global file)

Read the repo file first, then the global one, then fall back to the default.

```markdown
# lean-flow report

- Sections: Shipped, Next, Waiting on you
- Emojis: 🟢 🟡 🔴   (or "none")
- Position: top of the message
- Format: table with columns Item | Status | Owner
- Also include: time spent, links to PRs and deploys
- Skip when: the answer is under 5 lines
```

Any field can be left out. Free-form lines ("Always link the ticket", "Write the summary in German") also apply.
