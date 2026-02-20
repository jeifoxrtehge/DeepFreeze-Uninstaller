#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import shutil
import subprocess
import winreg
import ctypes
import datetime
from pathlib import Path


def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def is_pe_environment():
    """检测是否在 PE 环境下"""
    pe_indicators = [
        not os.path.exists(r"C:\Windows\System32\sc.exe"),
        os.path.exists(r"X:\Windows\System32\winpeshl.exe"),
        "PE" in os.environ.get("SYSTEMDRIVE", ""),
    ]
    return any(pe_indicators)


def get_system_drive():
    """询问用户系统盘路径"""
    print("[*] 请确认系统盘路径（PE环境下盘符可能变化）")
    print("[*] 例如: C 或 D 或 E")
    drive = input("请输入系统盘盘符 (默认 C): ").strip().upper()
    if not drive:
        drive = "C"
    if len(drive) == 1 and drive.isalpha():
        return f"{drive}:"
    return drive


def backup_system_file(system_drive):
    """备份 SYSTEM 注册表文件（直接复制文件）"""
    print("[*] 正在备份 SYSTEM 注册表文件...")

    system_file = f"{system_drive}\\Windows\\System32\\config\\SYSTEM"
    backup_file = f"{system_drive}\\SYSTEM.bak"

    if not os.path.exists(system_file):
        print(f"[!] 错误: 找不到 SYSTEM 文件: {system_file}")
        print("[!] 请确认系统盘路径是否正确")
        return None

    # 如果已有备份，重命名为 .bak2
    if os.path.exists(backup_file):
        backup_file2 = f"{system_drive}\\SYSTEM.bak2"
        try:
            if os.path.exists(backup_file2):
                os.remove(backup_file2)
            shutil.move(backup_file, backup_file2)
            print(f"[*] 已重命名旧备份为: SYSTEM.bak2")
        except Exception as e:
            print(f"[!] 重命名旧备份时出错: {e}")

    try:
        shutil.copy2(system_file, backup_file)
        print(f"[+] SYSTEM 文件已备份到: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"[!] 备份 SYSTEM 文件时出错: {e}")
        return None


def restore_system_file(system_drive):
    """恢复 SYSTEM 注册表文件"""
    backup_file = f"{system_drive}\\SYSTEM.bak"
    system_file = f"{system_drive}\\Windows\\System32\\config\\SYSTEM"

    if os.path.exists(backup_file):
        try:
            shutil.copy2(backup_file, system_file)
            print(f"[+] 已恢复 SYSTEM 文件")
            return True
        except Exception as e:
            print(f"[!] 恢复 SYSTEM 文件时出错: {e}")
    return False


def load_registry_hive(system_drive):
    """加载 SYSTEM 注册表配置单元"""
    print("[*] 正在加载 SYSTEM 注册表...")

    hive_path = f"{system_drive}\\Windows\\System32\\config\\SYSTEM"
    hive_name = "DF_UNINSTALL"

    if not os.path.exists(hive_path):
        print(f"[!] 错误: 找不到注册表文件: {hive_path}")
        return None

    try:
        # 先尝试卸载（如果之前加载失败）
        subprocess.run(
            ["reg", "unload", f"HKLM\\{hive_name}"],
            capture_output=True,
            check=False
        )

        result = subprocess.run(
            ["reg", "load", f"HKLM\\{hive_name}", hive_path],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            print(f"[+] 注册表加载成功: HKLM\\{hive_name}")
            return hive_name
        else:
            print(f"[!] 加载注册表失败: {result.stderr}")
            return None
    except Exception as e:
        print(f"[!] 加载注册表时出错: {e}")
        return None


def unload_registry_hive(hive_name):
    """卸载注册表配置单元"""
    print("[*] 正在卸载注册表配置单元...")
    try:
        result = subprocess.run(
            ["reg", "unload", f"HKLM\\{hive_name}"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            print(f"[+] 已卸载: HKLM\\{hive_name}")
        else:
            print(f"[!] 卸载失败: {result.stderr}")
    except Exception as e:
        print(f"[!] 卸载注册表时出错: {e}")


def fix_driver_filters(hive_name):
    """修复被冰点还原劫持的驱动过滤器"""
    print("[*] 正在修复驱动过滤器...")

    # 定义需要修复的注册表项
    fixes = [
        # 存储卷驱动 (DiskDrive)
        {
            "path": f"HKLM\\{hive_name}\\ControlSet001\\Control\\Class\\{{4D36E967-E325-11CE-BFC1-08002BE10318}}",
            "values": {
                "UpperFilters": "PartMgr\0",
                "LowerFilters": "iaStorF\0",
            }
        },
        # 键盘驱动
        {
            "path": f"HKLM\\{hive_name}\\ControlSet001\\Control\\Class\\{{4D36E96B-E325-11CE-BFC1-08002BE10318}}",
            "values": {
                "UpperFilters": "kbdclass\0",
            }
        },
        # 鼠标驱动
        {
            "path": f"HKLM\\{hive_name}\\ControlSet001\\Control\\Class\\{{4D36E96F-E325-11CE-BFC1-08002BE10318}}",
            "values": {
                "UpperFilters": "mouclass\0",
            }
        },
        # 删除 UpperFilters 中的 DeepFrz
        {
            "path": f"HKLM\\{hive_name}\\ControlSet001\\Control\\Class\\{{71A27CDD-812A-11D0-BEC7-08002BE2092F}}",
            "delete_values": ["UpperFilters"],
        },
    ]

    # 同样处理 ControlSet002 和 ControlSet003
    control_sets = ["ControlSet001", "ControlSet002", "ControlSet003"]

    for control_set in control_sets:
        print(f"[*] 处理 {control_set}...")

        # 修复存储卷驱动
        try:
            key_path = f"{hive_name}\\{control_set}\\Control\\Class\\{{4D36E967-E325-11CE-BFC1-08002BE10318}}"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)

            # 设置 UpperFilters 为 PartMgr
            winreg.SetValueEx(key, "UpperFilters", 0, winreg.REG_MULTI_SZ, ["PartMgr"])
            # 设置 LowerFilters 为 iaStorF
            winreg.SetValueEx(key, "LowerFilters", 0, winreg.REG_MULTI_SZ, ["iaStorF"])

            winreg.CloseKey(key)
            print(f"[+] {control_set}: 存储卷驱动过滤器已修复")
        except Exception as e:
            print(f"[!] {control_set}: 修复存储卷驱动失败: {e}")

        # 修复键盘驱动
        try:
            key_path = f"{hive_name}\\{control_set}\\Control\\Class\\{{4D36E96B-E325-11CE-BFC1-08002BE10318}}"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "UpperFilters", 0, winreg.REG_MULTI_SZ, ["kbdclass"])
            winreg.CloseKey(key)
            print(f"[+] {control_set}: 键盘驱动过滤器已修复")
        except Exception as e:
            print(f"[!] {control_set}: 修复键盘驱动失败: {e}")

        # 修复鼠标驱动
        try:
            key_path = f"{hive_name}\\{control_set}\\Control\\Class\\{{4D36E96F-E325-11CE-BFC1-08002BE10318}}"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "UpperFilters", 0, winreg.REG_MULTI_SZ, ["mouclass"])
            winreg.CloseKey(key)
            print(f"[+] {control_set}: 鼠标驱动过滤器已修复")
        except Exception as e:
            print(f"[!] {control_set}: 修复鼠标驱动失败: {e}")

        # 删除 DeepFrz 的 UpperFilters
        try:
            key_path = f"{hive_name}\\{control_set}\\Control\\Class\\{{71A27CDD-812A-11D0-BEC7-08002BE2092F}}"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, "UpperFilters")
                print(f"[+] {control_set}: 已删除 DeepFrz UpperFilters")
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[!] {control_set}: 删除 DeepFrz UpperFilters 失败: {e}")


