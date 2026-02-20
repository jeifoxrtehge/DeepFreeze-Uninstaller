@echo off
chcp 65001 >nul
title DeepFreeze Uninstaller Launcher
cls
color 0A

echo.
echo  ============================================
echo    DeepFreeze Uninstaller
echo  ============================================
echo.
echo  Select version to run:
echo.
echo  [1] CLI Version
echo      For advanced users
echo.
echo  [2] GUI Version
echo      User-friendly interface
echo.
echo  [3] Pro Version (Recommended)
echo      Fixes driver filters, most thorough
echo.
echo  [4] Help / Instructions
echo.
echo  [0] Exit
echo.
echo  ============================================
echo.

set /p choice=Enter option (0-4): 

if "%choice%"=="1" goto cmd_version
if "%choice%"=="2" goto gui_version
if "%choice%"=="3" goto pro_version
if "%choice%"=="4" goto help
if "%choice%"=="0" goto exit
goto invalid

:cmd_version
echo.
echo Starting CLI version...
echo.
python "强力uninstall 冰点还原.py"
pause
goto start

:gui_version
echo.
echo Starting GUI version...
echo.
python "强力uninstall 冰点还原_GUI.py"
pause
goto start

:pro_version
echo.
echo Starting Pro version...
echo.
python "强力uninstall 冰点还原_专业版.py"
pause
goto start

:help
echo.
echo  ============================================
echo    Instructions
echo  ============================================
echo.
echo  IMPORTANT:
echo  - Must run in PE environment!
echo  - Auto-backs up SYSTEM registry file
echo  - Ensure you know what you're doing
echo.
echo  STEPS:
echo  1. Enter PE system
echo  2. Check system drive letter (may not be C:)
echo  3. Run this tool
echo  4. Follow prompts
echo  5. Restart computer
echo.
echo  RECOVERY:
echo  If system bluescreens after uninstall:
echo  1. Re-enter PE
echo  2. Find backup file X:\SYSTEM.bak
echo  3. Copy to X:\Windows\System32\config\SYSTEM
echo  4. Restart
echo.
echo  ============================================
echo.
pause
goto start

:invalid
echo.
echo [!] Invalid option, please try again
echo.
pause
goto start

:exit
echo.
echo Goodbye!
echo.
timeout /t 2 /nobreak >nul
exit

:start
goto start
