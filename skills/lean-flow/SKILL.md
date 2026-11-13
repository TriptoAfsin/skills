---
name: lean-flow
description: House conventions for the dev loop around the code - GitHub CLI (repos across several orgs, PRs, releases, CI runs, advisories), verification and E2E testing (playwright-cli, agent-browser or whichever browser tool the user prefers), Railway CLI deploys and variables, Cloudflare wrangler (Workers, Pages, D1, R2, KV, secrets), choosing between tools by detecting the user's and repo's preference, safe use of any other platform CLI (supabase, vercel, stripe, eas, cloud CLIs - sort read/write/destructive, pin the target, dry-run first, secrets by name only), and cleaning up dev servers, browsers and Docker containers afterwards. Use when running gh, opening a PR or release, checking CI, verifying a change in the browser, writing or running E2E tests, deploying or inspecting a Railway service, running wrangler or any other platform CLI, choosing which tool to use for a job, or finishing a task that started servers or containers.
---

# lean-flow

These are the house rules. The command details live in the vendor skills (`playwright-cli`, Railway's `deploy` /
`deployment` / `environment` / `service` / `status`, `railway-docs`). Read only the reference you need:

| Doing | Read |
|---|---|
| Anything with `gh`: PRs, releases, CI, issues, API, advisories | [references/github.md](references/github.md) |
| Checking a change works: typecheck, unit, build, browser, E2E | [references/verify-e2e.md](references/verify-e2e.md) |
| Railway: deploy, logs, variables, services | [references/railway.md](references/railway.md) |
| Cloudflare: Workers, Pages, D1, R2, KV, secrets, deploys | [references/cloudflare.md](references/cloudflare.md) |
| Choosing between tools (e.g. playwright-cli vs agent-browser), or any other CLI (Supabase, Vercel, Stripe, EAS, cloud, Docker ...) | [references/cli.md](references/cli.md) |
| Finishing a task that started servers, browsers or containers | [references/cleanup.md](references/cleanup.md) |

## Always

0. **CLI first, and the user's own tools.** Prefer a CLI over a dashboard. When several tools could do the job,
   detect the one to use (user, then repo, then what's installed) and ask once only if it's still open
   ([cli.md](references/cli.md) §0).
1. **The repo's own rules win.** If the repo has a verify skill, `VERIFY.md`, `npm run verify` or deploy notes in its
   AGENTS.md, use those. These references are the defaults for repos that don't.
2. **Check which account and target a CLI points at before acting** (`git remote -v`, `gh auth status`,
   `railway status`, the tool's whoami), and pass the target explicitly on every write.
3. **Pushing, deploying, merging, releasing and changing variables need my yes**, unless I asked for that exact action.
   On Railway, pushing to `main` often *is* deploying.
4. **Never print secrets.** Report variable names or pass/fail, never values. Never read `.env` into chat.
5. **Never submit forms or fire webhooks against live credentials** while testing.
6. **A task isn't done until it has been checked**, and the evidence (command plus result, or a screenshot) goes in the answer.
7. **Leave the machine the way you found it.** Snapshot before (`scripts/dev-leftovers.ps1`), clean up after, and only stop what you started.
