#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强力卸载冰点还原精灵 (Deep Freeze) - GUI版本
使用方法：在 PE 系统下运行此脚本
"""

import os
import sys
import shutil
import subprocess
import winreg
import ctypes
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import threading


class DeepFreezeUninstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("强力卸载冰点还原精灵")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # 设置样式
        self.style = ttk.Style()
        self.style.configure('TButton', font=('微软雅黑', 10))
        self.style.configure('TLabel', font=('微软雅黑', 10))
        self.style.configure('TEntry', font=('微软雅黑', 10))

        self.system_drive = tk.StringVar(value="C:")
        self.backup_dir = ""
        self.loaded_hives = []

        self.create_widgets()

    def create_widgets(self):
        # 标题
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            title_frame,
            text="强力卸载冰点还原精灵 (Deep Freeze)",
            font=('微软雅黑', 16, 'bold')
        )
        title_label.pack()

        # 警告信息
        warning_frame = ttk.Frame(self.root, padding="10")
        warning_frame.pack(fill=tk.X)

        warning_text = """警告：此脚本将强制删除冰点还原的所有文件和注册表项！
建议在 PE 系统下运行此脚本。
操作前请确保已备份重要数据。"""

        warning_label = ttk.Label(
            warning_frame,
            text=warning_text,
            foreground='red',
            font=('微软雅黑', 10),
            justify=tk.CENTER
        )
        warning_label.pack()

        # 系统盘选择
        drive_frame = ttk.LabelFrame(self.root, text="系统盘设置", padding="10")
        drive_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(drive_frame, text="系统盘盘符:").pack(side=tk.LEFT)
        drive_entry = ttk.Entry(drive_frame, textvariable=self.system_drive, width=10)
        drive_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(drive_frame, text="(PE环境下盘符可能变化，如 C、D、E)").pack(side=tk.LEFT)

        # 按钮区域
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)

        self.load_btn = ttk.Button(
            button_frame,
            text="1. 加载注册表",
            command=self.load_registry,
            width=20
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)

        self.backup_btn = ttk.Button(
            button_frame,
            text="2. 备份注册表",
            command=self.backup_registry_gui,
            width=20,
            state=tk.DISABLED
        )
        self.backup_btn.pack(side=tk.LEFT, padx=5)

        self.uninstall_btn = ttk.Button(
            button_frame,
            text="3. 开始卸载",
            command=self.start_uninstall,
            width=20,
            state=tk.DISABLED
        )
        self.uninstall_btn.pack(side=tk.LEFT, padx=5)

        # 进度条
        self.progress = ttk.Progressbar(
            self.root,
            orient=tk.HORIZONTAL,
            length=680,
            mode='determinate'
        )
        self.progress.pack(padx=10, pady=5)

        # 日志区域
        log_frame = ttk.LabelFrame(self.root, text="操作日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            height=20
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 底部按钮
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(fill=tk.X)

        ttk.Button(
            bottom_frame,
            text="清空日志",
            command=self.clear_log
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            bottom_frame,
            text="退出",
            command=self.root.quit
        ).pack(side=tk.RIGHT, padx=5)

    def log(self, message):
        """添加日志"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()

    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)

    def is_admin(self):
        """检查是否以管理员权限运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def load_registry(self):
        """加载注册表配置单元"""
        if not self.is_admin():
            messagebox.showerror("错误", "请以管理员权限运行此脚本!")
            return

        system_drive = self.system_drive.get()
        if not system_drive:
            messagebox.showerror("错误", "请输入系统盘盘符!")
            return

        self.log(f"[*] 系统盘设置为: {system_drive}")
        self.log("[*] 正在加载系统注册表...")

        hives = [
            (f"{system_drive}\\Windows\\System32\\config\\SOFTWARE", "PE_SOFTWARE"),
            (f"{system_drive}\\Windows\\System32\\config\\SYSTEM", "PE_SYSTEM"),
        ]

        self.loaded_hives = []
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
                        self.log(f"[+] 已加载: {hive_path} -> HKLM\\{name}")
                        self.loaded_hives.append(name)
                    else:
                        self.log(f"[!] 加载失败: {hive_path}")
                        self.log(f"    错误: {result.stderr}")
                except Exception as e:
                    self.log(f"[!] 加载 {hive_path} 时出错: {e}")
            else:
                self.log(f"[!] 找不到文件: {hive_path}")

        if self.loaded_hives:
            self.log("[+] 注册表加载成功!")
            self.backup_btn.config(state=tk.NORMAL)
            self.load_btn.config(state=tk.DISABLED)
            messagebox.showinfo("成功", "注册表加载成功!")
        else:
            messagebox.showerror("错误", "无法加载注册表，请检查系统盘路径是否正确")

    def backup_registry_gui(self):
        """备份注册表"""
        system_drive = self.system_drive.get()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = f"{system_drive}\\DeepFreeze_Uninstall_Backup"

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        self.log("[*] 正在备份注册表...")

        registry_keys = [
            ("HKLM\\PE_SOFTWARE\\Faronics", "faronics_software"),
            ("HKLM\\PE_SOFTWARE\\WOW6432Node\\Faronics", "faronics_software_wow64"),
            ("HKLM\\PE_SYSTEM\\ControlSet001\\Services", "services"),
        ]

        for reg_path, name in registry_keys:
            backup_file = os.path.join(self.backup_dir, f"{name}_{timestamp}.reg")
            try:
                result = subprocess.run(
                    ["reg", "export", reg_path, backup_file, "/y"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    self.log(f"[+] 已备份: {reg_path}")
                else:
                    self.log(f"[!] 备份失败: {reg_path}")
            except Exception as e:
                self.log(f"[!] 备份 {reg_path} 时出错: {e}")

        self.log(f"[*] 注册表备份完成，保存在: {self.backup_dir}")
        self.backup_btn.config(state=tk.DISABLED)
        self.uninstall_btn.config(state=tk.NORMAL)
        messagebox.showinfo("成功", f"注册表备份完成!\n保存位置: {self.backup_dir}")

    def start_uninstall(self):
        """开始卸载"""
        if not messagebox.askyesno("确认", "确定要卸载冰点还原吗?\n此操作不可恢复!"):
            return

        self.uninstall_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0

        # 在新线程中运行卸载
        thread = threading.Thread(target=self.uninstall_process)
        thread.start()

    def uninstall_process(self):
        """卸载过程"""
        system_drive = self.system_drive.get()
        steps = 7

        # 1. 结束进程
        self.log("[1/7] 正在结束冰点还原进程...")
        self.kill_deepfreeze_processes()
        self.progress['value'] = (1 / steps) * 100

        # 2. 停止服务
        self.log("[2/7] 正在停止冰点还原服务...")
        self.stop_deepfreeze_services()
        self.progress['value'] = (2 / steps) * 100

        # 3. 删除文件
        self.log("[3/7] 正在删除冰点还原文件...")
        self.delete_deepfreeze_files(system_drive)
        self.progress['value'] = (3 / steps) * 100

        # 4. 删除注册表
        self.log("[4/7] 正在删除注册表项...")
        self.remove_registry_entries()
        self.progress['value'] = (4 / steps) * 100

        # 5. 删除启动项
        self.log("[5/7] 正在删除启动项...")
        self.remove_startup_entries()
        self.progress['value'] = (5 / steps) * 100

        # 6. 清理驱动
        self.log("[6/7] 正在清理驱动文件...")
        self.clean_driver_files(system_drive)
        self.progress['value'] = (6 / steps) * 100

        # 7. 卸载注册表配置单元
        self.log("[7/7] 正在卸载注册表配置单元...")
        self.unload_registry_hives()
        self.progress['value'] = 100

        self.log("=" * 60)
        self.log("[*] 卸载完成!")
        self.log(f"[*] 注册表备份位置: {self.backup_dir}")
        self.log("[*] 如需恢复注册表，可以双击备份的 .reg 文件")
        self.log("[*] 建议重启计算机以完成清理")
        self.log("=" * 60)

        messagebox.showinfo("完成", "卸载完成!\n建议重启计算机以完成清理。")

    def kill_deepfreeze_processes(self):
        """结束冰点还原进程"""
        # PE 环境下通常没有 taskkill 命令，跳过此步骤
        if self.is_pe_environment():
            self.log("[*] 检测到 PE 环境，跳过进程结束步骤（系统未运行）")
            return

        processes = [
            "DF5Serv.exe", "DF6Serv.exe", "DF7Serv.exe", "DF8Serv.exe",
            "DFServ.exe", "Dfrfos.exe", "Dfserv.exe", "FrzState2k.exe",
            "Deep Freeze.exe",
        ]
        for proc in processes:
            try:
                self.log(f"[*] 正在结束进程: {proc}")
                subprocess.run(
                    ["taskkill", "/F", "/T", "/IM", proc],
                    capture_output=True,
                    check=False
                )
            except Exception as e:
                self.log(f"[!] 结束进程 {proc} 时出错: {e}")

    def is_pe_environment(self):
        """检测是否在 PE 环境下"""
        pe_indicators = [
            not os.path.exists(r"C:\Windows\System32\sc.exe"),
            os.path.exists(r"X:\Windows\System32\winpeshl.exe"),
            "PE" in os.environ.get("SYSTEMDRIVE", ""),
        ]
        return any(pe_indicators)

    def stop_deepfreeze_services(self):
        """停止冰点还原相关服务"""
        # PE 环境下通常没有 sc 命令，跳过此步骤
        if self.is_pe_environment():
            self.log("[*] 检测到 PE 环境，跳过服务停止步骤（通过注册表删除服务）")
            return

        services = ["Deep Freeze", "DFServ", "DF5Serv", "DF6Serv", "DF7Serv", "DF8Serv"]
        for service in services:
            try:
                self.log(f"[*] 正在停止服务: {service}")
                subprocess.run(["sc", "stop", service], capture_output=True, check=False)
                subprocess.run(["sc", "delete", service], capture_output=True, check=False)
            except Exception as e:
                self.log(f"[!] 停止服务 {service} 时出错: {e}")

    def delete_deepfreeze_files(self, system_drive):
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
                        self.log(f"[*] 正在删除目录: {path}")
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        self.log(f"[*] 正在删除文件: {path}")
                        os.remove(path)
            except Exception as e:
                self.log(f"[!] 删除 {path} 时出错: {e}")

    def remove_registry_entries(self):
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
                self.log(f"[*] 正在删除注册表项: {path}")
                winreg.DeleteKey(hkey, path)
            except FileNotFoundError:
                pass
            except Exception as e:
                self.log(f"[!] 删除注册表项 {path} 时出错: {e}")

    def remove_startup_entries(self):
        """删除启动项"""
        startup_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"PE_SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "Deep Freeze"),
            (winreg.HKEY_LOCAL_MACHINE, r"PE_SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "DFServ"),
        ]
        for hkey, path, value_name in startup_paths:
            try:
                self.log(f"[*] 正在删除启动项: {value_name}")
                key = winreg.OpenKey(hkey, path, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, value_name)
                winreg.CloseKey(key)
            except FileNotFoundError:
                pass
            except Exception as e:
                self.log(f"[!] 删除启动项 {value_name} 时出错: {e}")

    def clean_driver_files(self, system_drive):
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
                    self.log(f"[*] 正在删除驱动: {driver}")
                    os.remove(driver)
            except Exception as e:
                self.log(f"[!] 删除驱动 {driver} 时出错: {e}")

    def unload_registry_hives(self):
        """卸载注册表配置单元"""
        self.log("[*] 正在卸载注册表配置单元...")
        for name in self.loaded_hives:
            try:
                subprocess.run(
                    ["reg", "unload", f"HKLM\\{name}"],
                    capture_output=True,
                    check=False
                )
                self.log(f"[+] 已卸载: HKLM\\{name}")
            except Exception as e:
                self.log(f"[!] 卸载 {name} 时出错: {e}")


def main():
    root = tk.Tk()
    app = DeepFreezeUninstallerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
