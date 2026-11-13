#!/usr/bin/env python3
"""Convert a Markdown message draft into the markup a destination expects, and optionally copy it.

    python fmt.py draft.md --to slack|teams|whatsapp|text|email [--copy] [--out file] [--max-words N]

The draft is plain Markdown: **bold**, *italic* or _italic_, ~~strike~~, `code`, [text](url), "- " or "1. " lists,
blank lines between paragraphs. Output per destination:

  slack     Slack mrkdwn text (*bold*, _italic_, ~strike~, <url|text>, bullets as "•"). With --copy the clipboard also
            gets rich HTML, which Slack pastes with real bold and bullet lists.
  teams     Markdown text. With --copy the clipboard gets rich HTML (Teams turns pasted HTML into bold and lists;
            pasted Markdown stays literal).
  whatsapp  WhatsApp text (*bold*, _italic_, ~strike~, `code`, "- " bullets, links as "text: url").
  text      Plain text, no markup ("- " bullets, links as "text (url)"). For .txt files, SMS and anywhere else.
  email     Same as text for the body; with --copy the clipboard also gets HTML for Outlook/Gmail.

--copy works on Windows (PowerShell clipboard with HTML + text) and falls back to plain text elsewhere (pbcopy/xclip).
"""
import argparse
import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BOLD = re.compile(r"\*\*(.+?)\*\*|__(.+?)__")
ITAL = re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])|(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])")
STRIKE = re.compile(r"~~(.+?)~~")
LINK = re.compile(r"\[([^\]]+)\]\((\S+?)\)")
CODE = re.compile(r"`([^`]+)`")
BULLET = re.compile(r"^(\s*)[-*+] +(.*)$")
NUMBER = re.compile(r"^(\s*)(\d+)[.)] +(.*)$")


def protect_code(s, render):
    """Swap inline code for placeholders so other rules don't touch it."""
    saved = []

    def keep(m):
        saved.append(render(m.group(1)))
        return "\x00%d\x00" % (len(saved) - 1)

    s = CODE.sub(keep, s)
    return s, lambda t: re.sub(r"\x00(\d+)\x00", lambda m: saved[int(m.group(1))], t)


def inline(s, to):
    if to == "slack":
        s, back = protect_code(s, lambda c: "`%s`" % c)
        s = LINK.sub(lambda m: "<%s|%s>" % (m.group(2), m.group(1)), s)
        s = BOLD.sub(lambda m: "\x01%s\x01" % (m.group(1) or m.group(2)), s)
        s = ITAL.sub(lambda m: "_%s_" % (m.group(1) or m.group(2)), s)
        s = STRIKE.sub(r"~\1~", s).replace("\x01", "*")
        return back(s)
    if to == "whatsapp":
        s, back = protect_code(s, lambda c: "`%s`" % c)
        s = LINK.sub(lambda m: m.group(1) if m.group(1) == m.group(2) else "%s: %s" % (m.group(1), m.group(2)), s)
        s = BOLD.sub(lambda m: "\x01%s\x01" % (m.group(1) or m.group(2)), s)
        s = ITAL.sub(lambda m: "_%s_" % (m.group(1) or m.group(2)), s)
        s = STRIKE.sub(r"~\1~", s).replace("\x01", "*")
        return back(s)
    if to in ("text", "email"):
        s, back = protect_code(s, lambda c: c)
        s = LINK.sub(lambda m: m.group(1) if m.group(1) == m.group(2) else "%s (%s)" % (m.group(1), m.group(2)), s)
        s = BOLD.sub(lambda m: m.group(1) or m.group(2), s)
        s = ITAL.sub(lambda m: m.group(1) or m.group(2), s)
        s = STRIKE.sub(r"\1", s)
        return back(s)
    return s  # teams: keep Markdown


def inline_html(s):
    s, back = protect_code(html.escape(s, quote=False), lambda c: "<code>%s</code>" % c)
    s = LINK.sub(lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), s)
    s = BOLD.sub(lambda m: "<b>%s</b>" % (m.group(1) or m.group(2)), s)
    s = ITAL.sub(lambda m: "<i>%s</i>" % (m.group(1) or m.group(2)), s)
    s = STRIKE.sub(r"<s>\1</s>", s)
    return back(s)


