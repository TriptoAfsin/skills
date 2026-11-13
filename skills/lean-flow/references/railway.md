# Railway CLI

Command details: Railway's own skills (`deploy`, `deployment`, `environment`, `service`, `status`, `new`) and
`railway-docs`. These are the house rules on top of them.

## Before anything

- `railway whoami` and `railway status`: confirm the project and environment. Several client projects share one account.
- **Always pass `--service <name>`.** Projects often hold several services (for example a `docs` and a `landing`
  service), and the linked default is often the wrong one.
- The repo's AGENTS.md usually names the service, project ID and domain. Read it first.

## Deploys

- Most services deploy automatically from GitHub on push to `main`, **so pushing is deploying**. Treat a push to `main` as a deploy.
- `railway up` is only for a one-off deploy of uncommitted work, always with `--service`, and only on my yes.
- Redeploy, restart, remove and rollback all need my yes.
- After a deploy: follow `railway logs --service <name>` until it's healthy, then check the live URL (see verify-e2e.md).

## Variables

- `railway variables --service <name>`: report names only, never values, and never paste the output into chat or files.
- Adding or changing a variable needs my yes. A new variable also goes in the repo's `.env.example` and its env validation (`lib/env.ts`).
- Next.js `NEXT_PUBLIC_*` values are inlined at build time, so changing one means rebuilding.

## Gotchas

- Next.js on Railway reads `PORT`, so don't hard-code 3000.
- A build that passes locally can fail if it reaches the database at build time. Builds must work with an unreachable DB.
