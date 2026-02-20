# 强力卸载冰点还原精灵 (Deep Freeze Uninstaller)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows/)

> 一键强力卸载冰点还原精灵，支持 PE 环境下操作

## 📋 简介

本工具用于在 **PE 系统** 环境下强力卸载冰点还原（Deep Freeze）软件。由于冰点还原会保护系统文件，常规方式无法卸载，本工具通过直接操作注册表和系统文件实现强制卸载。

**参考**: 本工具参考了 [SYSTEM-RAMOS-ZDY](https://space.bilibili.com/493998035) 的一键斩杀工具原理。

## ⚠️ 重要提示

- **必须在 PE 系统下运行！**
- 操作前会自动备份 SYSTEM 注册表文件
- 请确保你知道自己在做什么
- 建议在操作前备份重要数据

## 🚀 快速开始

### 方法一：使用启动器（推荐）

1. 进入 PE 系统
2. 双击 `launcher.bat`
3. 选择要使用的版本
4. 按提示操作

### 方法二：直接运行

```bash
# 命令行版
python "强力uninstall 冰点还原.py"

# 图形界面版
python "强力uninstall 冰点还原_GUI.py"

# 专业版（推荐）
python "强力uninstall 冰点还原_专业版.py"
```

## 📦 版本说明

| 版本 | 说明 | 适用场景 |
|------|------|----------|
| **命令行版** | 完整功能，命令行操作 | 熟悉命令行的用户 |
| **图形界面版** | 可视化操作，进度显示 | 普通用户 |
| **专业版** ⭐ | 修复驱动过滤器，处理更彻底 | **推荐所有用户** |

### 专业版特性

- ✅ 直接备份 SYSTEM 注册表文件
- ✅ 修复被劫持的存储卷、键盘、鼠标驱动
- ✅ 处理 ControlSet001/002/003
- ✅ 删除 FarDisk/FarSpace 服务
- ✅ 错误自动恢复机制

## 📖 使用步骤

1. **制作 PE 启动盘**
   - 使用微PE、优启通等工具制作

2. **进入 PE 系统**
   - 从 U 盘启动进入 PE

3. **确认系统盘盘符**
   - 打开文件管理器，查看哪个盘包含 Windows 文件夹
   - 注意：PE 下盘符可能变化（如 C 盘变成 D 盘）

4. **运行工具**
   - 运行 `launcher.bat` 或直接运行 Python 脚本
   - 输入系统盘盘符
   - 等待操作完成

5. **重启计算机**
   - 卸载完成后重启进入正常系统

## ⚙️ 技术原理

### 1. 加载注册表
```
reg load HKLM\DF_UNINSTALL X:\Windows\System32\config\SYSTEM
```

### 2. 删除服务
- DeepFrz
- DfDiskLo
- DFFilter
- DFServ
- FarDisk
- FarSpace

### 3. 修复驱动过滤器
- 存储卷: PartMgr, iaStorF
- 键盘: kbdclass
- 鼠标: mouclass

### 4. 删除文件
- C:\Program Files\Faronics
- C:\Windows\System32\drivers\DeepFrz.sys
- 其他相关驱动文件

## 🔄 问题恢复

如果卸载后系统蓝屏：

1. 重新进入 PE 系统
2. 找到备份文件 `X:\SYSTEM.bak`
3. 复制到系统目录：
   ```
   copy X:\SYSTEM.bak X:\Windows\System32\config\SYSTEM
   ```
4. 重启计算机

## 📁 文件清单

```
DeepFreeze-Uninstaller/
├── 启动器.bat                      # 启动器
├── 强力uninstall 冰点还原.py       # 命令行版
├── 强力uninstall 冰点还原_GUI.py   # 图形界面版
├── 强力uninstall 冰点还原_专业版.py # 专业版 ⭐
├── 一键斩杀冰点还原.bat            # 原版BAT
├── README.md                       # 说明文档
└── LICENSE                         # 许可证
```

## 🛡️ 免责声明

本工具仅供学习和研究使用，使用本工具造成的任何后果由使用者自行承担。

- 请在合法授权的情况下使用
- 操作前请备份重要数据
- 作者不对任何数据丢失或系统损坏负责

## 👏 致谢

- [SYSTEM-RAMOS-ZDY](https://space.bilibili.com/493998035) - 提供技术原理和原版工具
- 所有贡献者和测试者

## 📜 许可证

本项目采用 [MIT 许可证](LICENSE) 开源。

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- GitHub Issues
- B站: [SYSTEM-RAMOS-ZDY](https://space.bilibili.com/493998035)

---

**⚠️ 再次提醒：本工具必须在 PE 系统下运行！**
