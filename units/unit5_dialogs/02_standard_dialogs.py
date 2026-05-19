"""
Unit 5.2: QFileDialog, QFontDialog, QColorDialog, QInputDialog
学习目标:
  1. 掌握 QFileDialog 的静态方法快速打开/保存文件
  2. 学会 QFontDialog 获取用户字体选择
  3. 学会 QColorDialog 获取用户颜色选择
  4. 掌握 QInputDialog 获取用户输入的 5 种方法

关键概念:
  - QFileDialog: 文件选择对话框
    getOpenFileName, getOpenFileNames, getSaveFileName, getExistingDirectory
  - QFontDialog: 字体选择对话框
  - QColorDialog: 颜色选择对话框
  - QInputDialog: 通用输入对话框
    getText, getInt, getDouble, getItem, getMultiLineText

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qfiledialog.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qcolordialog.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qinputdialog.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QTextEdit, QFileDialog,
    QFontDialog, QColorDialog, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class StandardDialogsDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("标准对话框演示")
        self.resize(600, 550)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # === QFileDialog ===
        file_group = QGroupBox("QFileDialog 文件对话框")
        file_layout = QHBoxLayout(file_group)

        open_btn = QPushButton("打开文件")
        open_btn.clicked.connect(self._open_file)
        file_layout.addWidget(open_btn)

        save_btn = QPushButton("保存文件")
        save_btn.clicked.connect(self._save_file)
        file_layout.addWidget(save_btn)

        dir_btn = QPushButton("选择目录")
        dir_btn.clicked.connect(self._select_directory)
        file_layout.addWidget(dir_btn)

        file_layout.addStretch()
        main_layout.addWidget(file_group)

        # === QFontDialog ===
        font_group = QGroupBox("QFontDialog 字体对话框")
        font_layout = QHBoxLayout(font_group)

        font_btn = QPushButton("选择字体...")
        font_btn.clicked.connect(self._select_font)
        font_layout.addWidget(font_btn)

        self.font_label = QLabel("示例文字 Preview Text")
        self.font_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.font_label.setStyleSheet(
            "padding: 15px; background-color: #FFF3E0; border-radius: 4px;"
        )
        font_layout.addWidget(self.font_label)
        main_layout.addWidget(font_group)

        # === QColorDialog ===
        color_group = QGroupBox("QColorDialog 颜色对话框")
        color_layout = QHBoxLayout(color_group)

        color_btn = QPushButton("选择颜色...")
        color_btn.clicked.connect(self._select_color)
        color_layout.addWidget(color_btn)

        self.color_preview = QLabel("  ")
        self.color_preview.setStyleSheet(
            "min-width: 80px; min-height: 40px; background-color: #4CAF50;"
            "border: 1px solid #999; border-radius: 4px;"
        )
        color_layout.addWidget(self.color_preview)

        self.color_label = QLabel("#4CAF50")
        color_layout.addWidget(self.color_label)

        color_layout.addStretch()
        main_layout.addWidget(color_group)

        # === QInputDialog ===
        input_group = QGroupBox("QInputDialog 输入对话框")
        input_layout = QHBoxLayout(input_group)

        text_btn = QPushButton("文本输入")
        text_btn.clicked.connect(self._input_text)
        input_layout.addWidget(text_btn)

        int_btn = QPushButton("整数输入")
        int_btn.clicked.connect(self._input_int)
        input_layout.addWidget(int_btn)

        double_btn = QPushButton("浮点输入")
        double_btn.clicked.connect(self._input_double)
        input_layout.addWidget(double_btn)

        item_btn = QPushButton("列表选择")
        item_btn.clicked.connect(self._input_item)
        input_layout.addWidget(item_btn)

        main_layout.addWidget(input_group)

        # === 日志区域 ===
        log_group = QGroupBox("操作日志")
        log_layout = QVBoxLayout(log_group)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(180)
        log_layout.addWidget(self.log_output)

        clear_btn = QPushButton("清空日志")
        clear_btn.clicked.connect(self.log_output.clear)
        log_layout.addWidget(clear_btn)

        main_layout.addWidget(log_group)

        self.setCentralWidget(central)

    def _log(self, message):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{ts}] {message}")

    def _open_file(self):
        # getOpenFileName(parent, caption, dir, filter)
        # filter 格式: "描述 (*.ext1 *.ext2);;描述2 (*.ext3)"
        path, _ = QFileDialog.getOpenFileName(
            self,
            "打开文件",
            "",
            "Python 文件 (*.py);;文本文件 (*.txt);;所有文件 (*)"
        )
        if path:
            self._log(f"打开文件: {path}")

    def _save_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "保存文件",
            "untitled.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        if path:
            self._log(f"保存文件: {path}")

    def _select_directory(self):
        # getExistingDirectory: 选择目录
        directory = QFileDialog.getExistingDirectory(
            self, 
            "选择目录", 
            ""
        )
        if directory:
            self._log(f"选择目录: {directory}")

    def _select_font(self):
        # getFont(parent): 返回 (QFont, ok)
        font, ok = QFontDialog.getFont(self)
        if ok:
            self.font_label.setFont(font)
            self._log(f"设置字体: {font.family()} {font.pointSize()}pt")

    def _select_color(self):
        # getColor(initial, parent, title): 返回 QColor
        color = QColorDialog.getColor(QColor("#4CAF50"), self, "选择颜色")
        if color.isValid():
            # 返回 #000000 格式
            hex_color = color.name()
            self.color_preview.setStyleSheet(
                f"min-width: 80px; min-height: 40px; background-color: {hex_color};"
                "border: 1px solid #999; border-radius: 4px;"
            )
            self.color_label.setText(hex_color)
            self._log(f"选择颜色: {color.value()}")

    def _input_text(self):
        # getText(parent, title, label, echo=Normal, text='', ...)
        text, ok = QInputDialog.getText(
            self, "文本输入", "请输入你的名字:"
        )
        if ok and text:
            self._log(f"输入文本: {text}")

    def _input_int(self):
        # getInt(parent, title, label, value=0, min=-2147483647, max=2147483647, step=1)
        value, ok = QInputDialog.getInt(
            self, "整数输入", "请输入年龄:", 25, 0, 150, 1
        )
        if ok:
            self._log(f"输入整数: {value}")

    def _input_double(self):
        # getDouble(parent, title, label, value=0, min=..., max=..., decimals=1)
        value, ok = QInputDialog.getDouble(
            self, "浮点输入", "请输入价格:", 9.99, 0.0, 9999.99, 2
        )
        if ok:
            self._log(f"输入浮点: {value:.2f}")

    def _input_item(self):
        # getItem(parent, title, label, items, current=0, editable=True)
        items = ["Python", "JavaScript", "Go", "Rust", "C++", "Java"]
        item, ok = QInputDialog.getItem(
            self, "列表选择", "选择编程语言:", items, 0, False
        )
        if ok and item:
            self._log(f"选择项目: {item}")


def main():
    app = QApplication(sys.argv)
    window = StandardDialogsDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
