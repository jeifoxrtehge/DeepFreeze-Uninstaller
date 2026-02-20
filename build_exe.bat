@echo off
title Build DeepFreeze Uninstaller EXE
cls
color 0A

echo.
echo  ============================================
echo    Build Standalone EXE Files
echo  ============================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [!] PyInstaller not found!
    echo [*] Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [!] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo [*] PyInstaller found
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
del /q *.spec 2>nul

echo [*] Building CLI version...
pyinstaller --onefile --name "DeepFreeze_Uninstaller_CLI" "强力uninstall 冰点还原.py"
if errorlevel 1 (
    echo [!] CLI build failed
    pause
    exit /b 1
)

echo.
echo [*] Building GUI version...
pyinstaller --onefile --windowed --name "DeepFreeze_Uninstaller_GUI" "强力uninstall 冰点还原_GUI.py"
if errorlevel 1 (
    echo [!] GUI build failed
    pause
    exit /b 1
)

echo.
echo [*] Building Pro version...
pyinstaller --onefile --name "DeepFreeze_Uninstaller_Pro" "强力uninstall 冰点还原_专业版.py"
if errorlevel 1 (
    echo [!] Pro build failed
    pause
    exit /b 1
)

echo.
echo  ============================================
echo    Build Complete!
echo  ============================================
echo.
echo  Output files in dist folder:
echo  - DeepFreeze_Uninstaller_CLI.exe
echo  - DeepFreeze_Uninstaller_GUI.exe
echo  - DeepFreeze_Uninstaller_Pro.exe
echo.
pause
