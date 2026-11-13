# Lists dev servers, automated browsers and Docker containers that are still running.
# Report only: it never stops anything. Run it before starting work and again at the end, and compare.
# Usage: powershell -NoProfile -File scripts/dev-leftovers.ps1

$devNames = @('node', 'bun', 'deno', 'python', 'pythonw', 'uv', 'cargo', 'java', 'dotnet', 'php', 'ruby', 'go', 'esbuild')

function Short([string]$s, [int]$n) {
    if (-not $s) { return '' }
    $s = $s -replace '\s+', ' '
    if ($s.Length -gt $n) { return $s.Substring(0, $n - 1) + '...' }
    return $s
}

Write-Output '== Listening dev servers'
$procs = @{}
Get-CimInstance Win32_Process | ForEach-Object { $procs[[int]$_.ProcessId] = $_ }
$rows = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $_.LocalPort -ge 1024 } |
    Sort-Object OwningProcess, LocalPort -Unique |
    ForEach-Object {
        $p = $procs[[int]$_.OwningProcess]
        if ($p) {
            $name = [IO.Path]::GetFileNameWithoutExtension($p.Name)
            if ($devNames -contains $name.ToLower()) {
                [pscustomobject]@{ Port = $_.LocalPort; PID = $_.OwningProcess; Name = $name; Command = (Short $p.CommandLine 110) }
            }
        }
    }
if ($rows) { $rows | Format-Table -AutoSize | Out-String -Width 220 } else { Write-Output '  none' }

Write-Output '== Automated / headless browsers'
$browsers = $procs.Values | Where-Object {
    $_.Name -match '^chrome-headless-shell' -or
    (($_.Name -match '^(chrome|msedge|chromium)\.exe$') -and ($_.CommandLine -match '--headless|ms-playwright|--remote-debugging-port|playwright'))
} | Where-Object { $_.CommandLine -notmatch '--type=' }
if ($browsers) {
    $browsers | ForEach-Object { [pscustomobject]@{ PID = $_.ProcessId; Name = $_.Name; Command = (Short $_.CommandLine 110) } } |
        Format-Table -AutoSize | Out-String -Width 220
} else { Write-Output '  none' }

Write-Output '== Docker containers'
if (Get-Command docker -ErrorAction SilentlyContinue) {
    $out = & docker ps --format '{{.ID}}  {{.Names}}  {{.Image}}  {{.Status}}  {{.Ports}}' 2>$null
    if ($LASTEXITCODE -ne 0) { Write-Output '  Docker daemon not running' }
    elseif ($out) { $out | ForEach-Object { "  $_" } }
    else { Write-Output '  none' }
} else { Write-Output '  docker not installed' }
