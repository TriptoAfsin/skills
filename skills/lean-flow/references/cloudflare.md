# Cloudflare (wrangler)

Command details: Cloudflare's official skills (`cloudflare`, `wrangler`, `workers-best-practices`, plus the
product-specific ones). Load `wrangler` before running commands. These are the house rules on top of `cli.md`.
Flags were checked against wrangler 4.x `--help` in November 2026.

## Before anything

- Use the repo's wrangler (`npx wrangler` / `bunx wrangler`), not a global one, so the version matches the lockfile.
- `wrangler whoami`: confirm the account. If the login can see several accounts, the config's `account_id` (or
  `CLOUDFLARE_ACCOUNT_ID`) decides which one, so check that it's set.
- Read `wrangler.jsonc` / `wrangler.toml` first: the Worker name, `env.*` blocks, bindings (D1, R2, KV, Queues,
  Durable Objects), routes and custom domains. The config is the source of truth. Change it and commit, rather than
  changing things in the dashboard.

## Environments

- `--env <name>` selects an `env.<name>` block. **Leaving out `--env` uses the top-level config**, which in many repos
  is production. Say which environment you're targeting before every write.
- Bindings aren't inherited by environments. Each `env` block needs its own, so a binding missing in staging is a
  config bug, not a reason to point staging at production data.

## Local vs remote data

- `wrangler dev` runs locally (Miniflare) with local D1/R2/KV storage.
- **D1, R2 and KV commands have `--local` and `--remote`.** Don't rely on the default. Always pass the flag you mean, and treat
  `--remote` as a remote write when the command changes data.
- D1 migrations: create with `wrangler d1 migrations create`, test with `apply --local`, then
  `apply --remote --env <name>` on my yes. Never edit a migration that has already been applied remotely. Add a new one.
- `wrangler d1 execute --remote` with a write (`INSERT`/`UPDATE`/`DELETE`/`DROP`) counts as destructive (see `cli.md`
  §2). Prefer `--command "SELECT ..."` reads with a `LIMIT`.

## Deploys

- Preview first: `wrangler deploy --dry-run` (builds and checks, uploads nothing).
- `wrangler versions upload` uploads a version without sending it traffic. It's the safe way to stage a change. A
  gradual rollout or a full deploy needs my yes.
- Pages projects deploy from git or `wrangler pages deploy`. If the repo deploys on push, **pushing is deploying**, the
  same as Railway.
- After deploying: `wrangler tail --env <name>` while you hit the live URL, then follow `verify-e2e.md` §6.
  Rollback (`wrangler rollback`) needs my yes.

## Secrets and variables

- `wrangler secret put <NAME> --env <name>` prompts for the value. Never pass it on the command line or through `echo`.
- `wrangler secret list` shows names only. That's all that should reach the chat.
- Local secrets live in `.dev.vars` / `.env` (gitignored). Never read them into chat, but do keep a `.dev.vars.example`.
- Plain `vars` belong in the config and are public. Anything sensitive must be a secret.

## Gotchas

- R2 bucket names, D1 database IDs and KV namespace IDs differ per environment. Check the binding before running a
  data command.
- Deleting a bucket, database, namespace or Worker, purging the cache, or changing DNS or routes is destructive:
  my yes, with the account and zone named.
- For security products (WAF, Turnstile, rate limiting, Zero Trust), suggest them and don't configure them on your own.
