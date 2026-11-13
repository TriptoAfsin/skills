# Cleanup

Clean up when the task is finished, including when it ended in failure. Only touch what you started.

## Snapshot first

Before starting servers, browsers or containers:

```powershell
powershell -NoProfile -File ~/.agents/skills/lean-flow/scripts/dev-leftovers.ps1
```

Run it again at the end and compare. Anything that was already running is mine: leave it alone and mention it.

## Checklist

1. **Dev servers** (`next dev/start`, `vite`, `bun --watch`, `tauri dev`, email previews): stop the ones you started.
   On Windows use `taskkill //PID <pid> //T //F` (`//T` also kills child processes), then confirm the port is free. Prefer the
   repo's own command (`npm run clean`, or a smoke script that stops its own server).
2. **Browsers:** close every Playwright or Chrome instance you launched, and check that no `chrome-headless-shell` or `ms-playwright` process is left.
3. **Docker:** stop and remove containers you started (`docker compose down` in that repo, `docker rm -f <id>`).
   Keep volumes unless they were throwaway test data you created. Never run `docker system prune` without asking.
4. **Test data:** remove throwaway databases (e.g. `.data/pglite-verify*`), test rows and test sheet tabs.
5. **Scratch files** in the repo: delete them, since they belong in the scratchpad.
6. **Worktrees:** once merged, run `git worktree remove <path>`, but only if `git status` there is clean. Never force it.

## Build artifacts

Rust/Tauri `target/` folders grow to tens of GB. Clean them only when the work is done **and** tests passed, never
in the middle of a task. Ask before deleting an installer or bundle I might need. Tell me what you removed and roughly how much space it freed.
