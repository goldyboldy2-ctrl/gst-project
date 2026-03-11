$ErrorActionPreference = "Stop"

function U([int[]]$codes) {
    return -join ($codes | ForEach-Object { [char]$_ })
}

function E([int]$codePoint) {
    return [char]::ConvertFromUtf32($codePoint)
}

$blogFiles = Get-ChildItem -Path .\blog -Filter *.html

foreach ($file in $blogFiles) {
    Write-Host "Processing: $($file.Name)"

    $content = Get-Content $file.FullName -Raw -Encoding UTF8

    # STEP 1: Remove inline <style> blocks
    $content = $content -replace '<style>[\s\S]*?</style>', ''

    # STEP 2: Fix emoji encoding issues
    $content = $content -replace [regex]::Escape((U @(0x00E2,0x00BA))), ''
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0027))), (E 0x1F4A1)
    $content = $content -replace [regex]::Escape((U @(0x00E2))), (U @(0x20B9))
    $content = $content -replace [regex]::Escape((U @(0x00E2,0x0161,0x0020,0x00EF))), ''
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x00A7))), (E 0x1F9EE)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022,0x0161))), (E 0x1F4DA)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0161))), (E 0x1F680)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022,0x0160))), (E 0x1F4CA)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022))), (E 0x1F4D6)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022))), (E 0x1F4DD)
    $content = $content -replace [regex]::Escape((U @(0x00E2,0x0161,0x0020,0x00EF))), ''
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0027))), (E 0x1F4B0)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022))), (E 0x1F504)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022))), (E 0x1F4E6)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0027))), (E 0x1F4B3)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0027))), (E 0x1F4B8)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0161,0x0161))), (E 0x1F69A)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022))), (E 0x1F4C4)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022,0x0022))), (E 0x1F514)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022))), (E 0x1F50D)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022))), (E 0x1F522)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x0022))), (E 0x1F4C5)
    $content = $content -replace [regex]::Escape((U @(0x00E2,0x0161,0x2013,0x00EF))), ''
    $content = $content -replace [regex]::Escape((U @(0x00E2,0x0161))), ''
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178))), (E 0x1F195)
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178,0x2014,0x00EF))), (E 0x1F5C2)
    $content = $content -replace [regex]::Escape((U @(0x00E2))), ''
    $content = $content -replace [regex]::Escape((U @(0x00E2,0x0153))), ''
    $content = $content -replace [regex]::Escape((U @(0x00E2))), ''
    $content = $content -replace [regex]::Escape((U @(0x00E2,0x017E,0x00EF))), ''
    $content = $content -replace [regex]::Escape((U @(0x00E2,0x00EF))), ''
    $content = $content -replace [regex]::Escape((U @(0x00F0,0x0178))), (E 0x1F3C6)

    # STEP 3: Remove empty comment remnants
    $content = $content -replace '<!-- Header with Mobile Navigation -->\s*', ''
    $content = $content -replace '<!-- Breadcrumbs -->\s*', ''
    $content = $content -replace '<!-- NAVBAR -->\s+<!-- NAVBAR -->', '<!-- NAVBAR -->'
    $content = $content -replace '<!-- FOOTER -->\s+<!-- JAVASCRIPT -->', '<!-- FOOTER -->'
    $content = $content -replace '<!-- Mobile Menu Toggle Script -->\s*', ''

    # STEP 4: Remove duplicate empty lines (compress whitespace)
    $content = $content -replace '(\r?\n){3,}', "`r`n`r`n"

    # STEP 5: Save as UTF-8 without BOM
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($file.FullName, $content, $utf8NoBom)

    Write-Host " Fixed: $($file.Name)"
}

Write-Host "`nAll blog pages processed!"
