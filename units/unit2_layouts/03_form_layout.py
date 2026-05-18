"""
Unit 2.3: QFormLayout —— 表单布局
学习目标:
  1. 掌握 QFormLayout 快速创建 "标签-输入控件" 对
  2. 理解 addRow(label, widget) 和 addRow(label_text, widget) 的区别
  3. 理解 FieldGrowthPolicy 对标签和输入框的尺寸控制

关键概念:
  - QFormLayout 专门为表单场景设计: 左侧标签 + 右侧输入控件
  - addRow(str, QWidget): 自动创建 QLabel 作为标签文字
  - addRow(QWidget, QWidget): 使用自定义标签控件

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qformlayout.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QFormLayout, QLineEdit, QComboBox,
    QSpinBox, QTextEdit, QPushButton,
    QVBoxLayout, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt


class FormLayoutDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QFormLayout 表单布局演示")
        self.resize(450, 400)

        central = QWidget()
        outer = QVBoxLayout(central)

        title = QLabel("用户信息注册表单")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        outer.addWidget(title)

        # QFormLayout: 专为 "标签 + 输入控件" 对设计
        form = QFormLayout()

        # addRow(str, QWidget): 第一个参数是文本，自动创建 QLabel
        form.addRow("姓名:", QLineEdit())

        # addRow(QWidget, QWidget): 也可传入自定义标签控件
        age_spin = QSpinBox()
        age_spin.setRange(1, 150)
        age_spin.setValue(25)
        form.addRow("年龄:", age_spin)

        # QComboBox: 下拉选择框
        gender_combo = QComboBox()
        gender_combo.addItems(["男", "女", "其他"])
        form.addRow("性别:", gender_combo)

        form.addRow("邮箱:", QLineEdit())
        form.addRow("电话:", QLineEdit())

        # QTextEdit: 多行文本编辑
        form.addRow("简介:", QTextEdit())

        # 设置行间距
        form.setSpacing(12)

        outer.addLayout(form)

        # 按钮行
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        submit_btn = QPushButton("提交注册")
        submit_btn.setStyleSheet(
            "QPushButton { padding: 8px 20px; background-color: #4CAF50; "
            "color: white; border: none; border-radius: 4px; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        btn_layout.addWidget(submit_btn)
        btn_layout.addStretch()
        outer.addLayout(btn_layout)

        self.setCentralWidget(central)


def main():
    app = QApplication(sys.argv)
    window = FormLayoutDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
