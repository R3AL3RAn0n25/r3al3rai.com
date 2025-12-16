# R3ÆLƎR AI Enterprise Storage Presentation Markdown to PDF Converter
# Converts comprehensive markdown presentation to professional PDF format

param(
    [string]$InputFile = "R3ALER_AI_Enterprise_Storage_Presentation.md",
    [string]$OutputFile = "R3ALER_AI_Enterprise_Storage_Presentation.pdf",
    [string]$BrowserPath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    [string]$TempHtmlFile = "temp_presentation.html"
)

Write-Host "R3ÆLƎR AI Enterprise Storage Presentation PDF Converter" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# Check if input file exists
if (!(Test-Path $InputFile)) {
    Write-Host "Error: Input file '$InputFile' not found!" -ForegroundColor Red
    exit 1
}

# Get full paths
$InputPath = Resolve-Path $InputFile
$OutputPath = Join-Path (Get-Location) $OutputFile
$TempHtmlPath = Join-Path (Get-Location) $TempHtmlFile

Write-Host "Input File: $InputPath" -ForegroundColor Yellow
Write-Host "Output File: $OutputPath" -ForegroundColor Yellow
Write-Host "Temp HTML File: $TempHtmlPath" -ForegroundColor Yellow

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

# Step 1: Convert Markdown to HTML
Write-Host "Step 1: Converting markdown to HTML..." -ForegroundColor Green

