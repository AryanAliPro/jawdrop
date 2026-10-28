# Install the jawdrop skill into every AI coding agent found on this Windows machine.
#
#   irm https://raw.githubusercontent.com/AryanAliPro/jawdrop/main/install.ps1 | iex
#
# Set $env:JAWDROP_AGENTS = "claude-code,cursor" first to install into specific agents only.
# An existing jawdrop folder is moved to ~\.jawdrop-backups\<timestamp>\ first, so nothing is lost.

$ErrorActionPreference = 'Stop'
$Repo = 'AryanAliPro/jawdrop'
$Branch = if ($env:JAWDROP_BRANCH) { $env:JAWDROP_BRANCH } else { 'main' }
$Skill = 'jawdrop'
$H = $HOME

# Id, folder that shows the agent is installed, global skills folder
$Agents = @(
  @{ Id = 'claude-code';    Detect = "$H\.claude";               Dir = "$H\.claude\skills" },
  @{ Id = 'codex';          Detect = "$H\.codex";                Dir = "$H\.agents\skills" },
  @{ Id = 'cursor';         Detect = "$H\.cursor";               Dir = "$H\.cursor\skills" },
  @{ Id = 'antigravity';    Detect = "$H\.gemini\antigravity";   Dir = "$H\.gemini\antigravity\skills" },
  @{ Id = 'gemini-cli';     Detect = "$H\.gemini";               Dir = "$H\.gemini\skills" },
  @{ Id = 'windsurf';       Detect = "$H\.codeium\windsurf";     Dir = "$H\.codeium\windsurf\skills" },
  @{ Id = 'github-copilot'; Detect = "$H\.copilot";              Dir = "$H\.copilot\skills" },
  @{ Id = 'opencode';       Detect = "$H\.config\opencode";      Dir = "$H\.config\opencode\skills" },
  @{ Id = 'kiro';           Detect = "$H\.kiro";                 Dir = "$H\.kiro\skills" },
  @{ Id = 'trae';           Detect = "$H\.trae";                 Dir = "$H\.trae\skills" },
  @{ Id = 'roo';            Detect = "$H\.roo";                  Dir = "$H\.roo\skills" },
  @{ Id = 'agents';         Detect = "$H\.agents";               Dir = "$H\.agents\skills" }
)

if ($env:JAWDROP_AGENTS) {
  $wanted = $env:JAWDROP_AGENTS -split ',' | ForEach-Object { $_.Trim() }
  $targets = $Agents | Where-Object { $wanted -contains $_.Id }
} else {
  $targets = $Agents | Where-Object { Test-Path $_.Detect }
  if (-not $targets) { $targets = $Agents | Where-Object { @('claude-code', 'agents') -contains $_.Id } }
}

$tmp = Join-Path ([IO.Path]::GetTempPath()) ("jawdrop-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $tmp | Out-Null
try {
  Write-Host "Downloading $Repo ($Branch)..."
  $zip = Join-Path $tmp 'jawdrop.zip'
  Invoke-WebRequest -Uri "https://codeload.github.com/$Repo/zip/refs/heads/$Branch" -OutFile $zip -UseBasicParsing
  Expand-Archive -Path $zip -DestinationPath $tmp
  $src = Get-ChildItem -Path $tmp -Directory |
    ForEach-Object { Join-Path $_.FullName "skills\$Skill" } |
    Where-Object { Test-Path (Join-Path $_ 'SKILL.md') } |
    Select-Object -First 1
  if (-not $src) { throw "skills\$Skill not found in the download" }

  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $done = @{}
  foreach ($agent in $targets) {
    # Several agents share ~\.agents\skills; install there once.
    if ($done.ContainsKey($agent.Dir)) { Write-Host "installed  $($agent.Id) (shares $($agent.Dir))"; continue }
    $done[$agent.Dir] = $true

    New-Item -ItemType Directory -Force -Path $agent.Dir | Out-Null
    $dest = Join-Path $agent.Dir $Skill
    if (Test-Path $dest) {
      $backup = Join-Path $H ".jawdrop-backups\$stamp\$($agent.Id)"
      New-Item -ItemType Directory -Force -Path $backup | Out-Null
      Move-Item -Path $dest -Destination $backup
      Write-Host "backed up  previous $dest -> $backup\$Skill"
    }
    Copy-Item -Path $src -Destination $dest -Recurse
    Write-Host "installed  $($agent.Id) -> $dest"
  }
} finally {
  Remove-Item -Path $tmp -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Done. Restart your agent, then ask it to build a website, for example:"
Write-Host "  Build website for a family-run roofing company in Denver"
