<#
run_setup_nginx_downloads.ps1

Wrapper to run setup_nginx_ssl.ps1 against the downloaded nginx distribution
and capture the full output to `setup_nginx_downloads_log.txt` in the repo root.

Usage (Run PowerShell as Administrator):
  .\run_setup_nginx_downloads.ps1
  # Or pass a different nginx root:
  .\run_setup_nginx_downloads.ps1 -NginxRoot 'C:\path\to\nginx'
#>

param(
  [string]$NginxRoot = 'C:\Users\work8\Downloads\nginx-1.29.3\nginx-1.29.3'
)

function Fail([string]$msg, [int]$code=1) { Write-Error $msg; exit $code }

# Ensure running elevated
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
  Fail "Please re-run this script in an elevated (Administrator) PowerShell session." 10
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$setupScript = Join-Path $scriptDir 'setup_nginx_ssl.ps1'
if (-not (Test-Path $setupScript)) { Fail "Required file not found: $setupScript" 11 }

Write-Output "Running setup script: $setupScript against nginx root: $NginxRoot"
$logPath = Join-Path $scriptDir 'setup_nginx_downloads_log.txt'
if (Test-Path $logPath) { Remove-Item $logPath -Force }

# Execute and capture
powershell -ExecutionPolicy Bypass -File $setupScript -NginxRoot $NginxRoot 2>&1 | Tee-Object $logPath

Write-Output "--- Script output saved to: $logPath ---"
Write-Output "Displaying last 300 lines of log:"
Get-Content $logPath -Tail 300 | ForEach-Object { Write-Output $_ }

Write-Output "If the log contains 'nginx -t' errors, paste the full log here for diagnosis."