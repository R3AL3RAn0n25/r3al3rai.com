# R3ÆLƎR AI - Stop All Services (Windows PowerShell)
# Gracefully stops all running services on Windows

Write-Host ""
Write-Host "================================================================" -ForegroundColor Magenta
Write-Host "    R3ÆLƎR AI - STOPPING ALL SERVICES (Windows)" -ForegroundColor Magenta
Write-Host "================================================================" -ForegroundColor Magenta
Write-Host ""

$ProjectRoot = $PSScriptRoot

# Function to stop process on port
function Stop-ProcessOnPort {
    param([int]$Port, [string]$ServiceName)
    
    try {
        $tcpConnections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
        if ($tcpConnections) {
            foreach ($conn in $tcpConnections) {
                $processId = $conn.OwningProcess
                if ($processId) {
                    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
                    if ($process) {
                        Write-Host "Stopping $ServiceName on port $Port (PID: $processId)..." -ForegroundColor Yellow
                        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                        Write-Host "   $ServiceName stopped" -ForegroundColor Green
                    }
                }
            }
        } else {
            Write-Host "$ServiceName not running on port $Port" -ForegroundColor Gray
        }
    } catch {
        Write-Host "Could not check/stop $ServiceName on port $Port" -ForegroundColor Yellow
    }
}

Write-Host "Stopping all R3AL3R AI services..." -ForegroundColor Cyan
Write-Host ""

# Stop all services by port
Stop-ProcessOnPort -Port 3003 -ServiceName "Storage Facility"
Stop-ProcessOnPort -Port 5004 -ServiceName "Knowledge API"
Stop-ProcessOnPort -Port 5010 -ServiceName "Intelligence API"
Stop-ProcessOnPort -Port 5005 -ServiceName "Droid API"
Stop-ProcessOnPort -Port 5006 -ServiceName "User Auth API"
Stop-ProcessOnPort -Port 8443 -ServiceName "RVN Privacy System"
Stop-ProcessOnPort -Port 3002 -ServiceName "BitXtractor"
Stop-ProcessOnPort -Port 5003 -ServiceName "BlackArch Tools"
Stop-ProcessOnPort -Port 5000 -ServiceName "Management System"
Stop-ProcessOnPort -Port 3000 -ServiceName "Backend Server"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "   ALL R3AL3R AI SERVICES STOPPED" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "All services have been stopped successfully." -ForegroundColor Green
Write-Host ""
