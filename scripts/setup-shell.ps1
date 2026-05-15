# REGIQ local terminal bootstrap.
#
# Prepends the locally-installed Node.js 20 and Python 3.12 toolchains to
# $env:PATH for the current PowerShell session so `node`, `npm`, `python`,
# and `pip` resolve to the versions the CI pipeline targets.
#
# Usage:
#   . .\scripts\setup-shell.ps1
#
# The leading dot ("dot-source") is required so the PATH modification
# persists for the rest of the shell session instead of being scoped to
# the script's child process.

$ErrorActionPreference = 'Stop'

$nodeRoot   = 'C:\NodeJS-20'
$pythonRoot = 'C:\python-3.12.8'

$paths = @(
    $nodeRoot,
    $pythonRoot,
    (Join-Path $pythonRoot 'Scripts')
)

foreach ($p in $paths) {
    if (-not (Test-Path $p)) {
        Write-Warning "Path does not exist on this machine: $p"
        continue
    }
    if (-not (($env:PATH -split ';') -contains $p)) {
        $env:PATH = "$p;$env:PATH"
        Write-Host "Prepended to PATH: $p"
    } else {
        Write-Host "Already in PATH: $p"
    }
}

Write-Host ""
Write-Host "Tool versions in this shell:" -ForegroundColor Cyan

$tools = @(
    @{ Name = 'node';   Args = '--version' },
    @{ Name = 'npm';    Args = '--version' },
    @{ Name = 'python'; Args = '--version' },
    @{ Name = 'pip';    Args = '--version' }
)

foreach ($t in $tools) {
    try {
        $version = (& $t.Name $t.Args) 2>&1
        Write-Host ("  {0,-7} {1}" -f $t.Name, $version)
    } catch {
        Write-Warning ("{0} not resolvable: {1}" -f $t.Name, $_.Exception.Message)
    }
}

Write-Host ""
Write-Host "Ready. Try: cd backend; npm ci; npm test" -ForegroundColor Green
