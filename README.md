# PyQt6 学习教程 (Learn PyQt6)

基于 PyQt6 官方文档和 GitHub 社区实践的系统学习教程，知识循序渐进，代码注释详尽，最终通过实战项目完整演练。

## 学习路线图

```
Unit 1: PyQt6 基础与窗口
  │  01_hello_window.py        -- 第一个窗口, QApplication, 事件循环
  │  02_qmainwindow.py         -- QMainWindow, 菜单栏/工具栏/状态栏
  │  03_window_properties.py   -- 窗口居中, 置顶, 透明度, 尺寸约束
  │
Unit 2: 布局管理
  │  01_vbox_hbox.py           -- QVBoxLayout, QHBoxLayout, 嵌套布局
  │  02_grid_layout.py         -- QGridLayout, 行列跨度
  │  03_form_layout.py         -- QFormLayout, 标签-控件对
  │  04_stacked_layout.py      -- QStackedLayout, QTabWidget 页面切换
  │
Unit 3: 信号与槽机制
  │  01_builtin_signals.py     -- 内置信号连接, 多槽连接同一信号
  │  02_custom_signals.py      -- pyqtSignal 自定义信号, emit 发射
  │  03_event_handler.py       -- 事件重写, eventFilter, closeEvent
  │
Unit 4: 常用控件深入
  │  01_basic_widgets.py       -- QPushButton, QLabel, QLineEdit, QTextEdit
  │  02_selection_widgets.py   -- QComboBox, QSpinBox, QSlider, QCheckBox, QRadioButton
  │  03_data_widgets.py        -- QListWidget, QTreeWidget, QTableWidget
  │
Unit 5: 对话框与消息框
  │  01_messagebox.py          -- QMessageBox 标准/确认/自定义对话框
  │  02_standard_dialogs.py    -- QFileDialog, QFontDialog, QColorDialog, QInputDialog
  │  03_custom_dialog.py       -- 自定义 QDialog, 数据传递, exec()
  │
Unit 6: Model/View 架构与 QSS 样式
  │  01_modelview.py           -- QTableView + QStandardItemModel + QSortFilterProxyModel
  │  02_custom_model.py        -- QAbstractTableModel 自定义模型
  │  03_qss_themes.py          -- QSS 语法, 伪状态, 子控件, 主题切换
  │
Unit 7: 多线程与网络
  │  01_threading.py           -- QThread + Worker 模式, moveToThread
  │  02_timer.py               -- QTimer, 倒计时, 实时时钟, singleShot, 动画
  │  03_network.py             -- QNetworkAccessManager, GET/POST, JSON 解析
  │
Unit 8: 实战项目 —— TaskFlow 任务管理
      main.py                  -- 完整桌面应用, 集成所有 Unit 知识点
```

## 环境依赖

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | >= 3.9 | PyQt6 要求 Python 3.9+ |
| PyQt6 | >= 6.5 | GUI 框架核心库 |
| PyQt6-Qt6 | (自动安装) | Qt 6 的 Python 绑定 |
| PyQt6-sip | (自动安装) | Python/C++ 绑定工具 |

### 安装

```bash
# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate   # Windows

# 安装 PyQt6
pip install PyQt6>=6.5
```

### 验证安装

```bash
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 installed successfully')"
```

## 快速开始

每个 Unit 的 `.py` 文件可以独立运行。建议按 Unit 1 → Unit 8 的顺序学习:

```bash
# Unit 1: 第一个窗口
python unit1_basics/01_hello_window.py

# Unit 2: 布局管理
python unit2_layouts/01_vbox_hbox.py

# ...

# Unit 8: 实战项目
python unit8_project/main.py
```

## 参考资源

- [PyQt6 官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Qt 6 官方文档](https://doc.qt.io/qt-6/)
- [ZetCode PyQt6 教程](http://zetcode.com/pyqt6/)
- [PyQt6-Tutorial-Examples (GitHub)](https://github.com/janbodnar/PyQt6-Tutorial-Examples)
- [Qt Style Sheets Reference](https://doc.qt.io/qt-6/stylesheet-reference.html)
- [Model/View Programming](https://doc.qt.io/qt-6/model-view-programming.html)
