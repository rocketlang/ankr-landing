# ankr-install - install.ps1 - one line for Windows (PowerShell 5.1+)
#   irm https://ankr.in/install/install.ps1 | iex
#   & ([scriptblock]::Create((irm https://ankr.in/install/install.ps1))) -WSL      (Ubuntu inside Windows + VS Code Remote-WSL)
# What it does, in order: Git for Windows (so hooks can run through Git Bash) -> Claude Code (Anthropic's own installer)
# -> the ANKR harness into %USERPROFILE%\.claude (backed up, merged, never reset) -> VS Code + the Claude Code extension
# -> the BYOK page -> the doctor. Flags: -WSL -NoIDE -NoByok -Check -NoClaude -HarnessFrom <dir>
# UNTESTED ON THE BUILD BOX (Linux): the first Windows run is the founder's laptop - every step prints what it did.
param([switch]$WSL, [switch]$NoIDE, [switch]$NoByok, [switch]$Check, [switch]$NoClaude, [string]$HarnessFrom = '')
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
try { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 } catch {}
$Base = if ($env:ANKR_INSTALL_BASE) { $env:ANKR_INSTALL_BASE } else { 'https://ankr.in/install' }
$ClaudeHome = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$S = Join-Path $ClaudeHome 'settings.json'

# The marks are built from code points so this file stays pure ASCII: Windows PowerShell 5.1 reads a BOM-less file (and an
# `irm` body without a charset) as cp1252, where a UTF-8 tick or dash turns into curly quotes that break the parser.
$MK_OK = [string][char]0x2713; $MK_BAD = [string][char]0x2717
function Say($t) { Write-Host ""; Write-Host "== $t" }
function Ok($t) { Write-Host "  $MK_OK $t" }
function Warn($t) { Write-Host "  ! $t" }
function Die($t, $fix) { Write-Host ""; Write-Host "  $MK_BAD $t"; if ($fix) { Write-Host "    If not: $fix" }; exit 1 }
function Have($c) { return [bool](Get-Command $c -ErrorAction SilentlyContinue) }
function Refresh-Path { if ($env:OS -eq 'Windows_NT') { $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + (Join-Path $HOME '.local/bin') } }
$Shell = (Get-Process -Id $PID).Path   # the PowerShell running this script (powershell.exe on Windows, pwsh elsewhere)
function Write-Utf8NoBom([string]$Path, [string]$Text) { [IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false))) }
function Winget-Install($id, $what) {
  if (-not (Have 'winget')) { return $false }
  Write-Host "  ... installing $what with winget (this can take a few minutes)"
  & winget install --id $id -e --source winget --accept-package-agreements --accept-source-agreements --silent | Out-Null
  Refresh-Path
  return $true
}

Write-Host "ANKR install - windows - home $ClaudeHome"
Write-Host "Official installers only. Your key stays on this computer. Re-running updates, never resets."

if ($Check) {
  $doc = Join-Path $ClaudeHome 'ankr/bin/ankr-doctor.ps1'
  if (-not (Test-Path $doc)) { Die 'harness not installed yet' 'run the line without -Check' }
  & $Shell -NoProfile -ExecutionPolicy Bypass -File $doc; exit $LASTEXITCODE
}

