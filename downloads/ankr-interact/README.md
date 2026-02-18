# ANKR Interact Desktop

Desktop application and Windows integration for ANKR Interact - the Knowledge Browser.

## Quick Install (No Desktop App Required)

### Option 1: PowerShell Installer (Recommended)

Run in PowerShell:

```powershell
# Download and run installer
irm https://ankr.in/downloads/Install-ANKRInteract.ps1 | iex

# Or from local file:
.\scripts\Install-ANKRInteract.ps1
```

This adds:
- Right-click → **"Open with ANKR Interact"** for all files
- Right-click → **"Browse with ANKR Interact"** for folders
- Send To → **ANKR Interact**
- Protocol handler: `ankr://path/to/file`
- Desktop shortcut

### Option 2: Registry Files

1. Download `windows-context-menu-web.reg`
2. Double-click and confirm
3. Done! Right-click any file → "Open with ANKR Interact"

### Option 3: Manual Send To

1. Copy `ANKR Interact.bat` to: `%APPDATA%\Microsoft\Windows\SendTo\`
2. Right-click any file → Send To → ANKR Interact

---

## Desktop Application (Full Features)

For the full desktop experience with offline support:

### Install from Release

1. Download `ANKR-Interact-Setup.exe` from [releases](https://ankr.in/downloads/)
2. Run the installer
3. Done! The app registers as file handler for common formats

### Build from Source

```bash
# Install dependencies
npm install

# Run in development
npm run dev

# Build for Windows
npm run build:win

# Build for macOS
npm run build:mac

# Build for Linux
npm run build:linux
```

---

## Features

### File Viewing
- **PDF** - Full viewer with zoom, page navigation
- **Images** - Pan/zoom with mouse
- **Video/Audio** - Native playback
- **Excel/CSV** - Table rendering
- **Markdown** - Rendered with syntax highlighting
- **Code** - 50+ language syntax highlighting

### Editing
- **Edit any text file** - `Cmd/Ctrl+E`
- **Live preview** for Markdown
- **Auto-save indicator**

### Linked Notepad
- Persistent side panel - `Cmd/Ctrl+L`
- Take notes while browsing
- Link/unlink files dynamically

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Quick open file |
| `Ctrl+P` | Command palette |
| `Ctrl+E` | Edit mode |
| `Ctrl+S` | Save |
| `Ctrl+N` | New file |
| `Ctrl+L` | Linked notepad |
| `Ctrl+G` | Knowledge graph |

---

## URL Parameters

Open files directly via URL:

```
https://ankr.in/interact/?file=path/to/file.md
https://ankr.in/interact/?file=path/to/file.md&edit=true
https://ankr.in/interact/?file=path/to/file.md&notepad=true
https://ankr.in/interact/?source=folder-id
```

---

## Uninstall

### PowerShell

```powershell
.\scripts\Install-ANKRInteract.ps1 -Uninstall
```

### Registry

Run `windows-context-menu-uninstall.reg`

---

## License

MIT © ANKR Labs
