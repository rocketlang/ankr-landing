#!/usr/bin/env bash
# ankr-install — install.sh · one line for Linux · macOS · WSL · Android/Termux
#   curl -fsSL https://ankr.in/install/install.sh | bash
# What it does, in order: prerequisites → Claude Code (Anthropic's own installer; npm on Termux) → the ANKR harness
# into ~/.claude (backed up, merged, never reset) → VS Code extension if VS Code is here → the BYOK page → the doctor.
# Flags (after `bash -s --`): --check · --no-byok · --no-ide · --no-prereqs · --no-claude · --harness-from <dir>
# Re-running is an update. Nothing is mirrored or repackaged; you pay Anthropic, ANKR receives nothing.
set -u
BASE="${ANKR_INSTALL_BASE:-https://ankr.in/install}"
NO_BYOK=0; NO_IDE=0; CHECK=0; HARNESS_FROM=""; NO_CLAUDE=0; NO_PREREQS=0
while [ $# -gt 0 ]; do
  case "$1" in
    --check) CHECK=1;; --no-byok) NO_BYOK=1;; --no-ide) NO_IDE=1;; --no-prereqs) NO_PREREQS=1;; --no-claude) NO_CLAUDE=1;;
    --harness-from) HARNESS_FROM="${2:-}"; shift;;
    --) ;;
    *) printf 'unknown flag: %s\n' "$1" >&2; exit 2;;
  esac
  shift
done

say(){ printf '\n== %s\n' "$*"; }
ok(){ printf '  ✓ %s\n' "$*"; }
warn(){ printf '  ! %s\n' "$*"; }
die(){ printf '\n  ✗ %s\n' "$1" >&2; [ -n "${2:-}" ] && printf '    If not: %s\n' "$2" >&2; exit 1; }
have(){ command -v "$1" >/dev/null 2>&1; }

UNAME="${ANKR_FAKE_UNAME:-$(uname -s 2>/dev/null)}"
PLATFORM=""
case "$UNAME" in
  Darwin) PLATFORM=macos;;
  Linux)
    if [ -n "${PREFIX:-}" ] && case "$PREFIX" in *com.termux*) true;; *) false;; esac; then PLATFORM=termux
    elif [ -f /proc/version ] && grep -qi microsoft /proc/version 2>/dev/null; then PLATFORM=wsl
    else PLATFORM=linux; fi;;
  MINGW*|MSYS*|CYGWIN*) die "This is Git Bash on Windows. Use the Windows line instead:  irm $BASE/install.ps1 | iex" "open PowerShell (Start → type PowerShell → Enter) and paste that line";;
  *) die "Unsupported system: $UNAME. This line covers Linux, macOS, WSL and Android/Termux." "see https://ankr.in/install for your device";;
esac
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
S="$CLAUDE_HOME/settings.json"

printf 'ANKR install · %s · home %s\n' "$PLATFORM" "$CLAUDE_HOME"
printf 'Official installers only. Your key stays on this computer. Re-running updates, never resets.\n'

