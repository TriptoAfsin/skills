# Teams, WhatsApp, email, text files

| | Teams | WhatsApp | Email | Text file / SMS |
|---|---|---|---|---|
| Bold | rich paste | `*x*` | rich paste | none |
| Bullets | rich paste | `- ` | rich paste | `- ` |
| Links | rich paste | `text: url` | rich paste | `text (url)` |
| Greeting | from the style | from the style | from the style, after the subject | as asked |
| Length | bullets OK | short; split long ones into two messages | can be longer | as needed |

## Teams

- Use `fmt.py --to teams --copy`. Teams turns pasted HTML into real bold and lists, while pasted Markdown stays literal
  (`**x**`). Without the clipboard, the printed Markdown only formats if it's typed in, not pasted.
- @mentions must be retyped in Teams to notify anyone.
- Chats don't keep tables reliably, so use bullets. Channel posts can take a short bold subject line.

## WhatsApp

- `fmt.py --to whatsapp`: `*bold*`, `_italic_`, `~strike~`, `` `code` ``, `- ` and `1. ` lists. There are no
  link labels, so links become `text: url`.
- Keep it to one screen. Split a long update into two messages and say so.
- No @mentions or tables. In a group, address the person by name.

## Email

- First line of the draft: `Subject: ...`. Then the greeting, bullets, a closing line, and a name line if the user signs
  emails.
- `fmt.py --to email --copy` gives rich HTML for Outlook and Gmail, and the plain text is a fallback.
- Attach screenshots instead of linking local files.

## Text file / SMS

- `fmt.py --to text --out <file>`: no markup, `- ` bullets, links as `text (url)`.
- SMS: shortest version, one or two sentences, no bullets.
