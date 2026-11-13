# CLI first, any tool

lean-flow works through CLIs: they're scriptable, their output is small and checkable, and they leave a trail you
can repeat. Prefer a CLI over clicking through a dashboard, and over an MCP or web UI when both do the job.

This file covers any CLI, especially those that reach a remote account: hosting, databases, DNS, storage, email,
payments, mobile builds, cloud. `github.md`, `railway.md` and `cloudflare.md` apply the same rules to their tools.

## 0. Pick the tool: detect, then ask

People use different tools for the same job. Don't assume a particular one.

| Job | Common choices |
|---|---|
| Browser automation, screenshots, E2E | `playwright-cli`, `agent-browser`, Claude in Chrome, Chrome DevTools MCP, the repo's Playwright/Cypress suite |
| Mobile and device | `agent-device`, `adb`, `xcrun simctl`, `eas`, Maestro |
| Hosting and deploys | `wrangler`, `vercel`, `railway`, `fly`, `netlify`, `gcloud`, `aws` |
| Database | `supabase`, `psql`, `neonctl`, `turso`, `wrangler d1`, the repo's migration tool |
| Email, payments, other services | `resend`, `stripe`, the vendor's own CLI |
| Containers | `docker`, `docker compose`, `podman` |

Work out which one to use in this order and stop at the first that answers:

1. **The user said so** in this session, or in their global preferences.
2. **The repo says so:** AGENTS.md or CLAUDE.md, `package.json` scripts, config files (`wrangler.jsonc`/`.toml`,
   `vercel.json`, `railway.json`, `fly.toml`, `supabase/`, `eas.json`, `playwright.config.*`, `compose.yaml`),
   CI workflows.
3. **What's installed:** `command -v <tool>` and the installed skills. A tool with a skill beats one without.
4. **Still a real choice between two or more?** Ask once, in the question UI, with the recommended option first and
   one line on why. Don't ask when only one fits, or when it's a quick read-only check either could do.

After asking, offer to save the answer to the repo's AGENTS.md (a project choice) or the user's global preferences
(a personal default), so the question isn't asked again. If no suitable CLI is installed, say which one you'd install
and from where (the vendor's official package) and wait for a yes.

## 1. Find the vendor's own guidance first

- Look for an official skill: `npx skills find <tool>`, and if there is one, load it before running commands.
- Flags change between major versions. Check `<tool> --help`, `<tool> <cmd> --help` or the docs (context7 or the
  vendor's site) before using a flag you haven't seen in this repo. Don't rely on memory.
- Use the repo's pinned version (`npx <tool>`, `bunx <tool>`, a script in `package.json`) over a global install.
  Upgrading a global CLI needs my yes.

## 2. Sort the command before running it

| Kind | Examples | Rule |
|---|---|---|
| Read | whoami, status, list, logs, `env ls`, `secret list`, describe | Run freely |
| Local | dev servers, emulators, `docker compose up`, local DB | Run, then clean up (`cleanup.md`) |
| Remote write | deploy, `db push`, set a variable or secret, DNS, create a bucket, publish a build | My yes, with the exact command shown first |
| Destructive or live | delete, drop, purge, reset, rollback, rotate a key, live payments, send real email or SMS | My yes **plus** the target named out loud (account, project, environment) |

If you're unsure which kind a command is, treat it as the next row down.

## 3. Pin the target

- Check who and where first: the tool's whoami, then which project, app, account or environment is linked.
- **Pass the target explicitly on every write.** Don't rely on the linked default, because several projects or clients
  often share one login.
- Know which environment the default hits. Some CLIs default to production, some to preview, test or local. If the
  repo doesn't say, check `--help` and state it before writing.
- Production and staging are separate targets. "It worked on staging" is not a yes for production.

## 4. Preview, then apply

- Use the tool's dry run, plan or diff before any remote write, and show me the result with the exact command.
- Prefer config as code: change the repo's config file or migration and commit it, rather than an imperative command
  that leaves the dashboard different from git. If you have to run one, say what drifted.
- After applying, check the result: status, logs or the live URL (`verify-e2e.md`), and put the evidence in the answer.

## 5. Secrets

- List names only (`secret list`, `env ls`). Never print values and never paste output that might contain them.
- Set secrets through the CLI's prompt or stdin, never as a command-line argument (it lands in shell history).
- Never `pull` remote env into a file you then read into chat. A new variable also goes in `.env.example` and the
  repo's env validation in the same change.
- A CLI login stays the user's. Don't log in, log out, switch accounts or create API tokens unless I ask.

## 6. Output and automation

- Prefer `--json` (or `-o json`) piped through `jq` with a cap, so output stays small. Add `--no-color` or
  `NO_COLOR=1` when parsing.
- Use the non-interactive flag (`--yes`, `--force`, `CI=1`) only for reads, or for a write I've already approved. It
  skips the CLI's own confirmation step.
- A command that will be repeated becomes a short script that only reports, saved in the repo.

## Per-tool quick reference

The wrangler, supabase and stripe rows were checked in November 2026. Confirm the others, and any tool whose major
version has changed since then, with `--help` before relying on them.

| Tool | Who / where | Target flag | Preview | Default to watch |
|---|---|---|---|---|
| Cloudflare `wrangler` | `wrangler whoami` | `--env <name>`; `--remote` for data | `wrangler deploy --dry-run` | See `cloudflare.md`: data commands are local unless `--remote` |
| Supabase `supabase` | `supabase projects list` | `--linked` / `--project-ref`; `--remote` in v3 | `supabase db push --dry-run` | CLI v3 runs against the **local** stack unless you pass `--remote` |
| Vercel `vercel` | `vercel whoami` | `--scope <team>` | Plain `vercel` makes a preview deploy | `--prod` deploys to production |
| Stripe `stripe` | `stripe config --list` | `--live` | Test mode is the default | `--live` touches real money: only on an explicit yes |
| Expo `eas` | `eas whoami` | `--profile <name>`, `--environment` | Build locally first | `eas submit` and `eas update` reach real users |
| Docker | `docker context ls` | `--context <name>` | `docker compose config` | The current context might be a remote host |
