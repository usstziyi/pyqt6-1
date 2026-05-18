"""
Unit 1.2: QMainWindow —— 标准桌面应用窗口
学习目标:
  1. 理解 QMainWindow 与 QWidget 的区别
  2. 理解菜单栏 (QMenuBar)、工具栏 (QToolBar)、状态栏 (QStatusBar) 的结构
  3. 学会使用 QAction 创建可复用的动作对象
  4. 理解 addSeparator() 在界面组织中的作用

关键概念:
  QMainWindow 提供了标准桌面应用的窗口框架:
  ┌──────────────────────────────┐
  │  Menu Bar  (菜单栏)          │
  ├──────────────────────────────┤
  │  Tool Bar  (工具栏)          │
  ├──────────────────────────────┤
  │                              │
  │  Central Widget (中心控件)   │
  │                              │
  ├──────────────────────────────┤
  │  Status Bar (状态栏)         │
  └──────────────────────────────┘

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qmainwindow.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QMainWindow 示例")
        self.resize(600, 400)

        self._create_menu_bar()       # 创建菜单栏
        self._create_tool_bar()       # 创建工具栏
        self._create_status_bar()     # 创建状态栏
        self._create_central_widget() # 创建中心控件

    def _create_menu_bar(self):
        # menuBar(): 获取 QMainWindow 自带的菜单栏 (不存在则自动创建)
        menu_bar = self.menuBar()

        # ------ 文件菜单 ------
        file_menu = menu_bar.addMenu("文件(&F)")
        # QAction: 封装一个用户可触发的动作 (菜单项 / 工具栏按钮)
        new_action = QAction("新建(&N)", self)
        # 为 QAction 绑定快捷键 (Ctrl+N)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip("创建一个新文件")
        new_action.triggered.connect(self._on_new_file)
        file_menu.addAction(new_action)

        open_action = QAction("打开(&O)...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("打开一个已有文件")
        # 暂时不连接槽函数，只做演示
        file_menu.addAction(open_action)

        file_menu.addSeparator()  # 添加分隔线

        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("退出应用程序")
        # 连接到 QApplication 的 quit 静态方法
        exit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(exit_action)

        # ------ 帮助菜单 ------
        help_menu = menu_bar.addMenu("帮助(&H)")
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _create_tool_bar(self):
        # addToolBar(name): 创建并添加一个工具栏
        tool_bar = self.addToolBar("主工具栏")
        # 禁止工具栏被拖拽移动
        tool_bar.setMovable(False)

        # 工具栏上的按钮也使用 QAction
        new_action = QAction("新建", self)
        new_action.setStatusTip("新建文件")
        new_action.triggered.connect(self._on_new_file)
        tool_bar.addAction(new_action)

        tool_bar.addSeparator()

        exit_action = QAction("退出", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        tool_bar.addAction(exit_action)

    def _create_status_bar(self):
        # statusBar(): 获取 QMainWindow 自带的状态栏
        status_bar = self.statusBar()
        # 显示一条永久信息
        status_bar.showMessage("就绪")

    def _create_central_widget(self):
        # setCentralWidget(): 设置 QMainWindow 的中心控件
        # 这个控件会占据菜单栏/工具栏/状态栏之间的所有空间
        label = QLabel("欢迎使用 PyQt6 QMainWindow!\n请查看菜单栏和工具栏。")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter) # 设置对齐方式
        # 设置字体稍微大一些
        font = label.font()
        font.setPointSize(16)
        label.setFont(font)
        self.setCentralWidget(label)

    def _on_new_file(self):
        self.statusBar().showMessage("点击了新建菜单", 3000)

    def _on_about(self):
        self.statusBar().showMessage("这是一个 QMainWindow 教学示例", 3000)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