def blocks(md):
    """Yield ("p", [lines]) and ("ul"/"ol", [items]) blocks."""
    cur_kind, cur = None, []
    for raw in md.replace("\r\n", "\n").split("\n"):
        line = raw.rstrip()
        b, n = BULLET.match(line), NUMBER.match(line)
        kind = "ul" if b else "ol" if n else "p" if line.strip() else None
        if kind != cur_kind or kind is None:
            if cur:
                yield cur_kind, cur
            cur_kind, cur = kind, []
        if kind == "ul":
            cur.append(b.group(2))
        elif kind == "ol":
            cur.append(n.group(3))
        elif kind == "p":
            cur.append(line)
    if cur:
        yield cur_kind, cur


def to_text(md, to):
    out = []
    for kind, items in blocks(md):
        if kind == "p":
            out.append("\n".join(inline(l, to) for l in items))
        elif kind == "ul":
            mark = "•" if to == "slack" else "-"
            out.append("\n".join("%s %s" % (mark, inline(i, to)) for i in items))
        else:
            out.append("\n".join("%d. %s" % (k + 1, inline(i, to)) for k, i in enumerate(items)))
    return "\n\n".join(out) + "\n"


def to_html(md):
    parts = []
    for kind, items in blocks(md):
        if kind == "p":
            parts.append("<p>%s</p>" % "<br>".join(inline_html(l) for l in items))
        else:
            parts.append("<%s>%s</%s>" % (kind, "".join("<li>%s</li>" % inline_html(i) for i in items), kind))
    return "".join(parts)


def cf_html(fragment):
    """Wrap an HTML fragment in the Windows CF_HTML clipboard header."""
    head = "Version:0.9\r\nStartHTML:{0:010d}\r\nEndHTML:{1:010d}\r\nStartFragment:{2:010d}\r\nEndFragment:{3:010d}\r\n"
    pre = "<html><body><!--StartFragment-->"
    post = "<!--EndFragment--></body></html>"
    dummy = head.format(0, 0, 0, 0)
    start_html = len(dummy.encode())
    start_frag = start_html + len(pre.encode())
    end_frag = start_frag + len(fragment.encode())
    end_html = end_frag + len(post.encode())
    return head.format(start_html, end_html, start_frag, end_frag) + pre + fragment + post


def copy(text, fragment):
    if os.name == "nt":
        tmp = Path(tempfile.mkdtemp())
        (tmp / "t.txt").write_text(text, encoding="utf-8")
        ps = [
            "Add-Type -AssemblyName System.Windows.Forms",
            "$d = New-Object System.Windows.Forms.DataObject",
            "$d.SetData([System.Windows.Forms.DataFormats]::UnicodeText, [IO.File]::ReadAllText('%s', [Text.Encoding]::UTF8))" % (tmp / "t.txt"),
        ]
        if fragment:
            # CF_HTML offsets are UTF-8 byte counts; hand .NET the bytes as a stream so they stay exact.
            (tmp / "h.bin").write_bytes(cf_html(fragment).encode("utf-8"))
            ps.append("$d.SetData('HTML Format', (New-Object IO.MemoryStream(,[IO.File]::ReadAllBytes('%s'))))" % (tmp / "h.bin"))
        ps.append("[System.Windows.Forms.Clipboard]::SetDataObject($d, $true)")
        r = subprocess.run(["powershell", "-NoProfile", "-STA", "-Command", "; ".join(ps)], capture_output=True, text=True)
        if r.returncode:
            sys.exit("clipboard failed: " + r.stderr.strip())
        return "text + rich HTML" if fragment else "text"
    for cmd in (["pbcopy"], ["xclip", "-selection", "clipboard"], ["wl-copy"]):
        try:
            subprocess.run(cmd, input=text, text=True, check=True)
            return "text"
        except (OSError, subprocess.CalledProcessError):
            pass
    sys.exit("no clipboard tool found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--to", required=True, choices=["slack", "teams", "whatsapp", "text", "email"])
    ap.add_argument("--copy", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--quiet", action="store_true", help="don't print the converted text")
    ap.add_argument("--max-words", type=int, help="report OVER on stderr if the body is longer than this")
    a = ap.parse_args()
    md = Path(a.draft).read_text(encoding="utf-8")
    text = to_text(md, a.to)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    if not a.quiet:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text, end="")
    words = len(re.findall(r"\w[\w'’-]*", text))
    if a.max_words:
        state = "OK" if words <= a.max_words else "OVER by %d" % (words - a.max_words)
        print("\n[%d words, limit %d: %s]" % (words, a.max_words, state), file=sys.stderr)
    if a.copy:
        rich = to_html(md) if a.to in ("slack", "teams", "email") else None
        print("\n[copied to clipboard: %s]" % copy(text, rich), file=sys.stderr)


if __name__ == "__main__":
    main()
