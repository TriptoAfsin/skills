# Collecting the conversation

Ground the reply in what was actually said. Prefer a connector or CLI that reads the source directly. Otherwise ask
the user to paste the thread or send a screenshot. Don't write a reply to a thread you haven't seen.

| Source | How to read it |
|---|---|
| Slack | The Slack connector (search the person, read the thread). See [slack.md](slack.md) |
| Microsoft Teams | A Teams or Graph connector if one is installed. Otherwise ask the user to paste the chat (copying a message keeps the sender and time) |
| WhatsApp | Ask the user to paste the chat, use "Export chat" (a .txt), or send a screenshot |
| Email | A mail connector (Gmail or Outlook) if installed: read the whole thread, not just the last message. Otherwise ask for a paste |
| Ticket or PM tool | Its connector or CLI, for the issue's current status before you claim anything about it |
| Screenshot | Read it as an image. Ask about anything you can't make out, don't guess names or numbers |

## What to pull out

1. Every question or ask, in order, quoted short. The reply must cover all of them.
2. Facts they gave: names, numbers, dates, links.
3. What's already been promised, by whom.
4. Their language, register and length. Match them (a two-line question gets a short answer).
5. Who else is reading (a channel, a group, a Cc).

## When the facts aren't there

If answering needs information you don't have (is it deployed? what's the ETA?), check it first: the repo, CI, the
deploy or the ticket. If you can't check, write "I'll confirm by <time>" rather than guessing, and tell the user what's
missing.

## Not found

The person may be in another workspace, or a shared channel this login can't see. Say so in one line and work from
what the user pastes. Don't keep searching.