# ---------------------------------------------------------------- WSL route (the founder's own path)
if ($WSL) {
  Say 'WSL route: Ubuntu inside Windows + VS Code Remote-WSL'
  $wslOk = $false
  try { & wsl.exe --status 2>$null | Out-Null; $wslOk = ($LASTEXITCODE -eq 0) } catch {}
  if (-not $NoIDE) {
    if (-not (Have 'code')) { if (-not (Winget-Install 'Microsoft.VisualStudioCode' 'VS Code')) { Warn 'winget is missing; get VS Code from https://code.visualstudio.com' } }
    if (Have 'code') { & code --install-extension ms-vscode-remote.remote-wsl --force | Out-Null; & code --install-extension Anthropic.claude-code --force | Out-Null; Ok 'VS Code: Remote-WSL + Claude Code extensions' }
  }
  if (-not $wslOk) {
    Write-Host '  ... installing WSL with Ubuntu (Windows will ask to restart)'
    & wsl.exe --install -d Ubuntu
    Write-Host ''
    Write-Host 'Restart Windows now. After the restart, open the "Ubuntu" app, choose a username and password when it asks,'
    Write-Host "then paste this line there:   curl -fsSL $Base/install.sh | bash"
    Write-Host 'Then open VS Code -> bottom-left "><" -> Connect to WSL -> Terminal -> type claude.'
    exit 0
  }
  Ok 'WSL is present - handing the Linux line to your default distro'
  & wsl.exe -- bash -lc "curl -fsSL $Base/install.sh | bash"
  Write-Host ''
  Write-Host 'Open VS Code -> bottom-left "><" -> Connect to WSL -> Terminal -> type claude.'
  exit $LASTEXITCODE
}

# ---------------------------------------------------------------- 1 Git for Windows (hooks run through Git Bash)
Say '1/6 Git for Windows'
if (-not (Have 'git')) {
  if (-not (Winget-Install 'Git.Git' 'Git for Windows')) { Warn 'winget is not available on this Windows. Install "App Installer" from the Microsoft Store, or Git from https://git-scm.com, then run the line again.' }
}
$GitBash = $null
foreach ($c in @($env:CLAUDE_CODE_GIT_BASH_PATH, "$env:ProgramFiles\Git\bin\bash.exe", "${env:ProgramFiles(x86)}\Git\bin\bash.exe", "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe")) { if ($c -and (Test-Path $c)) { $GitBash = $c; break } }
if ($GitBash) { Ok "Git Bash at $GitBash" } else { Warn 'Git Bash not found - the guard hooks will NOT be registered (they need it); permissions.deny still applies. Install Git for Windows and run the line again.' }

# ---------------------------------------------------------------- 2 Claude Code
if (-not $NoClaude) {
  Say '2/6 Claude Code'
  Refresh-Path
  if (Have 'claude') { Ok ("already installed: " + (& claude --version 2>$null | Select-Object -First 1)) }
  else {
    Write-Host "  ... running Anthropic's installer"
    try { & ([scriptblock]::Create((Invoke-RestMethod -Uri 'https://claude.ai/install.ps1' -UseBasicParsing))) } catch { Die "Anthropic's installer did not finish: $($_.Exception.Message)" 'retry in a new PowerShell window:  irm https://claude.ai/install.ps1 | iex' }
    Refresh-Path
  }
  if (-not (Have 'claude')) { Die 'claude is not on PATH yet' 'close this window, open a new PowerShell and run the line again' }
  Ok (& claude --version 2>$null | Select-Object -First 1)
}