def delete_deepfreeze_services(hive_name):
    """删除冰点还原服务"""
    print("[*] 正在删除冰点还原服务...")

    services = [
        "DeepFrz",
        "DfDiskLo",
        "DFFilter",
        "DFServ",
        "FarDisk",
        "FarSpace",
    ]

    control_sets = ["ControlSet001", "ControlSet002", "ControlSet003"]

    for control_set in control_sets:
        print(f"[*] 处理 {control_set}...")

        for service in services:
            try:
                service_path = f"{hive_name}\\{control_set}\\Services\\{service}"
                winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, service_path)
                print(f"[+] 已删除服务: {service}")
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"[!] 删除服务 {service} 失败: {e}")

        # 删除事件日志
        try:
            eventlog_path = f"{hive_name}\\{control_set}\\Services\\eventlog\\System\\DeepFrz"
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, eventlog_path)
            print(f"[+] 已删除 DeepFrz 事件日志")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"[!] 删除事件日志失败: {e}")


def delete_deepfreeze_files(system_drive):
    """删除冰点还原文件"""
    print("[*] 正在删除冰点还原文件...")

    paths_to_delete = [
        f"{system_drive}\\Program Files\\Faronics",
        f"{system_drive}\\Program Files (x86)\\Faronics",
        f"{system_drive}\\Windows\\System32\\drivers\\DeepFrz.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DfDiskLo.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DfDiskUp.sys",
        f"{system_drive}\\Windows\\System32\\DF5Serv.exe",
        f"{system_drive}\\Windows\\System32\\DF6Serv.exe",
        f"{system_drive}\\Windows\\System32\\DF7Serv.exe",
        f"{system_drive}\\Windows\\System32\\DF8Serv.exe",
        f"{system_drive}\\Windows\\System32\\DFServ.exe",
        f"{system_drive}\\Windows\\System32\\Dfrfos.exe",
        f"{system_drive}\\Windows\\System32\\drivers\\DfDriver.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DFEngine.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DFFilter.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DFVol.sys",
    ]

    for path in paths_to_delete:
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    print(f"[*] 删除目录: {path}")
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    print(f"[*] 删除文件: {path}")
                    os.remove(path)
        except Exception as e:
            print(f"[!] 删除 {path} 失败: {e}")