# ---------------------------------------------------------------- Android / Termux → Ubuntu inside Termux, then the same line
# Claude Code ships no Android build (the npm package carries linux/darwin/win32 binaries only — checked 2026-09-12), so on a
# phone it runs inside Ubuntu under proot-distro, where Anthropic's own Linux installer works. This block sets that up, gives
# Termux a `claude` command that hands over, and runs this very line inside Ubuntu (proven in a Termux container 2026-09-12).
if [ "$PLATFORM" = termux ]; then
  say "Android: Claude Code runs inside Ubuntu-in-Termux (proot-distro); setting that up"
  PKGLOG="${TMPDIR:-$PREFIX/tmp}/ankr-install-pkg.log"
  pkg update -y >"$PKGLOG" 2>&1 || warn "pkg update did not finish (see $PKGLOG); trying to install anyway"
  if ! pkg install -y curl proot-distro >>"$PKGLOG" 2>&1; then
    # a rotated mirror can be stale (404 on pool files — seen in a Termux container 2026-09-12): pin Termux's primary and retry once
    warn "a package mirror failed; switching to the primary mirror (packages.termux.dev) and retrying"
    if [ -f "$PREFIX/etc/termux/mirrors/default" ]; then rm -rf "$PREFIX/etc/termux/chosen_mirrors"; ln -s "$PREFIX/etc/termux/mirrors/default" "$PREFIX/etc/termux/chosen_mirrors"; fi
    printf 'deb https://packages.termux.dev/apt/termux-main stable main\n' > "$PREFIX/etc/apt/sources.list"
    TERMUX_PKG_NO_MIRROR_SELECT=1 pkg update -y >>"$PKGLOG" 2>&1
    TERMUX_PKG_NO_MIRROR_SELECT=1 pkg install -y curl proot-distro >>"$PKGLOG" 2>&1 || { tail -5 "$PKGLOG" | sed 's/^/    | /'; die "pkg could not install curl and proot-distro (its last lines are above)" "in Termux run: termux-change-repo   (pick the main mirror), then: pkg update && pkg install -y curl proot-distro   and run the line again"; }
  fi
  ROOTFS="$PREFIX/var/lib/proot-distro/installed-rootfs/ubuntu"
  if [ ! -d "$ROOTFS" ]; then
    printf '  … downloading Ubuntu (a few minutes on a phone)\n'
    proot-distro install ubuntu >>"$PKGLOG" 2>&1 || { tail -5 "$PKGLOG" | sed 's/^/    | /'; die "proot-distro could not install Ubuntu (its last lines are above)" "run: proot-distro install ubuntu   and read what it says; then run the line again"; }
  fi
  ok "Ubuntu present under proot-distro"
  cat > "$PREFIX/bin/claude" <<'WRAP'
#!/data/data/com.termux/files/usr/bin/bash
# ankr-harness: Claude Code lives inside Ubuntu (proot-distro). This hands the command over; your projects live in Ubuntu's home.
exec proot-distro login ubuntu --shared-tmp -- /usr/bin/env PATH=/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/root TERM="${TERM:-xterm-256color}" claude "$@"
WRAP
  chmod +x "$PREFIX/bin/claude"
  ok "Termux now has a 'claude' command that hands over to Ubuntu"
  FLAGS=""; [ $NO_BYOK -eq 1 ] && FLAGS="$FLAGS --no-byok"; [ $NO_IDE -eq 1 ] && FLAGS="$FLAGS --no-ide"
  [ $NO_CLAUDE -eq 1 ] && FLAGS="$FLAGS --no-claude"; [ $NO_PREREQS -eq 1 ] && FLAGS="$FLAGS --no-prereqs"; [ $CHECK -eq 1 ] && FLAGS="$FLAGS --check"
  say "handing this line to Ubuntu (everything below runs inside it)"
  # a clean PATH: the Termux binaries on PATH cannot execute inside Ubuntu ("required file not found")
  exec proot-distro login ubuntu --shared-tmp -- /usr/bin/env PATH=/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/root TERM="${TERM:-xterm-256color}" ANKR_INSTALL_BASE="$BASE" \
    bash -c '{ command -v curl && command -v git && python3 -c "import json"; } >/dev/null 2>&1 || { apt-get update -qq; apt-get install -y -qq curl ca-certificates git python3; } >/tmp/ankr-install-apt.log 2>&1 || { tail -5 /tmp/ankr-install-apt.log; echo "apt inside Ubuntu failed (lines above); run: proot-distro login ubuntu   then   apt-get install -y curl git python3"; exit 1; }; curl -fsSL "$ANKR_INSTALL_BASE/install.sh" | bash -s -- '"$FLAGS"
fi

if [ $CHECK -eq 1 ]; then
  [ -x "$CLAUDE_HOME/ankr/bin/ankr-doctor.sh" ] || die "harness not installed yet" "run the line without --check"
  exec bash "$CLAUDE_HOME/ankr/bin/ankr-doctor.sh"
