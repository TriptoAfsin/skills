# Verify and E2E

Close the loop yourself: change it, check it, read the result, fix it, then check again. Fix root causes. Never
suppress a lint or type error, or weaken a check, just to get a pass.

## Order

1. **Static:** typecheck (`tsc --noEmit`, `bun run typecheck`) and lint, both at zero errors.
2. **Unit tests:** whatever the repo uses (`vitest`, `bun test`, `jest`, `pytest`, `cargo test`). A bug fix gets a test that
   would have caught it. Check whether a git hook runs the tests; often none does, so run them yourself.
3. **Build:** must pass. In Next.js, watch for a route flipping from static `○` to dynamic `ƒ`, and the build must pass with an unreachable `DATABASE_URL`.
4. **Browser:** see below.
5. **E2E:** if the repo has a suite (`bunx playwright test`, `bun test:e2e`), run it for the flows you touched.
6. **After deploy:** for anything user-facing, check the live URL. Don't say "shipped" about a deploy you haven't verified.

## Browser checks

Use whichever browser tool the repo or user prefers: `playwright-cli`, `agent-browser`, the Claude in Chrome tools,
Chrome DevTools MCP or similar. If more than one is available and nothing says which, pick by the rules in
[cli.md](cli.md) §0. Load that tool's own skill for the command reference. The checks below are the same whatever the tool.

- Check two viewports: **1440×900 and 390×844**. Take a full-page screenshot of each and actually look at it.
- No horizontal scroll: `document.documentElement.scrollWidth === document.documentElement.clientWidth`.
- No console errors, no hydration errors, no framework error overlay (Next: `[data-nextjs-dialog]` count 0).
- New pages or hero changes: CLS < 0.1 (a `PerformanceObserver` on `layout-shift` over the first 5 s).
- Pages that receive ad traffic: also load them with `?utm_campaign=x&fbclid=y`, since hydration mismatches often show up only then.
- UI changes on an established product: `before-after` skill.

## Writing E2E tests

- Test what a user does (sign up → act → see the result), not implementation details. Use role and label locators over CSS.
- Each test sets up and tears down its own data and never depends on another test's leftovers.
- External services (Stripe, email, CRMs) use test modes or sandbox servers with the upstream variables blanked,
  never live credentials. A form wired to a live CRM gets its pure functions tested instead of being submitted.
- Put `browser.close()` in a `finally`.

## Where output goes

Screenshots, traces and scratch scripts go in the session scratchpad or the OS temp directory, never in the repo
(unless the repo's tests keep their own snapshots).
