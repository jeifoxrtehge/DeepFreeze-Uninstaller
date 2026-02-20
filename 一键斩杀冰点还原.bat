Windows Registry Editor Version 5.00

@echo off
cls
title 冰点还原一键斩杀 SYSTEM-RAMOS-ZDY 制作
IF /I "%SystemDrive%"=="X:" (goto start) ELSE (
echo 警告：检测到当前系统可能不是PE系统，本软件必须在PE下运行！
echo.
echo 但如果你能确定你是在PE或 WinToGo 中运行的本程序，请按任意键继续...
pause>nul
)
:start
cls
title 冰点还原一键斩杀 SYSTEM-RAMOS-ZDY 制作
color 2f
echo.
echo 欢迎使用 @SYSTEM-RAMOS-ZDY 编写的冰点还原一键斩杀软件。
echo.
echo 本工具会自动备份 Windows\system32\config\SYSTEM 注册表文件至系统盘根目录 SYSTEM.bak ，如果运行本工具后系统出现蓝屏无法启动的情况，可以恢复注册表。
echo.
echo 本工具为 @SYSTEM-RAMOS-ZDY 原创，未经授权禁止转载。
echo.
echo 请在 PE 下运行本工具，在主系统运行无效。
echo.
echo 本工具编写不易，望大家可以给个点赞！！谢谢各位！
echo.
echo.echo 作者B站主页：https://space.bilibili.com/493998035
echo.
echo.
SET/p Disk=请输入【冰点还原的所在的系统的分区】的盘符（只要字母，不要冒号）：
echo.
IF /I "%Disk%"=="" GOTO start
set ZDY=%Disk:~0,1%
IF EXIST "%ZDY%:\Windows\system32\config\SYSTEM" (GOTO CopySYSTEM) ELSE (
cls
color 4f
echo 错误：指定的目录 %ZDY%: 中不包含 Windows 操作系统！请重新输入！
echo.
echo.
echo 错误：指定的路径 %ZDY%:\Windows\system32\config\SYSTEM 不存在或无法访问！
echo.
echo.
echo 如果无法确认错误原因，请联系作者 SYSTEM-RAMOS-ZDY 以获得帮助。
pause>nul
GOTO start
)
:CopySYSTEM
echo 正在备份%ZDY%盘 SYSTEM 注册表到 %ZDY%:\SYSTEM.bak
IF EXIST "%ZDY%:\SYSTEM.bak" (ren %ZDY%:\SYSTEM.bak SYSTEM.bak2)
copy %ZDY%:\Windows\system32\config\SYSTEM %ZDY%:\SYSTEM.bak
echo.
IF EXIST "%ZDY%:\SYSTEM.bak" (goto killdeepfrz) ELSE (
set reason=%ZDY%:\SYSTEM.bak 文件备份失败，请确认本软件是在 PE 下运行，且对相关目录具有访问权限。由于本软件不能保证一定能够破解成功，为了防止破解后系统出现蓝屏的情况，必须要备份 SYSTEM 注册表文件，在需要时可以还原。
set error=%errorlevel%
goto error
)
:killdeepfrz
echo %ZDY%:\SYSTEM.bak 注册表文件备份成功！即将执行暴力破解冰点还原！
echo.
echo 按任意键开始暴力破解冰点还原......
pause>nul
echo.
cls
echo 正在加载%ZDY%盘 SYSTEM 注册表，请稍候......
reg load HKLM\SYSTEM-RAMOS-ZDY %ZDY%:\Windows\system32\config\SYSTEM
IF /I NOT "%errorlevel%"=="0" (
set error=%errorlevel%
set reason=注册表文件加载失败，请检查是否是在PE环境下，而且注册表路径是否正确。
GOTO ERROR
)
echo.
echo 正在暴力卸载冰点还原的核心驱动，请稍候......
reg import %0
IF /I NOT "%errorlevel%"=="0" (
set error=%errorlevel%
set reason=注册表文件导入失败，卸载冰点还原的核心驱动失败。
GOTO ERROR
)
echo.
echo 正在修复被冰点还原劫持的系统存储卷、鼠标、键盘、磁盘驱动器，请稍候......
reg import %0
echo.
echo 正在卸载%ZDY%盘 SYSTEM 注册表，请稍候......
reg unload HKLM\SYSTEM-RAMOS-ZDY
echo.
echo.
echo 所有的操作已经成功完成，系统原本的 SYSTEM 注册表已经备份在 %ZDY%:\ ，如果系统启动蓝屏，请将此文件替换到 %ZDY%:\Windows\system32\config\SYSTEM。
echo.
echo 感谢您使用本工具。 编写、测试人员：@SYSTEM-RAMOS-ZDY
echo.
echo 本工具编写不易，望大家可以给个点赞！！谢谢各位！
echo.
echo 作者B站主页：https://space.bilibili.com/493998035
echo.
echo 按任意键退出本工具。
pause>nul
exit
:error
color 4f
echo.
echo 操作失败，正在还原更改......
echo.
reg unload HKLM\SYSTEM-RAMOS-ZDY
copy /y %ZDY%:\SYSTEM.bak %ZDY%:\Windows\system32\config\SYSTEM
cls
echo 错误：%reason%
echo.
echo 如果无法确认错误原因，请联系作者 SYSTEM-RAMOS-ZDY 以获得帮助。
echo.
echo 请访问 https://space.bilibili.com/493998035 给作者提供以下错误代码：
echo.
echo 错误代码：%error%
echo.
echo 已经为您还原所有更改，请按任意键退出本程序。
pause>nul
exit


