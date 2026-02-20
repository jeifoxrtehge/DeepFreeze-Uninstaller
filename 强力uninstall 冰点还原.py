#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强力卸载冰点还原精灵 (Deep Freeze)
使用方法：在 PE 系统下运行此脚本
"""

import os
import sys
import shutil
import subprocess
import winreg
import ctypes
from pathlib import Path


def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


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


def load_registry_hives(system_drive):
    """加载系统注册表配置单元"""
    print("[*] 正在加载系统注册表...")

    hives = [
        (f"{system_drive}\\Windows\\System32\\config\\SOFTWARE", "PE_SOFTWARE"),
        (f"{system_drive}\\Windows\\System32\\config\\SYSTEM", "PE_SYSTEM"),
    ]

    loaded = []
    for hive_path, name in hives:
        if os.path.exists(hive_path):
            try:
                result = subprocess.run(
                    ["reg", "load", f"HKLM\\{name}", hive_path],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    print(f"[+] 已加载: {hive_path} -> HKLM\\{name}")
                    loaded.append(name)
                else:
                    print(f"[!] 加载失败: {hive_path}")
                    print(f"    错误: {result.stderr}")
            except Exception as e:
                print(f"[!] 加载 {hive_path} 时出错: {e}")
        else:
            print(f"[!] 找不到文件: {hive_path}")

    return loaded


def unload_registry_hives(hive_names):
    """卸载注册表配置单元"""
    print("[*] 正在卸载注册表配置单元...")
    for name in hive_names:
        try:
            subprocess.run(
                ["reg", "unload", f"HKLM\\{name}"],
                capture_output=True,
                check=False
            )
            print(f"[+] 已卸载: HKLM\\{name}")
        except Exception as e:
            print(f"[!] 卸载 {name} 时出错: {e}")


def backup_registry(system_drive):
    """备份注册表"""
    import datetime
    backup_dir = f"{system_drive}\\DeepFreeze_Uninstall_Backup"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    print("[*] 正在备份注册表...")

    registry_keys = [
        ("HKLM\\PE_SOFTWARE\\Faronics", "faronics_software"),
        ("HKLM\\PE_SOFTWARE\\WOW6432Node\\Faronics", "faronics_software_wow64"),
        ("HKLM\\PE_SYSTEM\\ControlSet001\\Services", "services"),
    ]

    for reg_path, name in registry_keys:
        backup_file = os.path.join(backup_dir, f"{name}_{timestamp}.reg")
        try:
            result = subprocess.run(
                ["reg", "export", reg_path, backup_file, "/y"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                print(f"[+] 已备份: {reg_path} -> {backup_file}")
            else:
                print(f"[!] 备份失败: {reg_path}")
        except Exception as e:
            print(f"[!] 备份 {reg_path} 时出错: {e}")

    print(f"[*] 注册表备份完成，保存在: {backup_dir}")
    return backup_dir


def is_pe_environment():
    """检测是否在 PE 环境下"""
    # PE 环境通常没有某些系统命令或服务
    pe_indicators = [
        not os.path.exists(r"C:\Windows\System32\sc.exe"),
        os.path.exists(r"X:\Windows\System32\winpeshl.exe"),
        "PE" in os.environ.get("SYSTEMDRIVE", ""),
    ]
    return any(pe_indicators)


def stop_deepfreeze_services():
    """停止冰点还原相关服务"""
    # PE 环境下通常没有 sc 命令，跳过此步骤
    if is_pe_environment():
        print("[*] 检测到 PE 环境，跳过服务停止步骤（通过注册表删除服务）")
        return

    services = [
        "Deep Freeze",
        "DFServ",
        "DF5Serv",
        "DF6Serv",
        "DF7Serv",
        "DF8Serv",
    ]

    for service in services:
        try:
            print(f"[*] 正在停止服务: {service}")
            subprocess.run(
                ["sc", "stop", service],
                capture_output=True,
                check=False
            )
            subprocess.run(
                ["sc", "delete", service],
                capture_output=True,
                check=False
            )
        except Exception as e:
            print(f"[!] 停止服务 {service} 时出错: {e}")


def kill_deepfreeze_processes():
    """结束冰点还原进程"""
    # PE 环境下通常没有 taskkill 命令，跳过此步骤
    if is_pe_environment():
        print("[*] 检测到 PE 环境，跳过进程结束步骤（系统未运行）")
        return

    processes = [
        "DF5Serv.exe",
        "DF6Serv.exe",
        "DF7Serv.exe",
        "DF8Serv.exe",
        "DFServ.exe",
        "Dfrfos.exe",
        "Dfserv.exe",
        "FrzState2k.exe",
        "Deep Freeze.exe",
    ]

    for proc in processes:
        try:
            print(f"[*] 正在结束进程: {proc}")
            subprocess.run(
                ["taskkill", "/F", "/T", "/IM", proc],
                capture_output=True,
                check=False
            )
        except Exception as e:
            print(f"[!] 结束进程 {proc} 时出错: {e}")


def delete_deepfreeze_files(system_drive):
    """删除冰点还原文件"""
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
                    print(f"[*] 正在删除目录: {path}")
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    print(f"[*] 正在删除文件: {path}")
                    os.remove(path)
        except Exception as e:
            print(f"[!] 删除 {path} 时出错: {e}")


def remove_registry_entries():
    """删除注册表项"""
    registry_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SOFTWARE\Faronics"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SOFTWARE\WOW6432Node\Faronics"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\Deep Freeze"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DFServ"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DF5Serv"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DF6Serv"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DF7Serv"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DF8Serv"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DeepFrz"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DfDiskLo"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DfDiskUp"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DfDriver"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DFEngine"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DFFilter"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SYSTEM\ControlSet001\Services\DFVol"),
    ]

    for hkey, path in registry_paths:
        try:
            print(f"[*] 正在删除注册表项: {path}")
            winreg.DeleteKey(hkey, path)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"[!] 删除注册表项 {path} 时出错: {e}")


def remove_startup_entries():
    """删除启动项"""
    startup_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "Deep Freeze"),
        (winreg.HKEY_LOCAL_MACHINE, r"PE_SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "DFServ"),
    ]

    for hkey, path, value_name in startup_paths:
        try:
            print(f"[*] 正在删除启动项: {value_name}")
            key = winreg.OpenKey(hkey, path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, value_name)
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"[!] 删除启动项 {value_name} 时出错: {e}")


def clean_driver_files(system_drive):
    """清理驱动文件"""
    driver_paths = [
        f"{system_drive}\\Windows\\System32\\drivers\\DeepFrz.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DfDiskLo.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DfDiskUp.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DfDriver.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DFEngine.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DFFilter.sys",
        f"{system_drive}\\Windows\\System32\\drivers\\DFVol.sys",
    ]

    for driver in driver_paths:
        try:
            if os.path.exists(driver):
                print(f"[*] 正在删除驱动: {driver}")
                os.remove(driver)
        except Exception as e:
            print(f"[!] 删除驱动 {driver} 时出错: {e}")


def main():
    print("=" * 60)
    print("强力卸载冰点还原精灵 (Deep Freeze)")
    print("=" * 60)
    print()
    print("[!] 警告: 此脚本将强制删除冰点还原的所有文件和注册表项")
    print("[!] 建议在 PE 系统下运行此脚本")
    print()

    if not is_admin():
        print("[!] 错误: 请以管理员权限运行此脚本!")
        input("按回车键退出...")
        sys.exit(1)

    # 获取系统盘
    system_drive = get_system_drive()
    print(f"[*] 系统盘设置为: {system_drive}")
    print()

    # 加载注册表配置单元
    loaded_hives = load_registry_hives(system_drive)
    if not loaded_hives:
        print("[!] 错误: 无法加载注册表，请检查系统盘路径是否正确")
        input("按回车键退出...")
        sys.exit(1)

    print()
    confirm = input("确定要继续卸载吗? (yes/no): ")
    if confirm.lower() != "yes":
        print("[*] 操作已取消")
        unload_registry_hives(loaded_hives)
        sys.exit(0)

    print()

    # 0. 备份注册表
    print("[0/7] 正在备份注册表...")
    backup_dir = backup_registry(system_drive)
    print()

    print("[*] 开始卸载冰点还原...")
    print()

    # 1. 结束进程（PE环境下可能不需要）
    print("[1/7] 正在结束冰点还原进程...")
    kill_deepfreeze_processes()
    print()

    # 2. 停止服务（PE环境下可能不需要）
    print("[2/7] 正在停止冰点还原服务...")
    stop_deepfreeze_services()
    print()

    # 3. 删除文件
    print("[3/7] 正在删除冰点还原文件...")
    delete_deepfreeze_files(system_drive)
    print()

    # 4. 删除注册表
    print("[4/7] 正在删除注册表项...")
    remove_registry_entries()
    print()

    # 5. 删除启动项
    print("[5/7] 正在删除启动项...")
    remove_startup_entries()
    print()

    # 6. 清理驱动
    print("[6/7] 正在清理驱动文件...")
    clean_driver_files(system_drive)
    print()

    # 7. 卸载注册表配置单元
    print("[7/7] 正在卸载注册表配置单元...")
    unload_registry_hives(loaded_hives)
    print()

    print("=" * 60)
    print("[*] 卸载完成!")
    print(f"[*] 注册表备份位置: {backup_dir}")
    print("[*] 如需恢复注册表，可以双击备份的 .reg 文件")
    print("[*] 建议重启计算机以完成清理")
    print("=" * 60)
    
    input("按回车键退出...")


if __name__ == "__main__":
    main()
