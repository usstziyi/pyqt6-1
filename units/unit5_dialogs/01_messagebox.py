"""
Unit 5.1: QMessageBox —— 消息弹窗
学习目标:
  1. 掌握 QMessageBox 5 种标准对话框: question, information, warning, critical, about
  2. 理解 StandardButton 枚举: Yes, No, Ok, Cancel, Retry, Abort 等
  3. 学会自定义消息框按钮和详细文本
  4. 理解模态 (modal) 与非模态的区别

关键概念:
  - QMessageBox 静态方法: QMessageBox.information / question / warning / critical
  - 返回 StandardButton 值，用于判断用户点击了什么
  - setDetailedText(text): 设置可展开的详细信息
  - exec(): 以模态方式显示 (阻塞)

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qmessagebox.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QTextEdit, QMessageBox,
    QDialog
)
from PyQt6.QtCore import Qt


class MessageBoxDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMessageBox 消息弹窗演示")
        self.resize(500, 450)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # === 四种标准消息框 ===
        std_group = QGroupBox("标准消息框")
        std_layout = QHBoxLayout(std_group)

        # QMessageBox.information(parent, title, text, buttons, defaultButton)
        info_btn = QPushButton("信息\n(information)")
        info_btn.clicked.connect(
            lambda: QMessageBox.information(
                self, "信息", "这是一个信息提示框。",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Abort
            )
        )
        std_layout.addWidget(info_btn)

        warn_btn = QPushButton("警告\n(warning)")
        warn_btn.clicked.connect(
            lambda: QMessageBox.warning(
                self, "警告", "磁盘空间不足！",
                QMessageBox.StandardButton.Ok
            )
        )
        std_layout.addWidget(warn_btn)

        crit_btn = QPushButton("错误\n(critical)")
        crit_btn.clicked.connect(
            lambda: QMessageBox.critical(
                self, "严重错误", "操作失败，请重试。",
                QMessageBox.StandardButton.Retry
                | QMessageBox.StandardButton.Abort
            )
        )
        std_layout.addWidget(crit_btn)

        about_btn = QPushButton("关于\n(about)")
        about_btn.clicked.connect(
            lambda: QMessageBox.about(
                self, "关于本程序",
                "PyQt6 学习教程 v1.0\n基于 Qt 6 的 Python GUI 框架"
            )
        )
        std_layout.addWidget(about_btn)

        main_layout.addWidget(std_group)

        # === 带选择的确认框 ===
        confirm_group = QGroupBox("确认对话框 QMessageBox.question")
        confirm_layout = QHBoxLayout(confirm_group)

        save_btn = QPushButton("保存确认")
        save_btn.clicked.connect(self._confirm_save)
        confirm_layout.addWidget(save_btn)

        delete_btn = QPushButton("删除确认")
        delete_btn.clicked.connect(self._confirm_delete)
        confirm_layout.addWidget(delete_btn)

        overwrite_btn = QPushButton("覆盖确认")
        overwrite_btn.clicked.connect(self._confirm_overwrite)
        confirm_layout.addWidget(overwrite_btn)

        main_layout.addWidget(confirm_group)

        # === 自定义消息框 ===
        custom_group = QGroupBox("自定义消息框")
        custom_layout = QVBoxLayout(custom_group)

        custom_btn = QPushButton("显示自定义消息框 (含详细信息)")
        custom_btn.clicked.connect(self._show_custom_message)
        custom_layout.addWidget(custom_btn)

        main_layout.addWidget(custom_group)

        # === 响应日志 ===
        log_group = QGroupBox("用户响应日志")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        log_layout.addWidget(self.log_text)
        main_layout.addWidget(log_group)

        self.setCentralWidget(central)

    def _log(self, msg):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{ts}] {msg}")

    def _confirm_save(self):
        # question 返回 StandardButton
        # 按钮用 | 组合: Yes | No
        reply = QMessageBox.question(
            self,
            "保存确认",
            "是否保存当前文档?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Yes,  # 默认按钮
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._log("用户选择了: 保存")
        elif reply == QMessageBox.StandardButton.No:
            self._log("用户选择了: 不保存")
        else:
            self._log("用户选择了: 取消")

    def _confirm_delete(self):
        reply = QMessageBox.question(
            self,
            "删除确认",
            "确定要删除选中的项目吗？\n此操作不可撤销！",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if reply == QMessageBox.StandardButton.Ok:
            self._log("用户确认了删除操作")
        else:
            self._log("用户取消了删除操作")

    def _confirm_overwrite(self):
        # 使用 save/cancel 按钮风格
        reply = QMessageBox.question(
            self,
            "覆盖确认",
            "文件已存在，是否覆盖?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if reply == QMessageBox.StandardButton.Save:
            self._log("用户选择了: 覆盖文件")
        else:
            self._log("用户取消了覆盖操作")

    def _show_custom_message(self):
        # 创建自定义 QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("自定义消息框")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("是否提交本次修改?")
        msg.setInformativeText("提交后将无法撤回，请仔细检查。")
        # setDetailedText: 折叠的详细信息
        msg.setDetailedText(
            "修改列表:\n"
            "  - main.py: 新增 15 行\n"
            "  - utils.py: 修改 8 行\n"
            "  - config.ini: 删除 3 行\n"
        )
        # 自定义按钮 (标准按钮 + 自定义文字)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        # 添加额外按钮
        # ActionRole 表示这是一个"动作类"按钮——点击它会触发某种操作，而不是接受或拒绝对话框。它通常位于按钮组的左侧。
        review_btn = msg.addButton("查看详情(&R)", QMessageBox.ButtonRole.ActionRole)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        reply = msg.exec()

        if reply == QMessageBox.StandardButton.Yes:
            self._log("用户选择了: 提交")
        elif reply == QMessageBox.StandardButton.No:
            self._log("用户选择了: 不提交")
        # clickedButton() 只存在于 QMessageBox 类上， 
        # QWidget 和 QDialog 都没有这个方法。它并非通用接口。
        elif msg.clickedButton() == review_btn:
            self._log("用户选择了: 查看详情")


def main():
    app = QApplication(sys.argv)
    window = MessageBoxDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