fi

# ---------------------------------------------------------------- 1 prerequisites
if [ $NO_PREREQS -eq 0 ]; then
  say "1/6 prerequisites ($PLATFORM)"
  case "$PLATFORM" in
    macos)
      if ! xcode-select -p >/dev/null 2>&1; then
        xcode-select --install >/dev/null 2>&1 || true
        die "macOS needs its Command Line Tools first (git, python3). A window just opened." "click Install, wait for it to finish, then run the line again"
      fi
      ok "Command Line Tools present (git, python3)";;
    linux|wsl)
      need=""; have curl || need="$need curl"; have git || need="$need git"
      # the settings merge and the BYOK page need python3 or node that actually runs (a proot Ubuntu starts with neither)
      python3 -c 'import json' >/dev/null 2>&1 || node -e '1' >/dev/null 2>&1 || need="$need python3"
      if [ -n "$need" ]; then
        SUDO=""; [ "$(id -u)" -ne 0 ] && { have sudo && SUDO="sudo" || die "need to install:$need, but there is no sudo here" "ask an administrator to install:$need, then run the line again"; }
        APTLOG="${TMPDIR:-/tmp}/ankr-install-pkg.log"   # a hidden package-manager error is a defect: keep the log, print its tail on failure
        printf '  … installing%s\n' "$need"
        if have apt-get; then { $SUDO apt-get update -y; $SUDO apt-get install -y $need ca-certificates; } >"$APTLOG" 2>&1
        elif have dnf; then $SUDO dnf install -y $need >"$APTLOG" 2>&1
        elif have apk; then $SUDO apk add --no-cache $need bash >"$APTLOG" 2>&1
        elif have pacman; then $SUDO pacman -Sy --noconfirm $need >"$APTLOG" 2>&1
        elif have zypper; then $SUDO zypper install -y $need >"$APTLOG" 2>&1
        else die "no known package manager to install:$need" "install$need with your distribution's tool, then run the line again"; fi
        have curl && have git || { tail -5 "$APTLOG" 2>/dev/null | sed 's/^/    | /'; die "could not install:$need (the package manager's last lines are above)" "run your package manager by hand for:$need, then run the line again"; }
        if ! python3 -c 'import json' >/dev/null 2>&1 && ! node -e '1' >/dev/null 2>&1; then
          tail -5 "$APTLOG" 2>/dev/null | sed 's/^/    | /'
          warn "python3 did not install (lines above): settings.json can be created but not merged, and the sign-in page falls back to the terminal — install python3 by hand and run the line again"
        fi
      fi
      ok "curl, git present$(python3 -c 'import json' >/dev/null 2>&1 && printf ', python3 runs' || { node -e 1 >/dev/null 2>&1 && printf ', node runs'; })";;
  esac
fi

# ---------------------------------------------------------------- 2 Claude Code
if [ $NO_CLAUDE -eq 0 ]; then
  say "2/6 Claude Code"
  if have claude || [ -x "$HOME/.local/bin/claude" ]; then ok "already installed: $(claude --version 2>/dev/null || "$HOME/.local/bin/claude" --version 2>/dev/null | head -1)"
  else
    curl -fsSL https://claude.ai/install.sh | bash || die "Anthropic's installer did not finish" "read its message above; the line to retry is: curl -fsSL https://claude.ai/install.sh | bash"
  fi
  if ! have claude && [ -x "$HOME/.local/bin/claude" ]; then
    export PATH="$HOME/.local/bin:$PATH"
    for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
      [ -f "$rc" ] || [ "$rc" = "$HOME/.bashrc" ] || continue
      grep -qF '# ankr-harness: claude on PATH' "$rc" 2>/dev/null || printf '\n# ankr-harness: claude on PATH\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$rc"
    done
    ok "added ~/.local/bin to PATH in your shell file (open a new terminal later)"
  fi
  have claude || die "claude is not on PATH" "open a new terminal and run the line again"
  ok "$(claude --version 2>/dev/null | head -1)"
