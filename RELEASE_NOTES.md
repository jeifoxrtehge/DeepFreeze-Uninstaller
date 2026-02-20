# Release Notes

## v1.0.0 (2024-XX-XX)

### 🎉 首次发布

强力卸载冰点还原精灵工具集首次发布！

### ✨ 功能特性

- **命令行版** - 完整的命令行操作界面
- **图形界面版** - 可视化操作，适合普通用户
- **专业版** ⭐ - 整合 SYSTEM-RAMOS-ZDY 技术，修复驱动过滤器
- **原版BAT** - SYSTEM-RAMOS-ZDY 的原版工具

### 🔧 技术特点

- 支持 PE 环境下操作
- 自动检测 PE 环境并适配
- 直接备份 SYSTEM 注册表文件
- 修复被劫持的存储卷、键盘、鼠标驱动
- 处理 ControlSet001/002/003
- 错误自动恢复机制

### 📦 文件清单

```
DeepFreeze-Uninstaller-v1.0.0/
├── DeepFreeze_Uninstaller_CLI.exe      # 命令行版
├── DeepFreeze_Uninstaller_GUI.exe      # 图形界面版
├── DeepFreeze_Uninstaller_Pro.exe      # 专业版 ⭐
├── 启动器.bat                           # 启动菜单
├── 强力uninstall 冰点还原.py            # 源代码
├── 强力uninstall 冰点还原_GUI.py        # 源代码
├── 强力uninstall 冰点还原_专业版.py      # 源代码
├── README.md                            # 说明文档
└── LICENSE                              # 许可证
```

### 🚀 使用方法

1. 进入 PE 系统
2. 运行 `启动器.bat` 或直接运行 exe
3. 输入系统盘盘符（PE 下可能不是 C 盘）
4. 按提示操作，等待完成
5. 重启计算机

### ⚠️ 注意事项

- **必须在 PE 系统下运行**
- 操作前会自动备份 SYSTEM 文件
- 推荐优先使用专业版

### 🔄 恢复方法

如果卸载后系统蓝屏：
1. 重新进入 PE
2. 找到备份文件 `X:\SYSTEM.bak`
3. 复制到 `X:\Windows\System32\config\SYSTEM`
4. 重启计算机

### 👏 致谢

- [SYSTEM-RAMOS-ZDY](https://space.bilibili.com/493998035) - 提供技术原理和原版工具

### 📜 许可证

MIT License