def main():
    print("=" * 70)
    print("强力卸载冰点还原精灵 (Deep Freeze) - 专业版")
    print("参考: SYSTEM-RAMOS-ZDY 的一键斩杀工具")
    print("改作者github:https://github.com/jeifoxrtehge/")
    print("=" * 70)
    print()
    print("[!] 警告: 此脚本将强制删除冰点还原的所有文件和注册表项")
    print("[!] 建议在 PE 系统下运行此脚本")
    print("[!] 操作前已自动备份 SYSTEM 注册表文件")
    print()

    if not is_admin():
        print("[!] 错误: 请以管理员权限运行此脚本!")
        input("按回车键退出...")
        sys.exit(1)

    # 获取系统盘
    system_drive = get_system_drive()
    print(f"[*] 系统盘设置为: {system_drive}")
    print()

    # 1. 备份 SYSTEM 文件
    print("[1/6] 备份 SYSTEM 注册表文件...")
    backup_file = backup_system_file(system_drive)
    if not backup_file:
        print("[!] 备份失败，无法继续")
        input("按回车键退出...")
        sys.exit(1)
    print()

    # 2. 加载注册表
    print("[2/6] 加载 SYSTEM 注册表...")
    hive_name = load_registry_hive(system_drive)
    if not hive_name:
        print("[!] 注册表加载失败，正在恢复...")
        restore_system_file(system_drive)
        input("按回车键退出...")
        sys.exit(1)
    print()

    # 确认继续
    confirm = input("备份完成，确定要继续卸载吗? (yes/no): ")
    if confirm.lower() != "yes":
        print("[*] 操作已取消，恢复注册表...")
        unload_registry_hive(hive_name)
        input("按回车键退出...")
        sys.exit(0)

    print()

    try:
        # 3. 删除服务
        print("[3/6] 删除冰点还原服务...")
        delete_deepfreeze_services(hive_name)
        print()

        # 4. 修复驱动过滤器
        print("[4/6] 修复被劫持的驱动过滤器...")
        fix_driver_filters(hive_name)
        print()

        # 5. 删除文件
        print("[5/6] 删除冰点还原文件...")
        delete_deepfreeze_files(system_drive)
        print()

        # 6. 卸载注册表
        print("[6/6] 卸载注册表配置单元...")
        unload_registry_hive(hive_name)
        print()

        print("=" * 70)
        print("[+] 卸载完成!")
        print(f"[*] SYSTEM 注册表备份位置: {backup_file}")
        print("[*] 如果系统启动蓝屏，请将备份文件替换到:")
        print(f"    {system_drive}\\Windows\\System32\\config\\SYSTEM")
        print("=" * 70)

    except Exception as e:
        print()
        print("[!] 发生错误，正在恢复...")
        print(f"[!] 错误信息: {e}")
        unload_registry_hive(hive_name)
        restore_system_file(system_drive)
        print("[+] 已恢复 SYSTEM 文件")

    print()
    input("按回车键退出...")


if __name__ == "__main__":
    main()
