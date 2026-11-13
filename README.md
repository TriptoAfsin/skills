# skills

Agent skills I use every day, packaged so any agent that supports the open
[Agent Skills](https://agentskills.io) format can install them: Claude Code, Codex, Cursor and others.

## Skills

| Skill | What it does |
|---|---|
| [`lean-flow`](skills/lean-flow) | The dev loop around the code: GitHub CLI, verification and E2E with playwright-cli, Railway deploys and variables, and cleaning up dev servers, browsers and Docker containers afterwards |

## Install

With the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add TriptoAfsin/skills --skill lean-flow -g     # global, for every project
npx skills add TriptoAfsin/skills --skill lean-flow        # current project only
```

Or by hand: copy `skills/lean-flow/` into `~/.claude/skills/` (Claude Code) or your agent's skills folder.

Update later with `npx skills update -g`.

## lean-flow

The loop I run around every change: **check it, ship it, leave the machine tidy.**
It holds conventions only. Command details come from the vendor skills it points to
(`playwright-cli`, Railway's official skills).

It uses progressive disclosure, so an agent loads a short `SKILL.md` every time and reads a reference only when it needs that one:

```
skills/lean-flow/
├── SKILL.md                 7 rules that always apply + which reference to read
├── references/
│   ├── github.md            remotes across orgs, commits, PRs, CI, releases, advisories
│   ├── verify-e2e.md        static → unit → build → browser at 1440 and 390 → E2E → after deploy
│   ├── railway.md           --service always, pushing to main means deploying, variable names only
│   └── cleanup.md           snapshot before and after, servers, browsers, Docker, Rust target/
└── scripts/
    └── dev-leftovers.ps1    lists dev servers, headless browsers and containers still running (Windows, report-only)
```

The rules that matter most:

- The repo's own verify and deploy rules win over these defaults.
- Push, deploy, merge, release and variable changes need the user's yes. On Railway, pushing to `main` usually *is* deploying.
- Never print secrets, and never submit forms against live credentials while testing.
- A task isn't done until it has been checked, and the evidence goes in the answer.
- Only clean up what you started.

## License

MIT