# ---------------------------------------------------------------- 3 harness
Say "3/6 ANKR harness -> $ClaudeHome"
$Tmp = $null
if ($HarnessFrom) { $Payload = $HarnessFrom; if (-not (Test-Path (Join-Path $Payload 'harness.json'))) { Die "no harness.json in $Payload" } }
else {
  $Tmp = Join-Path ([IO.Path]::GetTempPath()) ("ankr-install-" + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
  try { Invoke-WebRequest -Uri "$Base/harness.zip" -OutFile (Join-Path $Tmp 'harness.zip') -UseBasicParsing } catch { Die "could not download $Base/harness.zip" 'check your internet connection and run the line again' }
  try {
    $ver = Invoke-RestMethod -Uri "$Base/version.json" -UseBasicParsing
    $want = $ver.files.'harness.zip'.sha256
    $got = (Get-FileHash -Algorithm SHA256 (Join-Path $Tmp 'harness.zip')).Hash.ToLower()
    if ($want -and ($want -ne $got)) { Die 'harness.zip checksum does not match version.json (a broken or tampered download)' 'run the line again; if it repeats, tell ankr.in' }
  } catch { if ($_.Exception.Message -like '*checksum*') { throw } else { Warn 'could not read version.json; continuing without the checksum' } }
  Expand-Archive -Path (Join-Path $Tmp 'harness.zip') -DestinationPath $Tmp -Force
  $Payload = Join-Path $Tmp 'harness'
}
$Version = ([IO.File]::ReadAllText((Join-Path $Payload 'harness.json')) | ConvertFrom-Json).version
New-Item -ItemType Directory -Force -Path (Join-Path $ClaudeHome 'rules'), (Join-Path $ClaudeHome 'skills') | Out-Null

# 3a back up + validate settings.json
$Bak = ''
$Settings = $null
if (Test-Path $S) {
  $ts = Get-Date -Format 'yyyyMMdd-HHmmss'; $Bak = "$S.bak-$ts"; $n = 1
  while (Test-Path $Bak) { $Bak = "$S.bak-$ts-$n"; $n++ }   # two runs in one second never share a backup
  Copy-Item $S $Bak; Ok "backup: $Bak"
  $raw = [IO.File]::ReadAllText($S)
  if ($raw.Trim()) {
    try { $Settings = $raw | ConvertFrom-Json } catch { Die "$S is not valid JSON, so nothing was merged into it (Claude Code would ignore a broken settings file silently). Your copy is safe at $Bak." "open $S in Notepad and fix the JSON (a missing comma or bracket), or restore an older $S.bak-*, then run the line again" }
    if ($Settings -isnot [PSCustomObject]) { Die "$S does not hold a JSON object; nothing was written" }
  }
}
if (-not $Settings) { $Settings = New-Object PSObject }

# 3b files
$Ankr = Join-Path $ClaudeHome 'ankr'
if (Test-Path $Ankr) { Remove-Item -Recurse -Force $Ankr }
Copy-Item -Recurse -Force $Payload $Ankr
Copy-Item -Force (Join-Path $Ankr 'rules/*.md') (Join-Path $ClaudeHome 'rules')
Get-ChildItem (Join-Path $Ankr 'skills') -Directory | ForEach-Object { $d = Join-Path (Join-Path $ClaudeHome 'skills') $_.Name; New-Item -ItemType Directory -Force -Path $d | Out-Null; Copy-Item -Force (Join-Path $_.FullName 'SKILL.md') (Join-Path $d 'SKILL.md') }
Ok "harness v${Version}: rules, hooks, skills, byok, doctor"

# 3c CLAUDE.md import line
$Import = if ($ClaudeHome -eq (Join-Path $HOME '.claude')) { '@~/.claude/ankr/ANKR.md' } else { '@' + ($ClaudeHome -replace '\\', '/') + '/ankr/ANKR.md' }
$cm = Join-Path $ClaudeHome 'CLAUDE.md'
$cur = if (Test-Path $cm) { [IO.File]::ReadAllText($cm) } else { '' }
if ($cur.Contains($Import)) { Ok 'CLAUDE.md already imports the ANKR rules' }
else {
  if ($cur -and -not $cur.EndsWith("`n")) { $cur += "`n" }
  $cur += "`n<!-- ankr-harness: the rules that travel; remove this line to opt out -->`n$Import`n"
  Write-Utf8NoBom $cm $cur; Ok "CLAUDE.md now imports $Import"
}

# 3d settings.json merge - hooks (only if Git Bash exists) + permissions.deny, by content
$Frag = [IO.File]::ReadAllText((Join-Path $Ankr 'settings.ankr.json')) | ConvertFrom-Json
$isAnkr = { param($e) foreach ($x in @($e.hooks)) { if (("" + $x.command) -like '*/ankr/hooks/*') { return $true } }; return $false }
if ($GitBash) {
  if (-not $Settings.PSObject.Properties['hooks'] -or $Settings.hooks -isnot [PSCustomObject]) { if ($Settings.PSObject.Properties['hooks']) { $Settings.PSObject.Properties.Remove('hooks') }; $Settings | Add-Member -NotePropertyName hooks -NotePropertyValue (New-Object PSObject) }
  foreach ($ev in $Frag.hooks.PSObject.Properties.Name) {
    $cur = @(); if ($Settings.hooks.PSObject.Properties[$ev]) { $cur = @($Settings.hooks.$ev | Where-Object { -not (& $isAnkr $_) }) }
    $cur += @($Frag.hooks.$ev)
    if ($Settings.hooks.PSObject.Properties[$ev]) { $Settings.hooks.$ev = $cur } else { $Settings.hooks | Add-Member -NotePropertyName $ev -NotePropertyValue $cur }
  }
}
if (-not $Settings.PSObject.Properties['permissions'] -or $Settings.permissions -isnot [PSCustomObject]) { if ($Settings.PSObject.Properties['permissions']) { $Settings.PSObject.Properties.Remove('permissions') }; $Settings | Add-Member -NotePropertyName permissions -NotePropertyValue (New-Object PSObject) }
$deny = @(); if ($Settings.permissions.PSObject.Properties['deny']) { $deny = @($Settings.permissions.deny) }
foreach ($d in $Frag.permissions.deny) { if ($deny -notcontains $d) { $deny += $d } }
if ($Settings.permissions.PSObject.Properties['deny']) { $Settings.permissions.deny = $deny } else { $Settings.permissions | Add-Member -NotePropertyName deny -NotePropertyValue $deny }
$json = ($Settings | ConvertTo-Json -Depth 32) + "`n"
$tmpS = "$S.tmp-$PID"; Write-Utf8NoBom $tmpS $json
try { [IO.File]::ReadAllText($tmpS) | ConvertFrom-Json | Out-Null } catch { Remove-Item $tmpS -Force; Die "the merged settings did not parse; $S was not changed" "your copy is at $Bak" }
Move-Item -Force $tmpS $S
if ($GitBash) { Ok 'settings.json: guard hook + session brief + permissions.deny merged (yours kept)' } else { Ok 'settings.json: permissions.deny merged (hooks skipped - no Git Bash)' }
if ($Tmp) { Remove-Item -Recurse -Force $Tmp -ErrorAction SilentlyContinue }

# ---------------------------------------------------------------- 4 IDE
Say '4/6 IDE'
if ($NoIDE) { Ok 'skipped (-NoIDE)' }
else {
  if (-not (Have 'code')) { if (-not (Winget-Install 'Microsoft.VisualStudioCode' 'VS Code')) { Warn 'winget is missing; get VS Code from https://code.visualstudio.com and run the line again' } }
  if (Have 'code') {
    & code --install-extension Anthropic.claude-code --force | Out-Null
    if ($LASTEXITCODE -eq 0) { Ok 'VS Code: Claude Code extension installed (Anthropic.claude-code)' } else { Warn "VS Code is here but the extension did not install; inside VS Code search Extensions for 'Claude Code' by Anthropic" }
  }
}

# ---------------------------------------------------------------- 5 BYOK
Say '5/6 sign-in (your key stays on this computer)'
if ($NoByok) { Ok 'skipped (-NoByok) - later: /ankr-byok inside Claude' }
else {
  & $Shell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Ankr 'byok/byok.ps1') -Serve
  if ($LASTEXITCODE -ne 0) { Warn 'the sign-in page did not finish - run /ankr-byok inside Claude any time, or just start claude and sign in' }
}

# ---------------------------------------------------------------- 6 doctor
Say '6/6 doctor'
& $Shell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Ankr 'bin/ankr-doctor.ps1'); $doc = $LASTEXITCODE
Write-Host ''
switch ($doc) {
  0 { Write-Host 'Installed and signed in.' }
  3 { Write-Host 'Installed. Not signed in yet - that is the only open item: type   claude   and sign in when the browser opens, or run /ankr-byok inside Claude.' }
  default { Write-Host "Installed with problems - the fix is printed after each $MK_BAD above. Run this line again after doing it." }
}
Write-Host 'Next: open a new PowerShell window in a project folder and type   claude'
Write-Host 'From your phone: on this computer run   claude remote-control   and scan the code with the Claude app.'
Write-Host 'Update any time by running this same line again. Source and facts: https://ankr.in/install'
exit $doc
