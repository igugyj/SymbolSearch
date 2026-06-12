# SymbolSearch

Unicode 符号搜索与复制工具。快速查找并复制特殊符号、希腊字母、数学符号、单位等。

## 功能

- 搜索 755+ 个符号，覆盖 16 个分类
- 实时文本搜索（支持中文/英文，多词取交集）
- 分类筛选（箭头、希腊字母、数学、单位、货币等）
- 双击符号自动复制到剪贴板
- 系统托盘（关闭窗口缩至托盘，双击托盘显示/隐藏）
- 单实例锁，防止重复启动
- 除 PySide6 外无额外依赖

## 符号分类

| 分类 | 数量 |
|------|------|
| 箭头 | 65 |
| 希腊字母 | 59 |
| 数学符号 | 103 |
| 常用单位 | 58 |
| 货币符号 | 37 |
| 标点符号 | 48 |
| 特殊符号 | 74 |
| 几何形状 | 62 |
| 罗马数字 | 28 |
| 分数 | 21 |
| 星座符号 | 12 |
| 音乐符号 | 17 |
| 技术符号 | 40 |
| 类字母符号 | 50 |
| 方块图素 | 43 |
| 化学物理 | 38 |

## 快速开始

```bash
# uv（推荐）
cd SymbolSearch
uv sync
uv run main.py

# 或 pip
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 使用说明

1. 在搜索框输入关键词，实时过滤符号（支持中文和英文）
2. 点击分类标签缩小范围
3. 双击任意符号，自动复制到剪贴板
4. 关闭窗口缩至系统托盘（右键托盘可退出）
5. 双击托盘图标显示/隐藏窗口

搜索示例：

| 输入 | 结果 |
|------|------|
| `箭头` | 所有箭头符号 |
| `右箭头` | `→` |
| `阿尔法` | `α` |
| `温度` | `℃` `℉` |

## 数据格式

符号存储在 `data/symbols.json`：

```json
{
  "箭头": {
    "→": ["右箭头", "向右箭头", "right arrow"],
    ...
  },
  ...
}
```

## 项目结构

```
SymbolSearch/
  main.py              入口
  pyproject.toml       项目元数据和依赖
  uv.lock              锁定依赖版本
  data/
    symbols.json       符号数据库（755 条）
  src/
    app.py             应用初始化
    lock.py            单实例锁
    main_window.py     主窗口布局
    search_panel.py    搜索栏和分类标签
    symbol_data.py     数据加载和过滤
    symbol_list.py     虚拟列表（懒渲染）
    tray.py            系统托盘
     resources.py       SVG 图标和样式
```

## 许可声明

SymbolSearch 使用 MIT 协议，详情见 [LICENSE](LICENSE)。

本程序使用了 PySide6（LGPL v3 协议）。您可以在此获取 PySide6 源代码：
<https://github.com/pyside/pyside6>

根据 LGPL v3 要求，您可以：

- 通过解包本程序替换 PySide6 相关 `.pyd` 文件
- 在 <https://www.gnu.org/licenses/lgpl-3.0.txt> 查阅完整 LGPL v3 协议文本
