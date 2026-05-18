"""
Unit 4.1: QPushButton, QLabel, QLineEdit, QTextEdit —— 基础控件
学习目标:
  1. 掌握 QPushButton 的各种状态 (普通/选中/禁用) 和样式
  2. 理解 QLabel 的富文本支持和对齐方式
  3. 掌握 QLineEdit 的输入掩码和验证
  4. 学会 QTextEdit 的 HTML 和纯文本操作

关键概念:
  - QPushButton: 可点击按钮，支持文本、图标、选中状态
  - QLabel: 用于显示文本或图片，支持富文本 (HTML)
  - QLineEdit: 单行文本输入，支持掩码、验证器、回显模式
  - QTextEdit: 多行富文本编辑器，支持 HTML/Markdown

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qpushbutton.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qlabel.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qlineedit.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qtextedit.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QGroupBox
)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator


class BasicWidgetsDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("基础控件演示")
        self.resize(600, 600)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # === 1. QPushButton 篇 ===
        btn_group = QGroupBox("1. QPushButton 按钮")
        btn_layout = QVBoxLayout(btn_group)

        # 普通按钮
        normal_btn = QPushButton("普通按钮")
        btn_layout.addWidget(normal_btn)

        # 可选中按钮 (Toggle)
        toggle_btn = QPushButton("可选中按钮 (Toggle)")
        # setCheckable(True): 使按钮可以保持按下状态
        toggle_btn.setCheckable(True)
        toggle_btn.toggled.connect(
            lambda checked: toggle_btn.setText(
                f"按钮已: {'选中' if checked else '取消'}"
            )
        )
        btn_layout.addWidget(toggle_btn)

        # 禁用按钮
        disabled_btn = QPushButton("禁用状态按钮")
        disabled_btn.setEnabled(False)
        btn_layout.addWidget(disabled_btn)

        # 带图标的按钮 (使用 Unicode 符号替代)
        icon_btn = QPushButton("★ 收藏")
        icon_btn.clicked.connect(
            lambda: icon_btn.setText(
                "★ 已收藏" if "已" not in icon_btn.text() else "★ 收藏"
            )
        )
        btn_layout.addWidget(icon_btn)

        main_layout.addWidget(btn_group)

        # === 2. QLabel 篇 ===
        label_group = QGroupBox("2. QLabel 标签")
        label_layout = QVBoxLayout(label_group)

        # 基础文本
        label_layout.addWidget(QLabel("这是普通文本标签"))

        # 富文本 (HTML)
        rich_label = QLabel()
        rich_label.setText(
            "<b>粗体</b> <i>斜体</i> <u>下划线</u> "
            "<span style='color: red;'>红色文字</span> "
            "<a href='https://www.python.org'>超链接</a>"
        )
        # setOpenExternalLinks(True): 允许在系统浏览器中打开链接
        rich_label.setOpenExternalLinks(True)
        label_layout.addWidget(rich_label)

        # 使用像素图 (这里用彩色方块模拟)
        color_label = QLabel("  ")
        color_label.setStyleSheet(
            "background-color: #4CAF50; min-width: 60px; min-height: 30px;"
            "border-radius: 4px;"
        )
        color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_layout.addWidget(color_label)

        main_layout.addWidget(label_group)

        # === 3. QLineEdit 篇 ===
        line_group = QGroupBox("3. QLineEdit 单行输入")
        line_layout = QGridLayout(line_group)

        # 密码输入
        line_layout.addWidget(QLabel("密码:"), 0, 0)
        pwd_edit = QLineEdit()
        # setEchoMode: 设置回显模式
        pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        pwd_edit.setPlaceholderText("输入密码")
        line_layout.addWidget(pwd_edit, 0, 1)

        # 输入掩码: 电话号码格式
        line_layout.addWidget(QLabel("电话:"), 1, 0)
        phone_edit = QLineEdit()
        # setInputMask: 设置输入掩码
        # 9: 可选数字, 0: 必填数字, ; 后面是占位符
        phone_edit.setInputMask("(999) 0000-0000;_")
        line_layout.addWidget(phone_edit, 1, 1)

        # 验证器: 只允许数字 (1-100)
        line_layout.addWidget(QLabel("年龄(1-100):"), 2, 0)
        age_edit = QLineEdit()
        age_edit.setPlaceholderText("输入年龄")
        # QRegularExpression: 正则表达式验证器
        regex = QRegularExpression(r"^(100|[1-9]?\d)$")
        validator = QRegularExpressionValidator(regex)
        age_edit.setValidator(validator)
        line_layout.addWidget(age_edit, 2, 1)

        # 带清空按钮
        line_layout.addWidget(QLabel("搜索:"), 3, 0)
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("输入搜索关键词")
        # setClearButtonEnabled: 在右侧显示清空按钮
        search_edit.setClearButtonEnabled(True)
        line_layout.addWidget(search_edit, 3, 1)

        main_layout.addWidget(line_group)

        # === 4. QTextEdit 篇 ===
        text_group = QGroupBox("4. QTextEdit 多行文本")
        text_layout = QVBoxLayout(text_group)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在这里输入多行文本...")
        text_layout.addWidget(self.text_edit)

        btn_row = QHBoxLayout()
        append_btn = QPushButton("添加红色文本")
        append_btn.clicked.connect(self._append_rich_text)
        btn_row.addWidget(append_btn)

        html_btn = QPushButton("获取 HTML")
        html_btn.clicked.connect(self._get_html)
        btn_row.addWidget(html_btn)

        plain_btn = QPushButton("获取纯文本")
        plain_btn.clicked.connect(self._get_plain_text)
        btn_row.addWidget(plain_btn)
        text_layout.addLayout(btn_row)

        main_layout.addWidget(text_group)

        self.setCentralWidget(central)

    def _append_rich_text(self):
        self.text_edit.append(
            '<span style="color: red;">这是一段红色文本，时间戳已记录。</span>'
        )

    def _get_html(self):
        html = self.text_edit.toHtml()
        self.text_edit.append(f"\n--- HTML 源码 ---\n{html[:200]}...")

    def _get_plain_text(self):
        plain = self.text_edit.toPlainText()
        self.text_edit.append(f"\n--- 纯文本 (共 {len(plain)} 字符) ---")


def main():
    app = QApplication(sys.argv)
    window = BasicWidgetsDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
