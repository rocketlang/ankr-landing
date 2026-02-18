# ANKR Interact - Quick Install
# irm https://ankr.in/downloads/ankr-interact/Install-ANKRInteract.ps1 | iex
$u="https://ankr.in/interact/"
Write-Host "[*] Installing ANKR Interact..." -ForegroundColor Cyan
reg add "HKCU\Software\Classes\*\shell\ANKRInteract" /ve /d "Open with ANKR Interact" /f 2>$null | Out-Null
reg add "HKCU\Software\Classes\*\shell\ANKRInteract" /v Icon /d "shell32.dll,14" /f 2>$null | Out-Null
reg add "HKCU\Software\Classes\*\shell\ANKRInteract\command" /ve /d "cmd /c start `"`" `"$u?file=%1`"" /f 2>$null | Out-Null
Write-Host "[OK] File context menu" -ForegroundColor Green
reg add "HKCU\Software\Classes\Directory\shell\ANKRInteract" /ve /d "Browse with ANKR Interact" /f 2>$null | Out-Null
reg add "HKCU\Software\Classes\Directory\shell\ANKRInteract" /v Icon /d "shell32.dll,4" /f 2>$null | Out-Null
reg add "HKCU\Software\Classes\Directory\shell\ANKRInteract\command" /ve /d "cmd /c start `"`" `"$u?source=%1`"" /f 2>$null | Out-Null
Write-Host "[OK] Folder context menu" -ForegroundColor Green
reg add "HKCU\Software\Classes\Directory\Background\shell\ANKRInteract" /ve /d "Open ANKR Interact here" /f 2>$null | Out-Null
reg add "HKCU\Software\Classes\Directory\Background\shell\ANKRInteract" /v Icon /d "shell32.dll,4" /f 2>$null | Out-Null
reg add "HKCU\Software\Classes\Directory\Background\shell\ANKRInteract\command" /ve /d "cmd /c start `"`" `"$u?source=%V`"" /f 2>$null | Out-Null
Write-Host "[OK] Background context menu" -ForegroundColor Green
reg add "HKCU\Software\Classes\ankr" /ve /d "URL:ANKR Protocol" /f 2>$null | Out-Null
reg add "HKCU\Software\Classes\ankr" /v "URL Protocol" /d "" /f 2>$null | Out-Null
reg add "HKCU\Software\Classes\ankr\shell\open\command" /ve /d "cmd /c start `"`" `"$u?file=%1`"" /f 2>$null | Out-Null
Write-Host "[OK] Protocol ankr://" -ForegroundColor Green
"@echo off`r`nstart `"`" `"$u`"" | Set-Content "$env:APPDATA\Microsoft\Windows\SendTo\ANKR Interact.bat"
Write-Host "[OK] Send To" -ForegroundColor Green
Write-Host "`nDone! Right-click any file -> 'Open with ANKR Interact'" -ForegroundColor Green
