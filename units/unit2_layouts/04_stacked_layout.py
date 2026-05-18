"""
Unit 2.4: QStackedLayout / QTabWidget —— 多页面切换布局
学习目标:
  1. 理解 QStackedLayout 的栈式管理 —— 同时只显示一个页面
  2. 掌握 addWidget() 添加页面、setCurrentIndex() 切换页面
  3. 学会 QTabWidget 替代手动 QStackedLayout + 按钮的组合

关键概念:
  - QStackedLayout: 页面栈，同一时刻只有一个页面可见
  - QTabWidget: 自带标签页切换，内部使用 QStackedWidget
  - 适用场景: 设置面板、向导流程、多视图切换

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qstackedlayout.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qtabwidget.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QStackedLayout,
    QPushButton, QLabel, QTabWidget
)
from PyQt6.QtCore import Qt


class StackedLayoutDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QStackedLayout 页面切换演示")
        self.resize(500, 350)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # --- 切换按钮 ---
        btn_layout = QHBoxLayout()

        self.btn_page1 = QPushButton("页面 1")
        self.btn_page2 = QPushButton("页面 2")
        self.btn_page3 = QPushButton("页面 3")

        btn_layout.addWidget(self.btn_page1)
        btn_layout.addWidget(self.btn_page2)
        btn_layout.addWidget(self.btn_page3)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        # --- QStackedLayout: 栈式布局 ---
        self.stack = QStackedLayout()

        # 创建 3 个页面
        page1 = QWidget()
        page1.setStyleSheet("background-color: #FFCDD2;")
        label1 = QLabel("页面 1: 个人信息")
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label1.setStyleSheet("font-size: 20px;")
        layout1 = QVBoxLayout(page1)
        layout1.addWidget(label1)

        page2 = QWidget()
        page2.setStyleSheet("background-color: #C8E6C9;")
        label2 = QLabel("页面 2: 设置选项")
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label2.setStyleSheet("font-size: 20px;")
        layout2 = QVBoxLayout(page2)
        layout2.addWidget(label2)

        page3 = QWidget()
        page3.setStyleSheet("background-color: #BBDEFB;")
        label3 = QLabel("页面 3: 关于信息")
        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label3.setStyleSheet("font-size: 20px;")
        layout3 = QVBoxLayout(page3)
        layout3.addWidget(label3)

        # addWidget(): 将页面压入栈
        self.stack.addWidget(page1)
        self.stack.addWidget(page2)
        self.stack.addWidget(page3)

        # 绑定按钮点击事件
        # lambda checked, i=0: 创建闭包捕获索引值
        self.btn_page1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_page2.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_page3.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        main_layout.addLayout(self.stack)
        self.setCentralWidget(central)


class TabWidgetDemo(QMainWindow):
    """
    使用 QTabWidget 替代手动 QStackedLayout
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTabWidget 标签页演示")
        self.resize(500, 350)

        # QTabWidget: 自带标签页的切换容器
        tabs = QTabWidget()

        # 创建标签页 1
        tab1 = QWidget()
        layout1 = QVBoxLayout(tab1)
        layout1.addWidget(QLabel("这是标签页 1 的内容"))
        layout1.addWidget(QPushButton("按钮 A"))
        layout1.addStretch()
        tabs.addTab(tab1, "常规")

        # 创建标签页 2
        tab2 = QWidget()
        layout2 = QVBoxLayout(tab2)
        layout2.addWidget(QLabel("这是标签页 2 的内容"))
        layout2.addWidget(QPushButton("按钮 B"))
        layout2.addStretch()
        tabs.addTab(tab2, "高级")

        # 创建标签页 3
        tab3 = QWidget()
        layout3 = QVBoxLayout(tab3)
        layout3.addWidget(QLabel("这是标签页 3 的内容"))
        layout3.addStretch()
        tabs.addTab(tab3, "关于")

        # 设置当前显示的标签页
        tabs.setCurrentIndex(0)

        self.setCentralWidget(tabs)


def main():
    app = QApplication(sys.argv)

    window1 = StackedLayoutDemo()
    window1.show()

    window2 = TabWidgetDemo()
    window2.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
