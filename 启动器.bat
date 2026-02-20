@echo off
chcp 65001 >nul
title 冰点还原卸载工具集
cls
color 0A

echo.
echo  ============================================
echo    冰点还原卸载工具集
echo    作者参考: SYSTEM-RAMOS-ZDY
echo    B站: https://space.bilibili.com/493998035
echo  ============================================
echo.
echo  请选择要运行的工具:
echo.
echo  [1] 强力卸载冰点还原 - 命令行版
echo      适合熟悉命令行的用户，功能完整
echo.
echo  [2] 强力卸载冰点还原 - 图形界面版
echo      适合普通用户，可视化操作
echo.
echo  [3] 强力卸载冰点还原 - 专业版
echo      推荐！整合SYSTEM-RAMOS-ZDY技术
echo      修复驱动过滤器，处理更彻底
echo.
echo  [4] 一键斩杀冰点还原 - 原版BAT
echo      SYSTEM-RAMOS-ZDY的原版工具
echo.
echo  [5] 查看使用说明
echo.
echo  [0] 退出
echo.
echo  ============================================
echo.

set /p choice=请输入选项 (0-5): 

if "%choice%"=="1" goto cmd_version
if "%choice%"=="2" goto gui_version
if "%choice%"=="3" goto pro_version
if "%choice%"=="4" goto bat_version
if "%choice%"=="5" goto help
if "%choice%"=="0" goto exit
goto invalid

:cmd_version
echo.
echo 正在启动命令行版...
echo.
python "强力uninstall 冰点还原.py"
pause
goto start

:gui_version
echo.
echo 正在启动图形界面版...
echo.
python "强力uninstall 冰点还原_GUI.py"
pause
goto start

:pro_version
echo.
echo 正在启动专业版...
echo.
python "强力uninstall 冰点还原_专业版.py"
pause
goto start

:bat_version
echo.
echo 正在启动原版BAT工具...
echo.
call "一键斩杀冰点还原.bat"
goto start

:help
echo.
echo  ============================================
echo              使用说明
echo  ============================================
echo.
echo  【重要提示】
echo  1. 本工具必须在 PE 系统下运行！
echo  2. 运行前请确认系统盘盘符（可能不是C盘）
echo  3. 操作前会自动备份注册表，可恢复
echo.
echo  【使用步骤】
echo  1. 制作PE启动盘（微PE、优启通等）
echo  2. 进入PE系统
echo  3. 确认系统盘盘符（打开文件管理器查看）
echo  4. 运行本工具，选择版本
echo  5. 按提示操作，等待完成
echo  6. 重启计算机
echo.
echo  【版本选择建议】
echo  - 普通用户: 选择图形界面版或专业版
echo  - 高级用户: 选择命令行版或专业版
echo  - 推荐: 专业版（修复驱动过滤器）
echo.
echo  【问题恢复】
echo  如果卸载后系统蓝屏:
echo  1. 重新进入PE
echo  2. 找到备份文件（通常在系统盘根目录）
echo  3. 将 SYSTEM.bak 复制到:
echo     X:\Windows\System32\config\SYSTEM
echo  4. 重启计算机
echo.
echo  ============================================
echo.
pause
goto start

:invalid
echo.
echo [!] 无效选项，请重新选择
echo.
pause
goto start

:exit
echo.
echo 感谢使用，再见！
echo.
timeout /t 2 /nobreak >nul
exit

:start
goto start
