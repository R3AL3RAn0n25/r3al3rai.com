# R3ÆLƎR AI Master Presentation PDF Converter
# Converts comprehensive master presentation to professional PDF format

param(
    [string]$InputFile = "R3ALER_AI_MASTER_PRESENTATION.html",
    [string]$OutputFile = "R3ALER_AI_MASTER_PRESENTATION.pdf",
    [string]$BrowserPath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
)

Write-Host "R3ÆLƎR AI Master Presentation PDF Converter" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check if input file exists
if (!(Test-Path $InputFile)) {
    Write-Host "Error: Input file '$InputFile' not found!" -ForegroundColor Red
    exit 1
}

# Get full paths
$InputPath = Resolve-Path $InputFile
$OutputPath = Join-Path (Get-Location) $OutputFile

Write-Host "Input File: $InputPath" -ForegroundColor Yellow
Write-Host "Output File: $OutputPath" -ForegroundColor Yellow

# Check if browser exists
if (!(Test-Path $BrowserPath)) {
    Write-Host "Warning: Microsoft Edge not found at default path. Trying Chrome..." -ForegroundColor Yellow
    $BrowserPath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    if (!(Test-Path $BrowserPath)) {
        Write-Host "Error: Neither Edge nor Chrome found. Please install a Chromium-based browser." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Using browser: $BrowserPath" -ForegroundColor Green

# Create PDF using browser headless mode with print settings optimized for presentation
$arguments = @(
    "--headless",
    "--disable-gpu",
    "--print-to-pdf=`"$OutputPath`"",
    "--print-to-pdf-no-header",
    "--print-to-pdf-no-footer",
    "--print-to-pdf-fit-to-page",
    "`"$InputPath`""
)

Write-Host "Converting master presentation HTML to PDF..." -ForegroundColor Green
Write-Host "This may take a moment due to the comprehensive content..." -ForegroundColor Yellow

try {
    $process = Start-Process -FilePath $BrowserPath -ArgumentList $arguments -Wait -PassThru -NoNewWindow

    if ($process.ExitCode -eq 0) {
        Write-Host "Master presentation PDF conversion completed successfully!" -ForegroundColor Green
        Write-Host "Output saved to: $OutputPath" -ForegroundColor Green

        # Get file size
        $fileSize = (Get-Item $OutputPath).Length
        $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
        Write-Host "File size: $fileSizeMB MB" -ForegroundColor Cyan

    } else {
        Write-Host "Error: PDF conversion failed with exit code $($process.ExitCode)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error during PDF conversion: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`nConversion Summary:" -ForegroundColor Cyan
Write-Host "- Input: $InputFile" -ForegroundColor White
Write-Host "- Output: $OutputFile" -ForegroundColor White
Write-Host "- Browser: $(Split-Path $BrowserPath -Leaf)" -ForegroundColor White
Write-Host "- Status: SUCCESS" -ForegroundColor Green

Write-Host "`nThe R3ÆLƎR AI Master Presentation PDF is ready!" -ForegroundColor Magenta
Write-Host "This comprehensive presentation includes:" -ForegroundColor White
Write-Host "  ✅ Complete benchmark suite results" -ForegroundColor Green
Write-Host "  ✅ Links to detailed PDF reports" -ForegroundColor Green
Write-Host "  ✅ Demo video reference and instructions" -ForegroundColor Green
Write-Host "  ✅ Screenshots placeholders and descriptions" -ForegroundColor Green
Write-Host "  ✅ Professional presentation formatting" -ForegroundColor Green
Write-Host "  ✅ Enterprise-ready validation and metrics" -ForegroundColor Green