fi

# ---------------------------------------------------------------- 3 harness
say "3/6 ANKR harness → $CLAUDE_HOME"
TMP=""
if [ -n "$HARNESS_FROM" ]; then
  PAYLOAD="$HARNESS_FROM"; [ -f "$PAYLOAD/harness.json" ] || die "no harness.json in $PAYLOAD"
else
  TMP=$(mktemp -d 2>/dev/null || mktemp -d -t ankr)
  curl -fsSL "$BASE/harness.tar.gz" -o "$TMP/harness.tar.gz" || die "could not download $BASE/harness.tar.gz" "check your internet connection and run the line again"
  curl -fsSL "$BASE/version.json" -o "$TMP/version.json" || die "could not download $BASE/version.json"
  want=$(sed -n 's/.*"harness\.tar\.gz"[[:space:]]*:[[:space:]]*{[^}]*"sha256"[[:space:]]*:[[:space:]]*"\([0-9a-f]*\)".*/\1/p' "$TMP/version.json" | head -1)
  if have sha256sum; then got=$(sha256sum "$TMP/harness.tar.gz" | cut -d' ' -f1); elif have shasum; then got=$(shasum -a 256 "$TMP/harness.tar.gz" | cut -d' ' -f1); else got=""; fi
  if [ -n "$want" ] && [ -n "$got" ] && [ "$want" != "$got" ]; then die "harness.tar.gz checksum does not match version.json (a broken or tampered download)" "run the line again; if it repeats, tell ankr.in"; fi
  tar -xzf "$TMP/harness.tar.gz" -C "$TMP" || die "could not unpack harness.tar.gz"
  PAYLOAD="$TMP/harness"
fi
VERSION=$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$PAYLOAD/harness.json" | head -1)

# A tool must RUN, not merely exist on PATH: inside Ubuntu-under-Termux (proot) the Termux python3 is still on PATH and
# cannot execute ("required file not found") — proven in a Termux container 2026-09-12.
JSON_TOOL=""
if python3 -c 'import json' >/dev/null 2>&1; then JSON_TOOL=python3
elif node -e '1' >/dev/null 2>&1; then JSON_TOOL=node; fi
mkdir -p "$CLAUDE_HOME/rules" "$CLAUDE_HOME/skills"

# 3a back up + validate settings.json before touching anything
BAK=""
if [ -f "$S" ]; then
  ts=$(date +%Y%m%d-%H%M%S); BAK="$S.bak-$ts"; n=1
  while [ -e "$BAK" ]; do BAK="$S.bak-$ts-$n"; n=$((n+1)); done   # two runs in one second never share a backup
  cp -p "$S" "$BAK" || die "could not back up $S"
  ok "backup: $BAK"
  if [ -s "$S" ]; then
    valid=1
    case "$JSON_TOOL" in
      python3) python3 -c 'import json,sys; json.load(open(sys.argv[1],encoding="utf-8-sig"))' "$S" >/dev/null 2>&1 || valid=0;;
      node) node -e 'JSON.parse(require("fs").readFileSync(process.argv[1],"utf8").replace(/^﻿/,""))' "$S" >/dev/null 2>&1 || valid=0;;
    esac
    [ $valid -eq 1 ] || die "$S is not valid JSON, so nothing was merged into it (Claude Code would ignore a broken settings file silently). Your copy is safe at $BAK." "open $S in an editor and fix the JSON (a missing comma or bracket), or restore an older $S.bak-*, then run the line again"
  fi
fi

