# GitHub CLI (`gh`)

## Before anything

- Work usually spans several orgs (employers, clients, your own). Run `git remote -v` and pass `-R owner/repo` when the
  target isn't obvious. If a home repo or AGENTS.md lists the orgs, check it.
- `gh auth status` if a call returns 404 on a private repo. It's usually the wrong account or a missing org SSO grant.

## Commits and branches

- Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `perf:`, `ci:`, scope optional.
  Summary under ~72 characters in the imperative mood, with a body that explains why. One logical change per commit.
- Branch off the default branch for anything that will become a PR. Never commit directly to `main` on team repos unless that's the repo's convention.
- Never `--no-verify`, never force-push a shared branch, never rewrite pushed history without asking.

## PRs

```bash
gh pr create --fill-first --base main        # then edit the body
gh pr view --web                             # only if I ask to open it
gh pr checks --watch                         # wait for CI rather than polling by hand
```

PR body: what changed and why, how it was verified (commands and screenshots, `before-after` for UI changes on
established products), and anything left over. Don't @-mention people unless I name them.

## CI

```bash
gh run list -L 5
gh run view <id> --log-failed | tail -80     # failed steps only, capped
gh run watch <id> --exit-status
```

## Releases

Prefer the repo's own release script (e.g. `bun run release patch`). Otherwise:
`gh release create vX.Y.Z --generate-notes`, only on my yes. Tags follow SemVer `vX.Y.Z`.

## API and output size

- Use `--json <fields> --jq '<filter>'` so output stays small. Don't dump whole JSON objects.
- Security advisories for a dependency:
  `gh api "/advisories?ecosystem=npm&affects=<pkg>@<version>" --jq '.[] | "\(.severity) \(.ghsa_id) \(.summary)"'`
  Mention critical and high ones. Suggest the fix, don't apply it (see `~/.agents/AGENTS.md`, Security).
