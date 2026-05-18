"""
Unit 2.2: QGridLayout —— 网格布局
学习目标:
  1. 掌握 QGridLayout 的行列概念
  2. 理解 addWidget(widget, row, col, rowSpan, colSpan) 的参数含义
  3. 学会用 rowSpan / colSpan 创建跨行跨列的控件
  4. 理解 setColumnStretch / setRowStretch 控制列/行伸缩比

关键概念:
  - QGridLayout 将空间划分为网格 (行 x 列)
  - rowSpan: 控件占据的行数 (默认 1)
  - colSpan: 控件占据的列数 (默认 1)
  - setColumnStretch(col, factor): 设置第 col 列的伸缩因子

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qgridlayout.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QGridLayout, QPushButton, QLabel, QLineEdit
)
from PyQt6.QtCore import Qt


class GridLayoutDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGridLayout 网格布局演示")
        self.resize(450, 350)

        central = QWidget()
        grid = QGridLayout(central)

        # setSpacing(px): 设置格子之间的间距
        grid.setSpacing(10)

        # -- 注册表单示例 --
        grid.addWidget(QLabel("用户名:"), 0, 0)
        grid.addWidget(QLineEdit(), 0, 1, 1, 2)
        #                row col  rowSpan colSpan
        # 上方的 1, 2 表示 QLineEdit 占据 1 行、2 列

        grid.addWidget(QLabel("密码:"), 1, 0)
        grid.addWidget(QLineEdit(), 1, 1, 1, 2)

        grid.addWidget(QLabel("邮箱:"), 2, 0)
        grid.addWidget(QLineEdit(), 2, 1, 1, 2)

        # -- 计算器按钮布局 --
        grid.addWidget(QLabel("--- 计算器按钮区域 ---"), 3, 0, 1, 3)

        display = QLineEdit("0")
        display.setReadOnly(True)
        display.setAlignment(Qt.AlignmentFlag.AlignRight)
        # 添加显示屏，占据 3 列
        grid.addWidget(display, 4, 0, 1, 3)

        # 数字按钮的文本列表
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+",
        ]

        # 从第 5 行开始放置 4x4 的按钮矩阵
        for i, text in enumerate(buttons):
            row = 5 + i // 4
            col = i % 4
            btn = QPushButton(text)
            grid.addWidget(btn, row, col)

        # 设置列拉伸因子，让第 0、1、2 列均分剩余空间
        for col in range(4):
            grid.setColumnStretch(col, 1)

        self.setCentralWidget(central)


def main():
    app = QApplication(sys.argv)
    window = GridLayoutDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