[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\Control\Class\{71A27CDD-812A-11D0-BEC7-08002BE2092F}]
"UpperFilters"=-

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\services\DeepFrz]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\services\DfDiskLo]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\services\DFFilter]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\services\DFServ]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\services\eventlog\System\DeepFrz]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\services\FarDisk]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\services\FarSpace]

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\Control\Class\{4D36E967-E325-11CE-BFC1-08002BE10318}]
"UpperFilters"=hex(7):50,00,61,00,72,00,74,00,4d,00,67,00,72,00,00,00,00,00
"LowerFilters"=hex(7):69,00,61,00,53,00,74,00,6f,00,72,00,46,00, 00,00,00,00

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\Control\Class\{4D36E96B-E325-11CE-BFC1-08002BE10318}]
"UpperFilters"=hex(7):6b,00,62,00,64,00,63,00,6c,00,61,00,73,00,73,00,00,00,00,\
  00

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\Control\Class\{4D36E96C-E325-11CE-BFC1-08002BE10318}\0000\Settings\Drv8311_DevType_0662_SS1025102a]
"PCOSS"=hex:38,ad,42,a8,bf,0d,92,3b,3f,8e,0a,60,e3,3d,2a,a0,a2,75,64,81,35,84,\
  2d,dd,8c,01,e5,46,66,ce,bc,12

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet001\Control\Class\{4D36E96F-E325-11CE-BFC1-08002BE10318}]
"UpperFilters"=hex(7):6d,00,6f,00,75,00,63,00,6c,00,61,00,73,00,73,00,00,00,00,\
  00


[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\Control\Class\{71A27CDD-812A-11D0-BEC7-08002BE2092F}]
"UpperFilters"=-

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\services\DeepFrz]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\services\DfDiskLo]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\services\DFFilter]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\services\DFServ]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\services\eventlog\System\DeepFrz]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\services\FarDisk]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\services\FarSpace]

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\Control\Class\{4D36E967-E325-11CE-BFC1-08002BE10318}]
"UpperFilters"=hex(7):50,00,61,00,72,00,74,00,4d,00,67,00,72,00,00,00,00,00
"LowerFilters"=hex(7):69,00,61,00,53,00,74,00,6f,00,72,00,46,00,00,00,00,00

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\Control\Class\{4D36E96B-E325-11CE-BFC1-08002BE10318}]
"UpperFilters"=hex(7):6b,00,62,00,64,00,63,00,6c,00,61,00,73,00,73,00,00,00,00,\
  00

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\Control\Class\{4D36E96C-E325-11CE-BFC1-08002BE10318}\0000\Settings\Drv8311_DevType_0662_SS1025102a]
"PCOSS"=hex:38,ad,42,a8,bf,0d,92,3b,3f,8e,0a,60,e3,3d,2a,a0,a2,75,64,81,35,84,\
  2d,dd,8c,01,e5,46,66,ce,bc,12

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet002\Control\Class\{4D36E96F-E325-11CE-BFC1-08002BE10318}]
"UpperFilters"=hex(7):6d,00,6f,00,75,00,63,00,6c,00,61,00,73,00,73,00,00,00,00,\
  00


[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\Control\Class\{71A27CDD-812A-11D0-BEC7-08002BE2092F}]
"UpperFilters"=-

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\services\DeepFrz]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\services\DfDiskLo]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\services\DFFilter]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\services\DFServ]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\services\eventlog\System\DeepFrz]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\services\FarDisk]

[-HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\services\FarSpace]

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\Control\Class\{4D36E967-E325-11CE-BFC1-08002BE10318}]
"UpperFilters"=hex(7):50,00,61,00,72,00,74,00,4d,00,67,00,72,00,00,00,00,00
"LowerFilters"=hex(7):69,00,61,00,53,00,74,00,6f,00,72,00,46,00,00,00,00,00

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\Control\Class\{4D36E96B-E325-11CE-BFC1-08002BE10318}]
"UpperFilters"=hex(7):6b,00,62,00,64,00,63,00,6c,00,61,00,73,00,73,00,00,00,00,\
  00

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\Control\Class\{4D36E96C-E325-11CE-BFC1-08002BE10318}\0000\Settings\Drv8311_DevType_0662_SS1025102a]
"PCOSS"=hex:38,ad,42,a8,bf,0d,92,3b,3f,8e,0a,60,e3,3d,2a,a0,a2,75,64,81,35,84,\
  2d,dd,8c,01,e5,46,66,ce,bc,12

[HKEY_LOCAL_MACHINE\SYSTEM-RAMOS-ZDY\ControlSet003\Control\Class\{4D36E96F-E325-11CE-BFC1-08002BE10318}]
"UpperFilters"=hex(7):6d,00,6f,00,75,00,63,00,6c,00,61,00,73,00,73,00,00,00,00,\
  00
