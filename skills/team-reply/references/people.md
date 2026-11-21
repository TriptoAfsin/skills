# People directory: who's reading, and how to write to them

A reply lands better when it's written for the person: their name and title, their organization, how formal they are,
and how they like updates laid out. A people directory keeps that between sessions.

The style file names it: `- People directory: <path>`. Keep it in a **private** place (a private repo or a local
folder), never inside this skill or a public repo. It holds notes about real people.

## Layout

```
<people dir>/
  <org>/_org.md       what the organization is, how it relates to the user, house tone, vocabulary, roster
  <org>/<person>.md   one person the user has actually talked to
  <org>/groups.md     channels and group chats: who reads them, what goes there
```

## Before writing

1. Find the reader: match the name, nickname, chat ID or email against `<org>/<person>.md`. Not there: look in the
   roster in each `_org.md`.
2. Use the profile's **greeting, tone, length, format and platform**. A profile beats the style file, and the user's
   words in this session beat both.
3. Use `_org.md` for the organization's words (product names, locations, teams) and for what not to say.
4. For a group or channel, read `groups.md` to see who else is reading.
5. No profile: write in the default style and say so, so the user can correct it.

## Person file

```markdown
---
name: Full Name
goes_by: Nickname
org: <org folder>
title: Their title (and where it came from)
relation: client | manager | teammate | report | vendor, plus what you do for them
platform: Slack DM / Teams / WhatsApp / email, with IDs
timezone: Area/City
updated: YYYY-MM-DD
source: where this came from
---

## Who they are           two or three lines
## How to write to them   greeting, register, length, format, what works with them
## Working on together    current topics and open asks
```

## Building and keeping it current

- **Seed it from real messages:** read the user's own recent messages to that person (Slack DMs, threads) and copy how
  the user actually writes to them: greeting, length, structure, recurring phrases. Take titles from chat profiles
  and the organization's About page.
- Mark anything guessed (no real thread yet) as *unverified*, and replace it after the first real conversation.
- When a draft teaches something new (a preferred platform, a new title, an open ask), offer to update the profile.
- Never store passwords, API keys, phone numbers or private personal details. Work email and chat IDs are fine.