try {
    $markdownContent = Get-Content -Path $InputPath -Raw

    # Create HTML template with professional styling
    $htmlTemplate = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>R3ÆLƎR AI Enterprise Storage Presentation</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Source+Code+Pro:wght@400;500;600&display=swap');

        body {
            font-family: 'Inter', 'Calibri', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            max-width: 1100px;
            margin: 0 auto;
            padding: 40px;
            background-color: #ffffff;
            font-size: 14px;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', 'Calibri', sans-serif;
            font-weight: 600;
            color: #000000;
            margin-top: 2.2em;
            margin-bottom: 0.8em;
            page-break-after: avoid;
            line-height: 1.1;
            letter-spacing: -0.01em;
        }

        h1 {
            font-size: 3.2em;
            font-weight: 800;
            text-align: center;
            color: #b91c1c;
            border-bottom: 5px solid #b91c1c;
            padding-bottom: 0.5em;
            margin-bottom: 2em;
            margin-top: 1em;
            letter-spacing: -0.02em;
            text-transform: uppercase;
            font-feature-settings: "kern" 1;
        }

        h2 {
            font-size: 2.4em;
            font-weight: 700;
            color: #1e40af;
            border-left: 8px solid #1e40af;
            padding-left: 25px;
            margin-top: 3em;
            margin-bottom: 1em;
            letter-spacing: -0.01em;
            text-transform: uppercase;
            font-size-adjust: 0.5;
        }

        h3 {
            font-size: 1.8em;
            font-weight: 600;
            color: #059669;
            margin-top: 2.5em;
            margin-bottom: 0.8em;
            border-bottom: 2px solid #d1fae5;
            padding-bottom: 0.3em;
        }

        h4 {
            font-size: 1.3em;
            font-weight: 500;
            color: #1a202c;
        }

        p {
            margin: 1.2em 0;
            font-size: 1em;
            line-height: 1.7;
            color: #4a5568;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 2em 0;
            background-color: #ffffff;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
            page-break-inside: avoid;
        }

        th, td {
            border: 1px solid #d1d5db;
            padding: 18px 20px;
            text-align: left;
            font-size: 0.95em;
            vertical-align: top;
        }

        th {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            font-weight: 700;
            color: #111827;
            font-size: 1em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 2px solid #9ca3af;
        }

        tr:nth-child(even) {
            background-color: #f8fafc;
        }

        tr:hover {
            background-color: #edf2f7;
        }

        code {
            font-family: 'Source Code Pro', 'Consolas', 'Monaco', 'Courier New', monospace;
            background-color: #f1f5f9;
            color: #dc2626;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.85em;
            font-weight: 500;
            border: 1px solid #e2e8f0;
            letter-spacing: 0.02em;
        }

        pre {
            font-family: 'Source Code Pro', 'Consolas', 'Monaco', monospace;
            background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
            color: #f9fafb;
            padding: 25px;
            border-radius: 12px;
            overflow-x: auto;
            margin: 2em 0;
            page-break-inside: avoid;
            font-size: 0.9em;
            line-height: 1.6;
            border: 1px solid #4b5563;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }

        pre code {
            background-color: transparent;
            padding: 0;
            border: none;
            color: inherit;
            font-size: inherit;
        }

        .highlight {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 6px solid #d97706;
            padding: 20px 25px;
            margin: 2em 0;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 4px 12px rgba(217, 119, 6, 0.1);
        }

        .success {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border-left: 6px solid #059669;
            padding: 20px 25px;
            margin: 2em 0;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 4px 12px rgba(5, 150, 105, 0.1);
        }

        .warning {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 6px solid #d97706;
            padding: 20px 25px;
            margin: 2em 0;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 4px 12px rgba(217, 119, 6, 0.1);
        }

        .error {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-left: 6px solid #dc2626;
            padding: 20px 25px;
            margin: 2em 0;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);
        }

        ul, ol {
            margin: 1.2em 0;
            padding-left: 2em;
        }

        li {
            margin: 0.6em 0;
            line-height: 1.6;
        }

        blockquote {
            border-left: 6px solid #1e40af;
            padding-left: 25px;
            margin: 2em 0;
            font-style: italic;
            color: #4b5563;
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            padding: 20px 25px;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 4px 12px rgba(30, 64, 175, 0.1);
            font-weight: 500;
        }

        .architecture-diagram {
            text-align: center;
            margin: 2.5em 0;
            page-break-inside: avoid;
        }

        .architecture-diagram pre {
            text-align: left;
            display: inline-block;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border: 2px solid #9ca3af;
            border-radius: 12px;
            font-family: 'Source Code Pro', 'Consolas', monospace;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }

        strong {
            font-weight: 600;
            color: #1a202c;
        }

        em {
            font-style: italic;
            color: #4a5568;
        }

        a {
            color: #3182ce;
            text-decoration: none;
            font-weight: 500;
        }

        a:hover {
            text-decoration: underline;
        }

        @media print {
            body {
                background-color: white;
                max-width: none;
                margin: 0;
                padding: 20px;
                font-size: 14px;
            }

            .page-break {
                page-break-before: always;
            }

            table {
                page-break-inside: avoid;
            }

            pre {
                page-break-inside: avoid;
                font-size: 11px;
            }

            h1 {
                font-size: 2.5em;
            }

            h2 {
                font-size: 1.8em;
            }

            h3 {
                font-size: 1.4em;
            }
        }
    </style>
</head>
<body>
"@

    # Convert markdown to basic HTML (simple conversion)
    $htmlContent = $markdownContent

    # Convert headers
    $htmlContent = $htmlContent -replace '^# (.+)$', '<h1>$1</h1>'
    $htmlContent = $htmlContent -replace '^## (.+)$', '<h2>$1</h2>'
    $htmlContent = $htmlContent -replace '^### (.+)$', '<h3>$1</h3>'
    $htmlContent = $htmlContent -replace '^#### (.+)$', '<h4>$1</h4>'

    # Convert bold and italic
    $htmlContent = $htmlContent -replace '\*\*(.+?)\*\*', '<strong>$1</strong>'
    $htmlContent = $htmlContent -replace '\*(.+?)\*', '<em>$1</em>'

    # Convert code blocks
    $htmlContent = $htmlContent -replace '```(\w+)?\n(.*?)\n```', '<pre><code>$2</code></pre>'
    $htmlContent = $htmlContent -replace '`([^`]+)`', '<code>$1</code>'

    # Convert links
    $htmlContent = $htmlContent -replace '\[([^\]]+)\]\(([^)]+)\)', '<a href="$2">$1</a>'

    # Convert lists (basic)
    $htmlContent = $htmlContent -replace '^-\s+(.+)$', '<li>$1</li>'
    $htmlContent = $htmlContent -replace '(?m)^(\d+)\.\s+(.+)$', '<li>$2</li>'

    # Convert paragraphs
    $htmlContent = $htmlContent -split '\n\n'
    $processedContent = @()
    foreach ($paragraph in $htmlContent) {
        if ($paragraph -notmatch '^<(h[1-6]|ul|ol|li|pre|table)') {
            $processedContent += "<p>$($paragraph -replace '\n', '<br>')</p>"
        } else {
            $processedContent += $paragraph
        }
    }
    $htmlContent = $processedContent -join "`n"

    # Wrap lists
    $htmlContent = $htmlContent -replace '(<li>.*?</li>\s*)+', '<ul>$&</ul>'

    # Final HTML assembly
    $finalHtml = $htmlTemplate + $htmlContent + "`n</body>`n</html>"

    # Write HTML file
    $finalHtml | Out-File -FilePath $TempHtmlPath -Encoding UTF8

    Write-Host "HTML conversion completed successfully!" -ForegroundColor Green

} catch {
    Write-Host "Error during markdown to HTML conversion: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 2: Convert HTML to PDF using browser
Write-Host "Step 2: Converting HTML to PDF..." -ForegroundColor Green
Write-Host "This may take a moment due to the comprehensive content..." -ForegroundColor Yellow

$arguments = @(
    "--headless",
    "--disable-gpu",
    "--print-to-pdf=`"$OutputPath`"",
    "--print-to-pdf-no-header",
    "--print-to-pdf-no-footer",
    "--print-to-pdf-fit-to-page",
    "`"$TempHtmlPath`""
)

try {
    $process = Start-Process -FilePath $BrowserPath -ArgumentList $arguments -Wait -PassThru -NoNewWindow

    if ($process.ExitCode -eq 0) {
        Write-Host "Enterprise storage presentation PDF conversion completed successfully!" -ForegroundColor Green
        Write-Host "Output saved to: $OutputPath" -ForegroundColor Green

        # Get file size
        $fileSize = (Get-Item $OutputPath).Length
        $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
        Write-Host "File size: $fileSizeMB MB" -ForegroundColor Cyan

        # Clean up temp file
        if (Test-Path $TempHtmlPath) {
            Remove-Item $TempHtmlPath -Force
            Write-Host "Temporary HTML file cleaned up." -ForegroundColor Gray
        }

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

Write-Host "`nThe R3ÆLƎR AI Enterprise Storage Presentation PDF is ready!" -ForegroundColor Magenta
Write-Host "This comprehensive presentation includes:" -ForegroundColor White
Write-Host "  ✅ Complete enterprise storage architecture overview" -ForegroundColor Green
Write-Host "  ✅ Domain isolation and hot-swap scaling details" -ForegroundColor Green
Write-Host "  ✅ Evolution engine and performance optimization" -ForegroundColor Green
Write-Host "  ✅ Security architecture and compliance features" -ForegroundColor Green
Write-Host "  ✅ Deployment procedures and business value proposition" -ForegroundColor Green
Write-Host "  ✅ Professional presentation formatting for enterprise pitching" -ForegroundColor Green

Write-Host "`nReady for enterprise presentation delivery! 🚀" -ForegroundColor Magenta