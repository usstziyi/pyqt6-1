"""
Unit 2.1: QVBoxLayout 与 QHBoxLayout —— 线形布局
学习目标:
  1. 掌握 QVBoxLayout (垂直布局) 和 QHBoxLayout (水平布局)
  2. 理解 addStretch() 的作用 —— 创建可伸缩的空白空间
  3. 理解 addSpacing() 的作用 —— 创建固定间距
  4. 理解嵌套布局: 在布局中嵌入另一个布局

关键概念:
  - QVBoxLayout: 所有子控件从顶部到底部垂直排列
  - QHBoxLayout: 所有子控件从左到右水平排列
  - addStretch(factor): 添加伸缩因子，factor 越大占据越多剩余空间
  - 布局可以任意嵌套，形成复杂的界面结构

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qvboxlayout.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qhboxlayout.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PyQt6.QtCore import Qt


class BoxLayoutDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QVBoxLayout / QHBoxLayout 演示")
        self.resize(500, 400)

        central = QWidget()
        # 主布局: 垂直布局
        main_layout = QVBoxLayout(central)

        # 顶部标签
        title = QLabel("线形布局嵌套示例")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title)

        # --- 第一组: 水平布局嵌套 ---
        group1_label = QLabel("--- 水平布局 (HBox) ---")
        main_layout.addWidget(group1_label)

        # 创建水平布局作为子布局
        hbox = QHBoxLayout()
        # 添加 4 个按钮到水平布局中
        for i in range(1, 5):
            btn = QPushButton(f"按钮 {i}")
            hbox.addWidget(btn)
        # 将水平布局嵌入到主垂直布局中
        main_layout.addLayout(hbox)

        # --- 第二组: 混合布局 ---
        group2_label = QLabel("--- 混合嵌套布局 ---")
        main_layout.addWidget(group2_label)

        # 创建外层水平布局
        outer_hbox = QHBoxLayout()

        # 左侧垂直布局 (3 个按钮)
        left_vbox = QVBoxLayout()
        left_vbox.addWidget(QLabel("左侧 VBox:"))
        left_vbox.addWidget(QPushButton("A"))
        left_vbox.addWidget(QPushButton("B"))
        left_vbox.addWidget(QPushButton("C"))
        # addStretch(): 在底部添加可伸缩空白，把按钮推到顶部
        left_vbox.addStretch()

        # 右侧垂直布局 (3 个按钮)
        right_vbox = QVBoxLayout()
        right_vbox.addWidget(QLabel("右侧 VBox:"))
        right_vbox.addWidget(QPushButton("X"))
        right_vbox.addWidget(QPushButton("Y"))
        right_vbox.addWidget(QPushButton("Z"))
        right_vbox.addStretch()

        # 将两个垂直布局添加到水平布局中
        outer_hbox.addLayout(left_vbox)
        # addSpacing(px): 添加固定像素间距
        outer_hbox.addSpacing(30)
        outer_hbox.addLayout(right_vbox)

        main_layout.addLayout(outer_hbox)

        # 底部伸缩空间
        main_layout.addStretch()

        self.setCentralWidget(central)


def main():
    app = QApplication(sys.argv)
    window = BoxLayoutDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
