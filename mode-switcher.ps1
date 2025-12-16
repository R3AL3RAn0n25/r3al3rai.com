<#
.SYNOPSIS
R3AL3R AI - Dev/Prod Mode Switcher PowerShell Wrapper

.DESCRIPTION
Convenient PowerShell wrapper for the mode_switcher.py CLI tool
Handles JWT token management and mode switching from Windows

.EXAMPLE
.\mode-switcher.ps1 status
.\mode-switcher.ps1 dev -Token "eyJhbGc..."
.\mode-switcher.ps1 toggle
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet('status', 'dev', 'prod', 'toggle', 'help')]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [string]$Token,
    
    [Parameter(Mandatory=$false)]
    [string]$Url = "http://localhost:3000"
)

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "mode_switcher.py"
$TokenFile = Join-Path $ScriptDir ".r3al3r_token"

function Show-Help {
    @"
╔══════════════════════════════════════════════════════════════╗
║      R3AL3R AI - Dev/Prod Mode Switcher (PowerShell)        ║
╚══════════════════════════════════════════════════════════════╝

SYNOPSIS
    .\mode-switcher.ps1 <command> [-Token <token>] [-Url <url>]

COMMANDS
    status    Show current mode and configuration
    dev       Switch to development mode
    prod      Switch to production mode
    toggle    Toggle between dev and production
    help      Show this help message

OPTIONS
    -Token <token>     JWT authentication token
                      If not provided, uses R3AL3R_JWT_TOKEN env var or .r3al3r_token file
    
    -Url <url>         API base URL (default: http://localhost:3000)
                      Example: http://localhost:3000 or https://api.r3aler.ai

EXAMPLES
    # Show current mode
    .\mode-switcher.ps1 status

    # Switch to development mode
    .\mode-switcher.ps1 dev

    # Toggle to production
    .\mode-switcher.ps1 toggle

    # Use custom token
    .\mode-switcher.ps1 status -Token "eyJhbGc..."

    # Use custom API URL
    .\mode-switcher.ps1 prod -Url "https://api.r3aler.ai"

TOKEN MANAGEMENT
    The tool looks for JWT token in this order:
    1. -Token parameter (if provided)
    2. R3AL3R_JWT_TOKEN environment variable
    3. .r3al3r_token file in current directory

    To save token for future use:
        # PowerShell
        [System.Environment]::SetEnvironmentVariable('R3AL3R_JWT_TOKEN', 'your_token_here', 'User')
        
        # Or create .r3al3r_token file
        'your_token_here' | Out-File -FilePath .r3al3r_token -Encoding UTF8 -NoNewline

QUICK START
    1. Get JWT token from login: Login to R3AL3R AI web interface
    2. Save token: \$env:R3AL3R_JWT_TOKEN = 'your_token_here'
    3. Check mode: .\mode-switcher.ps1 status
    4. Switch modes: .\mode-switcher.ps1 dev  (or prod, or toggle)

FOR MORE INFO
    See MODE_MANAGER_README.md for complete documentation
"@
}

function Invoke-ModeSwitcher {
    param(
        [string]$Command,
        [string]$Token,
        [string]$Url
    )
    
    # Build Python arguments
    $args = @($PythonScript, $Command)
    
    # Add URL if not default
    if ($Url -ne "http://localhost:3000") {
        $args += "--url", $Url
    }
    
    # Determine token source
    if ($Token) {
        $args += "--token", $Token
    } elseif ($env:R3AL3R_JWT_TOKEN) {
        $args += "--token", $env:R3AL3R_JWT_TOKEN
    } elseif (Test-Path $TokenFile) {
        $savedToken = Get-Content $TokenFile -Raw
        $args += "--token", $savedToken.Trim()
    } else {
        Write-Error "Error: JWT token not found. Provide -Token parameter or set R3AL3R_JWT_TOKEN environment variable"
        exit 1
    }
    
    # Run Python script
    python @args
}

# Main logic
switch ($Command) {
    'help' {
        Show-Help
    }
    'status' {
        Invoke-ModeSwitcher -Command $Command -Token $Token -Url $Url
    }
    'dev' {
        Invoke-ModeSwitcher -Command $Command -Token $Token -Url $Url
    }
    'prod' {
        Invoke-ModeSwitcher -Command $Command -Token $Token -Url $Url
    }
    'toggle' {
        Invoke-ModeSwitcher -Command $Command -Token $Token -Url $Url
    }
}
