# Style: the default, and how to change it

## Default (the author's own)

- **Short and to the point.** Answer first, no warm-up, no recap of what they said, no "hope you're well".
- **Greeting:** `Salam @Name,` followed by one short line of context on the same line.
- **Body:** bullets that start with a **bold label**, then one or two plain sentences each. A single point goes
  without bullets.
- **Closing:** one friendly, practical line ("Shout if anything looks off.", "I'll check back at 4.").
- **No emojis.** No exclamation marks unless the thread is casual.
- **Length budgets:**

| Destination | Budget |
|---|---|
| Slack, Teams chat | ≤ 80 words, ≤ 4 bullets |
| Teams channel post | ≤ 120 words, optional bold subject line |
| WhatsApp | ≤ 60 words, split longer ones into two messages |
| Email | ≤ 150 words plus `Subject:` |
| SMS | 1–2 sentences |
| One point to a teammate | 1–2 sentences |

- **By audience:**

| Audience | Tone |
|---|---|
| Client | Full structure, plain words, no internal detail, only what's live |
| Teammate, one to one | Shortest form, technical words fine |
| Manager | Result first, then what's left and who it's blocked on |
| Group or channel | Address people by name for asks, nothing private |

## Changing it

Create a style file. Only the lines you write override the default, everything else stays as above.

- For yourself, everywhere: `~/.agents/team-reply.md`
- For one project or client: `STYLE.md` in its drafts folder (for example `.messages/STYLE.md`)

```markdown
# Reply style

- Greeting: "Hi {name}," (or "none")
- Closing: "Thanks, Sam"
- Emojis: one at most, only in Slack
- Budgets: Slack 60 words; WhatsApp 40 words; email 200 words
- Language: English, or match the thread's language
- Always: link the ticket ID when there is one
- Never: promise dates without a ticket

## People
- Alex: Slack, client, non-technical, wants screenshots
- Priya: Teams, teammate, technical
```

The `People` list is how the destination and tone get remembered per person. Add to it when you learn something new
(with the user's OK), instead of asking again.
