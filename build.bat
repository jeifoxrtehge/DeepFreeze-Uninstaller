@echo off
chcp 65001 >nul
title Build DeepFreeze Uninstaller
cls
color 0A

echo.
echo  ============================================
echo    Build DeepFreeze Uninstaller
echo  ============================================
echo.

set "VERSION=v1.0.0"
set "OUTPUT_DIR=DeepFreeze-Uninstaller-%VERSION%"

echo [*] Creating output directory...
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%"

echo [*] Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [!] PyInstaller not found, installing...
    pip install pyinstaller
)

echo [*] Building executables...

echo [*] Building CLI version...
pyinstaller --onefile --name "DeepFreeze_Uninstaller_CLI" "强力uninstall 冰点还原.py"

echo [*] Building GUI version...
pyinstaller --onefile --windowed --name "DeepFreeze_Uninstaller_GUI" "强力uninstall 冰点还原_GUI.py"

echo [*] Building Pro version...
pyinstaller --onefile --name "DeepFreeze_Uninstaller_Pro" "强力uninstall 冰点还原_专业版.py"

echo [*] Copying files...
copy "dist\DeepFreeze_Uninstaller_CLI.exe" "%OUTPUT_DIR%\" >nul
copy "dist\DeepFreeze_Uninstaller_GUI.exe" "%OUTPUT_DIR%\" >nul
copy "dist\DeepFreeze_Uninstaller_Pro.exe" "%OUTPUT_DIR%\" >nul
copy "launcher.bat" "%OUTPUT_DIR%\" >nul
copy "README.md" "%OUTPUT_DIR%\" >nul
copy "LICENSE" "%OUTPUT_DIR%\" >nul

echo [*] Cleaning up...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q *.spec 2>nul

echo [*] Creating zip archive...
if exist "%OUTPUT_DIR%.zip" del "%OUTPUT_DIR%.zip"

powershell -Command "Compress-Archive -Path '%OUTPUT_DIR%' -DestinationPath '%OUTPUT_DIR%.zip'" >nul 2>&1
if errorlevel 0 (
    echo [+] Zip archive created successfully
) else (
    echo [!] Failed to create zip, please manually compress: %OUTPUT_DIR%
)

echo [*] Cleaning temp directory...
rmdir /s /q "%OUTPUT_DIR%" 2>nul

echo.
echo  ============================================
echo    Build Complete!
echo  ============================================
echo.
echo  Output: %OUTPUT_DIR%.zip
echo.
pause
