<#
diag_checks.ps1

Runs quick diagnostics for the R3AL3R AI repo on Windows and prints
a copy/paste-ready DNS record snippet (A/AAAA) using detected public IPs.

Usage (PowerShell):
  .\diag_checks.ps1

This script performs checks but does NOT modify system files.
#>

Write-Output "=== R3AL3R AI Diagnostic Script ==="
Write-Output "Date: $(Get-Date -Format o)"
Write-Output "Working directory: $(Get-Location)"
Write-Output ""

function Section($title) { Write-Output ""; Write-Output "--- $title ---" }

Section "Python / Virtualenv"
$pythonCmd = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonCmd) { $pythonCmd = (Get-Command python3 -ErrorAction SilentlyContinue).Source }
Write-Output "Python on PATH: $($pythonCmd -ne $null)";
if ($pythonCmd) { & $pythonCmd --version 2>&1 | ForEach-Object { Write-Output "  $_" } }

$venvPython = Join-Path -Path $PSScriptRoot -ChildPath ".venv\Scripts\python.exe"
if (Test-Path $venvPython) { Write-Output "Found venv python: $venvPython"; & $venvPython --version 2>&1 | ForEach-Object { Write-Output "  $_" } }
else { Write-Output "No .venv python found at: $venvPython" }

Section "Search for hardcoded Unix Python paths in repo"
Write-Output "(searching for '/usr/bin' style references — may highlight shebangs)"
$patterns = @('/usr/bin/python','/usr/bin/python3','/usr/bin\\python','/usr/bin\\python3')
foreach ($p in $patterns) {
  $matches = Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | Select-String -Pattern $p -SimpleMatch -ErrorAction SilentlyContinue
  if ($matches) {
    Write-Output "Matches for '$p':"
    $matches | ForEach-Object { Write-Output "  $($_.Path):$($_.LineNumber): $($_.Line.Trim())" }
  }
}

Section "Nginx (if available)"
$nginxCmd = (Get-Command nginx -ErrorAction SilentlyContinue).Source
if (-not $nginxCmd) { # try common folder
  $candidates = @("C:\nginx\nginx.exe","$env:USERPROFILE\Downloads\nginx-*/nginx.exe")
  foreach ($c in $candidates) { if (Test-Path $c) { $nginxCmd = $c; break } }
}
if ($nginxCmd) {
  Write-Output "nginx executable: $nginxCmd"
  & $nginxCmd -t 2>&1 | ForEach-Object { Write-Output "  $_" }
} else { Write-Output "nginx not found on PATH or common locations." }

Section "Open ports 80/443 and local 5000"
Write-Output "Listening sockets relevant to 80/443/5000 (netstat output):"
try { netstat -ano | Select-String ':80\s|:443\s|:5000\s' | ForEach-Object { Write-Output "  $($_.ToString())" } } catch { Write-Output "  (netstat failed)" }

# If something is listening on 127.0.0.1:5000, show process
$listen5000 = netstat -ano | Select-String '127.0.0.1:5000' -ErrorAction SilentlyContinue
if ($listen5000) {
  foreach ($line in $listen5000) {
    $text = $line.ToString()
    Write-Output "  $text"
    $pid = ($text -split '\s+')[-1]
    if ($pid -match '^[0-9]+$') { Write-Output "    PID: $pid"; Get-Process -Id $pid -ErrorAction SilentlyContinue | ForEach-Object { Write-Output "    Process: $($_.ProcessName) (Id=$($_.Id))" } }
  }
} else { Write-Output "  No listener found on 127.0.0.1:5000" }

Section "Backend probe (127.0.0.1:5000)"
try {
  $r = Invoke-WebRequest -Uri 'http://127.0.0.1:5000/' -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
  Write-Output "  HTTP 127.0.0.1:5000 responded: $($r.StatusCode)"
  $body = $r.Content -split "\n" | Select-Object -First 6 -Skip 0
  Write-Output "  Body (first lines):"; $body | ForEach-Object { Write-Output "    $_" }
} catch { Write-Output "  Could not reach http://127.0.0.1:5000 — $($_.Exception.Message)" }

Section "HTTPS probe (www.r3al3rai.com) — certificate validation temporarily bypassed"
# Bypass cert validation for this probe only
try {
  add-type @"
using System.Net;
using System.Security.Cryptography.X509Certificates;
public class TrustAllCertsPolicy {
  public static bool Validate(object sender, X509Certificate certificate, X509Chain chain, System.Net.Security.SslPolicyErrors sslPolicyErrors) { return true; }
}
"@ -ErrorAction SilentlyContinue
  [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { param($sender,$cert,$chain,$errors) return $true }
  try {
    $resp = Invoke-WebRequest -Uri 'https://www.r3al3rai.com/' -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
    Write-Output "  HTTPS probe responded: $($resp.StatusCode)"
  } catch { Write-Output "  HTTPS probe failed: $($_.Exception.Message)" }
} catch { Write-Output "  Could not set temporary cert callback: $($_.Exception.Message)" }

Section "Public IPs (for DNS snippet)"
$ipv4 = $null; $ipv6 = $null
try { $ipv4 = Invoke-RestMethod -Uri 'https://api.ipify.org' -TimeoutSec 6 -ErrorAction Stop } catch { $ipv4 = $null }
try { $ipv6 = Invoke-RestMethod -Uri 'https://api6.ipify.org' -TimeoutSec 6 -ErrorAction Stop } catch { $ipv6 = $null }
Write-Output "  Detected public IPv4: $ipv4"
Write-Output "  Detected public IPv6: $ipv6"

Section "DNS record snippet (copy/paste-ready)"
if ($ipv4 -or $ipv6) {
  Write-Output "# Add these records at your DNS provider. Replace TTL if desired."
  if ($ipv4) {
    Write-Output "@    A     $ipv4    3600"
    Write-Output "www  A     $ipv4    3600"
  }
  if ($ipv6) {
    Write-Output "@    AAAA  $ipv6    3600"
    Write-Output "www  AAAA  $ipv6    3600"
  }
  Write-Output "# If your DNS provider needs a different format, use:"
  Write-Output "# example: `Type= A, Name=@, Value=$ipv4, TTL=3600`"
} else {
  Write-Output "Could not detect public IPs — ensure this machine has outbound access to api.ipify.org and try again." }

Section "Hints / Next steps"
Write-Output "- If nginx -t showed errors, open the config and fix paths (ssl_certificate, ssl_certificate_key)."
Write-Output "- To run the backend: activate your venv and run the runner: `& '.\.venv\Scripts\Activate.ps1'; python .\"R3AL3R Production\manage\runner.py"`"
Write-Output "- After updating DNS (A/AAAA), allow TTL to propagate and test https://www.r3al3rai.com"

Write-Output ""
Write-Output "=== End of diagnostic ==="
