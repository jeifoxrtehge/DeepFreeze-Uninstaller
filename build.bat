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

echo [*] Copying files...
copy "README.md" "%OUTPUT_DIR%\" >nul
copy "LICENSE" "%OUTPUT_DIR%\" >nul
copy "启动器.bat" "%OUTPUT_DIR%\" >nul
copy "一键斩杀冰点还原.bat" "%OUTPUT_DIR%\" >nul
copy "强力uninstall 冰点还原.py" "%OUTPUT_DIR%\" >nul
copy "强力uninstall 冰点还原_GUI.py" "%OUTPUT_DIR%\" >nul
copy "强力uninstall 冰点还原_专业版.py" "%OUTPUT_DIR%\" >nul

echo [*] Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [!] PyInstaller not found, skipping exe build
    echo [*] Install: pip install pyinstaller
) else (
    echo [*] Building executables...
    
    echo [*] Building CLI version...
    pyinstaller --onefile --name "DeepFreeze_Uninstaller_CLI" "强力uninstall 冰点还原.py" >nul 2>&1
    
    echo [*] Building GUI version...
    pyinstaller --onefile --windowed --name "DeepFreeze_Uninstaller_GUI" "强力uninstall 冰点还原_GUI.py" >nul 2>&1
    
    echo [*] Building Pro version...
    pyinstaller --onefile --name "DeepFreeze_Uninstaller_Pro" "强力uninstall 冰点还原_专业版.py" >nul 2>&1
    
    if exist "dist\DeepFreeze_Uninstaller_CLI.exe" (
        copy "dist\DeepFreeze_Uninstaller_CLI.exe" "%OUTPUT_DIR%\" >nul
        echo [+] CLI build success
    )
    
    if exist "dist\DeepFreeze_Uninstaller_GUI.exe" (
        copy "dist\DeepFreeze_Uninstaller_GUI.exe" "%OUTPUT_DIR%\" >nul
        echo [+] GUI build success
    )
    
    if exist "dist\DeepFreeze_Uninstaller_Pro.exe" (
        copy "dist\DeepFreeze_Uninstaller_Pro.exe" "%OUTPUT_DIR%\" >nul
        echo [+] Pro build success
    )
    
    echo [*] Cleaning temp files...
    rmdir /s /q build 2>nul
    rmdir /s /q dist 2>nul
    del /q *.spec 2>nul
)

echo [*] Creating zip archive...
if exist "%OUTPUT_DIR%.zip" del "%OUTPUT_DIR%.zip"

where 7z >nul 2>&1
if %errorlevel% == 0 (
    7z a -tzip "%OUTPUT_DIR%.zip" "%OUTPUT_DIR%\" >nul
    echo [+] Zip created with 7z
) else (
    powershell -Command "Compress-Archive -Path '%OUTPUT_DIR%' -DestinationPath '%OUTPUT_DIR%.zip'" >nul 2>&1
    if %errorlevel% == 0 (
        echo [+] Zip created with PowerShell
    ) else (
        echo [!] Failed to create zip, please manually zip: %OUTPUT_DIR%
    )
)

echo [*] Cleaning up...
rmdir /s /q "%OUTPUT_DIR%" 2>nul

echo.
echo  ============================================
echo    Build Complete!
echo  ============================================
echo.
echo  Output: %OUTPUT_DIR%.zip
echo.
pause
