param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath
)

if (-not (Test-Path -LiteralPath $FilePath)) {
    Write-Error "File not found: $FilePath"
    exit 1
}

$fullPath = (Resolve-Path -LiteralPath $FilePath).Path
$content = Get-Content -LiteralPath $fullPath -Raw -Encoding utf8
$original = $content

$summary = [ordered]@{
    File                          = $fullPath
    AddedSharedGlobalCss          = $false
    ReplacedNavWithSharedMount    = $false
    ReplacedFooterWithSharedMount = $false
    AddedSharedLoaderScript       = $false
    Saved                         = $false
}

# 1) Add shared/global.css after GA script (fallback: before </head>)
if ($content -notmatch 'href="shared/global\.css"') {
    $gaPattern = '(?is)(<!--\s*Google tag \(gtag\.js\)\s*-->.*?<script[^>]*gtag/js\?id=[^"]+"[^>]*></script>\s*<script>.*?</script>)'
    if ([regex]::IsMatch($content, $gaPattern)) {
        $content = [regex]::Replace(
            $content,
            $gaPattern,
            '${1}' + "`r`n  <link rel=""stylesheet"" href=""../shared/global.css"">",
            1
        )
    }
    elseif ($content -match '</head>') {
        $content = [regex]::Replace(
            $content,
            '</head>',
            "  <link rel=`"stylesheet`" href=`"shared/global.css`">`r`n</head>",
            1
        )
    }
    $summary.AddedSharedGlobalCss = $content -ne $original -and ($content -match 'href="shared/global\.css"')
}

# 2) Replace nav with shared mount
if ($content -notmatch '<div id="shared-navbar"></div>') {
    $navMarkerPattern = '(?is)<!--\s*NAVBAR\s*-->\s*<nav\b[^>]*>.*?</nav>'
    $newNavBlock = "<!-- NAVBAR -->`r`n<div id=`"shared-navbar`"></div>"

    if ([regex]::IsMatch($content, $navMarkerPattern)) {
        $content = [regex]::Replace($content, $navMarkerPattern, $newNavBlock, 1)
        $summary.ReplacedNavWithSharedMount = $true
    }
    else {
        $plainNavPattern = '(?is)<nav\b[^>]*>.*?</nav>'
        if ([regex]::IsMatch($content, $plainNavPattern)) {
            $content = [regex]::Replace($content, $plainNavPattern, $newNavBlock, 1)
            $summary.ReplacedNavWithSharedMount = $true
        }
    }
}

# 3) Replace footer with shared mount
if ($content -notmatch '<div id="shared-footer"></div>') {
    $footerMarkerPattern = '(?is)<!--\s*FOOTER\s*-->\s*<footer\b[^>]*>.*?</footer>'
    $newFooterBlock = "<!-- FOOTER -->`r`n<div id=`"shared-footer`"></div>"

    if ([regex]::IsMatch($content, $footerMarkerPattern)) {
        $content = [regex]::Replace($content, $footerMarkerPattern, $newFooterBlock, 1)
        $summary.ReplacedFooterWithSharedMount = $true
    }
    else {
        $plainFooterPattern = '(?is)<footer\b[^>]*>.*?</footer>'
        if ([regex]::IsMatch($content, $plainFooterPattern)) {
            $content = [regex]::Replace($content, $plainFooterPattern, $newFooterBlock, 1)
            $summary.ReplacedFooterWithSharedMount = $true
        }
    }
}

# 4) Add shared loader script before </body>
if ($content -notmatch 'function\s+ensureSharedNavigationCss\s*\(') {
    $loaderScript = @'
  <script>
  function ensureSharedNavigationCss() {
    if (document.getElementById('shared-navigation-css')) return;
    const link = document.createElement('link');
    link.id = 'shared-navigation-css';
    link.rel = 'stylesheet';
    link.href = '../shared/navigation.css';
    document.head.appendChild(link);
  }

  async function loadSharedNavigation() {
    const mountPoint = document.getElementById('shared-navbar');
    if (!mountPoint) return;
    try {
      ensureSharedNavigationCss();
      const response = await fetch('../shared/navigation.html');
      if (!response.ok) throw new Error('Navigation load failed');
      const html = await response.text();
      mountPoint.innerHTML = html;
      initNavbarBehavior();
    } catch (error) {
      console.error('Unable to load shared navigation:', error);
    }
  }

  async function loadSharedFooter() {
    const mountPoint = document.getElementById('shared-footer');
    if (!mountPoint) return;
    try {
      const response = await fetch('../shared/footer.html');
      if (!response.ok) throw new Error('Footer load failed');
      const html = await response.text();
      mountPoint.innerHTML = html;
    } catch (error) {
      console.error('Unable to load shared footer:', error);
    }
  }

  function initNavbarBehavior() {
    const nav = document.getElementById('navLinks');
    const hamburger = document.getElementById('hamburger');
    if (nav && hamburger) {
      hamburger.addEventListener('click', function() {
        nav.classList.toggle('active');
      });
      document.addEventListener('click', function(e) {
        if (!nav.contains(e.target) && !hamburger.contains(e.target)) {
          nav.classList.remove('active');
        }
      });
    }
  }

  loadSharedNavigation();
  loadSharedFooter();
  </script>
'@

    if ($content -match '</body>') {
        $content = [regex]::Replace($content, '(?is)</body>', "`r`n$loaderScript`r`n</body>", 1)
        $summary.AddedSharedLoaderScript = $true
    }
}

if ($content -ne $original) {
    Set-Content -LiteralPath $fullPath -Value $content -Encoding utf8
    $summary.Saved = $true
}

Write-Output "Migration summary:"
$summary.GetEnumerator() | ForEach-Object {
    Write-Output ("- {0}: {1}" -f $_.Key, $_.Value)
}

