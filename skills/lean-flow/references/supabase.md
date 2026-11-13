# Supabase CLI

Command details: `supabase <cmd> --help`, the official Supabase skills if installed (`npx skills find supabase`), and `supabase-postgres-best-practices` for SQL. These
are the house rules on top of `cli.md`. Checked against CLI **3.1** `--help` in November 2026. v3 changed targeting,
so re-check if the major version moves.

## Before anything

- Use the repo's version (a `supabase` devDependency, `npx supabase@<version>` or `bunx`) so everyone runs the same CLI.
- `supabase whoami` and `supabase projects list`: confirm the account. `supabase link --project-ref <ref>` links a
  project. Check which one is linked before any remote command, since one login often sees several projects.
- The local stack (`supabase start` / `stop` / `status`) needs Docker. Containers you start are yours to stop
  (`cleanup.md`).

## Local vs remote (v3)

- **Database commands run against the local stack unless you pass `--remote`.** That covers `db push`, `db diff`,
  `db reset`, `db dump`, `migration list/up/down/repair` and `gen types`. Bare `--remote` means the linked project.
  `--remote=<ref|branch|url>` picks another one.
- `secrets`, `functions deploy` and `link` are **remote only**, so they always hit the linked project.
- Write `--remote` explicitly when you mean it, and state the project ref before every remote write.
- `--yes` skips confirmations. For hosted changes it only works as a flag or an exported `SUPABASE_YES`, never from a
  `.env` file. Use it only after my yes.

## Migrations

| Step | Command | Rule |
|---|---|---|
| Create | `supabase migration new <name>`, or `supabase db diff -f <name>` from local changes | One logical change per migration |
| Test | `supabase db reset` (local), then the app and tests | Must apply cleanly from zero |
| Preview | `supabase db push --remote --dry-run` | Show me the list of migrations |
| Apply | `supabase db push --remote` | My yes, with the project ref named |
| Check | `supabase migration list --remote` | Local and remote histories match |

- Never edit a migration that has been applied remotely. Add a new one.
- `db push --include-all` (applies migrations missing from history) and `migration repair` rewrite history: my yes,
  and only once you understand why history drifted.
- `db reset --remote` wipes the remote database: **destructive**, never without an explicit yes naming the project.
- Generate types after a schema change: `supabase gen types --lang typescript --remote > <types file>` (or local).

## Secrets and functions

- `supabase secrets list` shows names and hashes only. That's all that should reach the chat.
- Set secrets from a gitignored file with `supabase secrets set --env-file <file>`, not `NAME=VALUE` on the command line
  (that lands in shell history). Never read that file into chat.
- `supabase functions deploy <name>` deploys to the linked project: my yes. `--prune` deletes remote functions that
  aren't in the repo, so it's destructive. `--no-verify-jwt` makes a function public: say so before using it.

## Gotchas

- `supabase/.env` is for local config. It isn't read for `--yes` and must never hold production secrets in git.
- Preview branches (`supabase branches`) are real remote databases: treat writes to them like any remote write.
- Row Level Security: a new table without RLS policies is open to the anon key. Flag it (see the security rules) rather
  than shipping it.
