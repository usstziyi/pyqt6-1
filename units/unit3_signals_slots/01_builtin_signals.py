"""
Unit 3.1: 内置信号与槽的连接
学习目标:
  1. 理解信号 (Signal) 与槽 (Slot) 是 PyQt 的核心通信机制
  2. 掌握 signal.connect(slot) 的标准连接方式
  3. 学会 signal.disconnect(slot) 断开连接
  4. 理解信号可以连接多个槽函数，一个槽可以接收多个信号

关键概念:
  - 信号: 当特定事件发生时被发射 (emit)，如按钮点击、文本变化
  - 槽: 接收信号并执行响应的可调用对象 (函数/方法)
  - 连接: signal.connect(slot) 把信号和槽绑定在一起
  - 信号的参数类型必须与槽的参数类型匹配

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/signals_slots.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSlider,
    QProgressBar
)
from PyQt6.QtCore import Qt


class BuiltinSignalsDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("内置信号与槽演示")
        self.resize(500, 450)

        central = QWidget()
        layout = QVBoxLayout(central)

        # === 示例 1: 按钮 clicked 信号 ===
        layout.addWidget(QLabel("1. QPushButton.clicked 信号:"))

        self.btn = QPushButton("点击我")
        label_btn = QLabel("按钮未被点击")

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn)
        btn_row.addWidget(label_btn)
        layout.addLayout(btn_row)

        # clicked 信号不传参，连接到自定义槽
        self.btn.clicked.connect(lambda: label_btn.setText("按钮被点击了!"))

        # === 示例 2: QLineEdit.textChanged 信号 ===
        layout.addWidget(QLabel("2. QLineEdit.textChanged(str) 信号:"))

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("在这里输入文字...")
        self.text_label = QLabel("你输入了: ")

        edit_row = QHBoxLayout()
        edit_row.addWidget(self.line_edit)
        edit_row.addWidget(self.text_label)
        layout.addLayout(edit_row)

        # textChanged(str) 信号携带当前文本，传给槽函数
        self.line_edit.textChanged.connect(self._on_text_changed)

        # === 示例 3: QSlider.valueChanged 信号 ===
        layout.addWidget(QLabel("3. QSlider.valueChanged(int) 信号:"))

        # QSlider: 滑块控件
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider_label = QLabel("当前值: 50")

        layout.addWidget(self.slider)
        layout.addWidget(self.slider_label)

        # valueChanged(int) 信号带整数值
        self.slider.valueChanged.connect(self._on_slider_changed)

        # === 示例 4: 一个信号连接多个槽 ===
        layout.addWidget(QLabel("4. 一个信号连接多个槽 (多个观察者):"))

        multi_btn = QPushButton("触发多个响应")
        self.multi_label1 = QLabel("观察者 1: 等待...")
        self.multi_label2 = QLabel("观察者 2: 等待...")
        self.multi_label3 = QLabel("观察者 3: 等待...")

        layout.addWidget(multi_btn)
        layout.addWidget(self.multi_label1)
        layout.addWidget(self.multi_label2)
        layout.addWidget(self.multi_label3)

        # 同一个信号可以连接多个槽，它们按连接顺序依次执行
        multi_btn.clicked.connect(lambda: self.multi_label1.setText("观察者 1: 已触发!"))
        multi_btn.clicked.connect(lambda: self.multi_label2.setText("观察者 2: 已触发!"))
        multi_btn.clicked.connect(lambda: self.multi_label3.setText("观察者 3: 已触发!"))

        layout.addStretch()
        self.setCentralWidget(central)

    def _on_text_changed(self, text):
        self.text_label.setText(f"你输入了: {text}")

    def _on_slider_changed(self, value):
        self.slider_label.setText(f"当前值: {value}")


def main():
    app = QApplication(sys.argv)
    window = BuiltinSignalsDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