# 3b files
rm -rf "$CLAUDE_HOME/ankr"
cp -R "$PAYLOAD" "$CLAUDE_HOME/ankr" || die "could not copy the harness into $CLAUDE_HOME/ankr"
chmod +x "$CLAUDE_HOME/ankr/hooks/"*.sh "$CLAUDE_HOME/ankr/bin/"*.sh "$CLAUDE_HOME/ankr/byok/"*.sh "$CLAUDE_HOME/ankr/byok/"*.py "$CLAUDE_HOME/ankr/byok/"*.mjs 2>/dev/null
cp "$CLAUDE_HOME/ankr/rules/"*.md "$CLAUDE_HOME/rules/"
for sk in "$CLAUDE_HOME/ankr/skills/"*/; do n=$(basename "$sk"); mkdir -p "$CLAUDE_HOME/skills/$n"; cp "$sk"SKILL.md "$CLAUDE_HOME/skills/$n/SKILL.md"; done
ok "harness v$VERSION: rules, hooks, skills, byok, doctor"

# 3c CLAUDE.md import line (added once, never removes yours)
if [ "$CLAUDE_HOME" = "$HOME/.claude" ]; then IMPORT='@~/.claude/ankr/ANKR.md'; else IMPORT="@$CLAUDE_HOME/ankr/ANKR.md"; fi
if [ -f "$CLAUDE_HOME/CLAUDE.md" ] && grep -qF "$IMPORT" "$CLAUDE_HOME/CLAUDE.md"; then ok "CLAUDE.md already imports the ANKR rules"
else
  [ -f "$CLAUDE_HOME/CLAUDE.md" ] && [ -s "$CLAUDE_HOME/CLAUDE.md" ] && [ "$(tail -c1 "$CLAUDE_HOME/CLAUDE.md" | od -An -c | tr -d ' ')" != '\n' ] && printf '\n' >> "$CLAUDE_HOME/CLAUDE.md"
  printf '\n<!-- ankr-harness: the rules that travel; remove this line to opt out -->\n%s\n' "$IMPORT" >> "$CLAUDE_HOME/CLAUDE.md"
  ok "CLAUDE.md now imports $IMPORT"
fi

# 3d settings.json merge (hooks + permissions.deny), by content, never clobbering yours
FRAG="$CLAUDE_HOME/ankr/settings.ankr.json"
if [ -z "$JSON_TOOL" ]; then
  if [ ! -s "$S" ]; then cp "$FRAG" "$S"; chmod 600 "$S"; ok "settings.json created from the harness fragment (no python3/node here to merge)"
  else die "neither python3 nor node is here, so settings.json cannot be merged safely" "install python3 (or node), then run the line again — your file was not touched"; fi
else
  TMPS="$S.tmp-$$"
  if [ "$JSON_TOOL" = python3 ]; then
    python3 - "$S" "$FRAG" "$TMPS" <<'EOF'
import json,sys,os
sp,fp,out=sys.argv[1:4]
s=json.load(open(sp,encoding='utf-8-sig')) if os.path.exists(sp) and os.path.getsize(sp)>0 else {}
f=json.load(open(fp,encoding='utf-8'))
if not isinstance(s,dict): sys.exit(3)
def is_ankr(e): return isinstance(e,dict) and any('/ankr/hooks/' in str(h.get('command','')) for h in (e.get('hooks') or []) if isinstance(h,dict))
hooks=s.get('hooks') if isinstance(s.get('hooks'),dict) else {}
for ev,entries in f['hooks'].items():
    cur=[e for e in (hooks.get(ev) if isinstance(hooks.get(ev),list) else []) if not is_ankr(e)]
    cur.extend(entries); hooks[ev]=cur
s['hooks']=hooks
perms=s.get('permissions') if isinstance(s.get('permissions'),dict) else {}
deny=[d for d in (perms.get('deny') if isinstance(perms.get('deny'),list) else [])]
for d in f['permissions']['deny']:
    if d not in deny: deny.append(d)
perms['deny']=deny; s['permissions']=perms
json.dump(s,open(out,'w',encoding='utf-8'),indent=2,ensure_ascii=False); open(out,'a').write('\n')
json.load(open(out,encoding='utf-8'))
EOF
    rc=$?
  else
    node - "$S" "$FRAG" "$TMPS" <<'EOF'
