@echo off
:: ═══════════════════════════════════════════════════════════════════════════
:: ANKR Interact - Send To Script
:: ═══════════════════════════════════════════════════════════════════════════
::
:: Installation:
:: 1. Copy this file to: %APPDATA%\Microsoft\Windows\SendTo\
:: 2. Right-click any file → Send To → ANKR Interact
::
:: ═══════════════════════════════════════════════════════════════════════════

if "%~1"=="" (
    start "" "https://ankr.in/interact/"
    exit /b
)

:: Convert Windows path to URL-safe format
set "FILE=%~1"
set "FILE=%FILE:\=/%"

:: URL encode spaces
set "FILE=%FILE: =%%20%"

:: Open in default browser
start "" "https://ankr.in/interact/?file=%FILE%"
