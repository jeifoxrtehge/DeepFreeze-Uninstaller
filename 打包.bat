@echo off
chcp 65001 >nul
title 打包 DeepFreeze Uninstaller
cls
color 0A

echo.
echo  ============================================
echo    打包 DeepFreeze Uninstaller
echo  ============================================
echo.

set "VERSION=v1.0.0"
set "OUTPUT_DIR=DeepFreeze-Uninstaller-%VERSION%"

echo [*] 正在创建发布目录...
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%"

echo [*] 复制文件...
copy "README.md" "%OUTPUT_DIR%\" >nul
copy "LICENSE" "%OUTPUT_DIR%\" >nul
copy "启动器.bat" "%OUTPUT_DIR%\" >nul
copy "一键斩杀冰点还原.bat" "%OUTPUT_DIR%\" >nul
copy "强力uninstall 冰点还原.py" "%OUTPUT_DIR%\" >nul
copy "强力uninstall 冰点还原_GUI.py" "%OUTPUT_DIR%\" >nul
copy "强力uninstall 冰点还原_专业版.py" "%OUTPUT_DIR%\" >nul

echo [*] 检查是否安装 PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [!] 未安装 PyInstaller，跳过生成 exe
    echo [*] 安装命令: pip install pyinstaller
) else (
    echo [*] 正在生成可执行文件...
    
    echo [*] 编译命令行版...
    pyinstaller --onefile --name "DeepFreeze_Uninstaller_CLI" "强力uninstall 冰点还原.py" >nul 2>&1
    
    echo [*] 编译图形界面版...
    pyinstaller --onefile --windowed --name "DeepFreeze_Uninstaller_GUI" "强力uninstall 冰点还原_GUI.py" >nul 2>&1
    
    echo [*] 编译专业版...
    pyinstaller --onefile --name "DeepFreeze_Uninstaller_Pro" "强力uninstall 冰点还原_专业版.py" >nul 2>&1
    
    if exist "dist\DeepFreeze_Uninstaller_CLI.exe" (
        copy "dist\DeepFreeze_Uninstaller_CLI.exe" "%OUTPUT_DIR%\" >nul
        echo [+] 命令行版编译成功
    )
    
    if exist "dist\DeepFreeze_Uninstaller_GUI.exe" (
        copy "dist\DeepFreeze_Uninstaller_GUI.exe" "%OUTPUT_DIR%\" >nul
        echo [+] 图形界面版编译成功
    )
    
    if exist "dist\DeepFreeze_Uninstaller_Pro.exe" (
        copy "dist\DeepFreeze_Uninstaller_Pro.exe" "%OUTPUT_DIR%\" >nul
        echo [+] 专业版编译成功
    )
    
    echo [*] 清理临时文件...
    rmdir /s /q build 2>nul
    rmdir /s /q dist 2>nul
    del /q *.spec 2>nul
)

echo [*] 创建压缩包...
if exist "%OUTPUT_DIR%.zip" del "%OUTPUT_DIR%.zip"

:: 尝试使用 7z
where 7z >nul 2>&1
if %errorlevel% == 0 (
    7z a -tzip "%OUTPUT_DIR%.zip" "%OUTPUT_DIR%\" >nul
    echo [+] 使用 7z 创建压缩包成功
) else (
    :: 尝试使用 PowerShell
    powershell -Command "Compress-Archive -Path '%OUTPUT_DIR%' -DestinationPath '%OUTPUT_DIR%.zip'" >nul 2>&1
    if %errorlevel% == 0 (
        echo [+] 使用 PowerShell 创建压缩包成功
    ) else (
        echo [!] 无法创建压缩包，请手动压缩目录: %OUTPUT_DIR%
    )
)

echo [*] 清理临时目录...
rmdir /s /q "%OUTPUT_DIR%" 2>nul

echo.
echo  ============================================
echo    打包完成！
echo  ============================================
echo.
echo  输出文件: %OUTPUT_DIR%.zip
echo.
echo  包含内容:
echo  - DeepFreeze_Uninstaller_CLI.exe (命令行版)
echo  - DeepFreeze_Uninstaller_GUI.exe (图形界面版)
echo  - DeepFreeze_Uninstaller_Pro.exe (专业版)
echo  - 启动器.bat
echo  - Python 源代码
echo  - README.md
echo  - LICENSE
echo.
pause
