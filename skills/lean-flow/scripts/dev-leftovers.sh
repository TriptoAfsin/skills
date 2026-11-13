#!/bin/sh
# Lists dev servers, automated browsers and Docker containers that are still running (macOS and Linux).
# Report only: it never stops anything. Run it before starting work and again at the end, and compare.
# Usage: sh scripts/dev-leftovers.sh        (Windows: scripts/dev-leftovers.ps1)

DEV='^(node|bun|deno|python[0-9.]*|uv|cargo|java|dotnet|php|ruby|go|esbuild|vite|next-server)$'

short() { cut -c1-110; }

echo '== Listening dev servers'
found=0
if command -v lsof >/dev/null 2>&1; then
  # COMMAND PID ... NAME (host:port)
  lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print $1, $2, $9}' | sort -u |
  while read -r name pid addr; do
    port=${addr##*:}
    [ "$port" -ge 1024 ] 2>/dev/null || continue
    echo "$name" | grep -Eqi "$DEV" || continue
    cmd=$(ps -o args= -p "$pid" 2>/dev/null | short)
    printf '  %-6s %-7s %-10s %s\n' "$port" "$pid" "$name" "$cmd"
  done
elif command -v ss >/dev/null 2>&1; then
  ss -ltnpH 2>/dev/null | while read -r _ _ _ local _ users; do
    port=${local##*:}
    [ "$port" -ge 1024 ] 2>/dev/null || continue
    name=$(echo "$users" | sed -n 's/.*(("\([^"]*\)".*/\1/p')
    pid=$(echo "$users" | sed -n 's/.*pid=\([0-9]*\).*/\1/p')
    echo "$name" | grep -Eqi "$DEV" || continue
    cmd=$(ps -o args= -p "$pid" 2>/dev/null | short)
    printf '  %-6s %-7s %-10s %s\n' "$port" "$pid" "$name" "$cmd"
  done
else
  echo '  neither lsof nor ss is installed'
fi | { out=$(cat); if [ -n "$out" ]; then echo "$out"; else echo '  none'; fi; }

echo '== Automated / headless browsers'
ps -axo pid=,args= 2>/dev/null |
  grep -Ei 'chrome-headless-shell|(chrome|chromium|msedge|Google Chrome).*(--headless|ms-playwright|--remote-debugging-port|playwright)' |
  grep -v -- '--type=' | grep -v grep | short |
  { out=$(cat); if [ -n "$out" ]; then echo "$out" | sed 's/^ */  /'; else echo '  none'; fi; }

echo '== Docker containers'
if command -v docker >/dev/null 2>&1; then
  if out=$(docker ps --format '{{.ID}}  {{.Names}}  {{.Image}}  {{.Status}}  {{.Ports}}' 2>/dev/null); then
    if [ -n "$out" ]; then echo "$out" | sed 's/^/  /'; else echo '  none'; fi
  else
    echo '  Docker daemon not running'
  fi
else
  echo '  docker not installed'
fi