const fs=require('fs');const [sp,fp,out]=process.argv.slice(2);
const s=(fs.existsSync(sp)&&fs.statSync(sp).size>0)?JSON.parse(fs.readFileSync(sp,'utf8').replace(/^﻿/,'')):{};
const f=JSON.parse(fs.readFileSync(fp,'utf8'));
if(!s||typeof s!=='object'||Array.isArray(s))process.exit(3);
const isAnkr=e=>e&&typeof e==='object'&&(e.hooks||[]).some(h=>h&&String(h.command||'').includes('/ankr/hooks/'));
const hooks=(s.hooks&&typeof s.hooks==='object'&&!Array.isArray(s.hooks))?s.hooks:{};
for(const [ev,entries] of Object.entries(f.hooks)){const cur=(Array.isArray(hooks[ev])?hooks[ev]:[]).filter(e=>!isAnkr(e));cur.push(...entries);hooks[ev]=cur;}
s.hooks=hooks;
const perms=(s.permissions&&typeof s.permissions==='object'&&!Array.isArray(s.permissions))?s.permissions:{};
const deny=Array.isArray(perms.deny)?perms.deny.slice():[];for(const d of f.permissions.deny){if(!deny.includes(d))deny.push(d);}
perms.deny=deny;s.permissions=perms;
fs.writeFileSync(out,JSON.stringify(s,null,2)+'\n');JSON.parse(fs.readFileSync(out,'utf8'));
EOF
    rc=$?
  fi
  [ $rc -eq 0 ] && [ -s "$TMPS" ] || { rm -f "$TMPS"; die "the settings merge failed (code $rc); $S was not changed" "your copy is at ${BAK:-<no previous file>}; run the line again, and if it repeats tell ankr.in"; }
  mv "$TMPS" "$S" && chmod 600 "$S"
  ok "settings.json: guard hook + session brief + permissions.deny merged (yours kept)"
fi
[ -n "$TMP" ] && rm -rf "$TMP"

# ---------------------------------------------------------------- 4 IDE
say "4/6 IDE"
if [ $NO_IDE -eq 1 ]; then ok "skipped (--no-ide)"
elif have code; then
  if code --install-extension Anthropic.claude-code --force >/dev/null 2>&1; then ok "VS Code: Claude Code extension installed (Anthropic.claude-code)"
  else warn "VS Code is here but the extension did not install; inside VS Code search Extensions for 'Claude Code' by Anthropic"; fi
else ok "VS Code not found (optional). Get it at https://code.visualstudio.com and run this line again to add the extension"; fi

# ---------------------------------------------------------------- 5 BYOK
say "5/6 sign-in (your key stays on this computer)"
if [ $NO_BYOK -eq 1 ]; then ok "skipped (--no-byok) — later: /ankr-byok inside Claude"
elif [ -r /dev/tty ]; then
  bash "$CLAUDE_HOME/ankr/byok/byok.sh" </dev/tty || warn "the sign-in page did not finish — you can run /ankr-byok inside Claude any time, or just start claude and sign in"
else ok "no terminal attached — later: /ankr-byok inside Claude, or just start claude and sign in"; fi

# ---------------------------------------------------------------- 6 doctor
say "6/6 doctor"
bash "$CLAUDE_HOME/ankr/bin/ankr-doctor.sh"; DOC=$?
case $DOC in
  0) printf '\nInstalled and signed in.\n';;
  3) printf '\nInstalled. Not signed in yet — that is the only open item: type   claude   and sign in when the browser opens, or run /ankr-byok inside Claude.\n';;
  *) printf '\nInstalled with problems — the fix is printed after each ✗ above. Run this line again after doing it.\n';;
esac
printf 'Next: open a terminal in a project folder and type   claude\n'
[ "$PLATFORM" = termux ] || printf 'From your phone: on this computer run   claude remote-control   and scan the code with the Claude app.\n'
printf 'Update any time by running this same line again. Source and facts: https://ankr.in/install\n'
exit $DOC
