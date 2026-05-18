"""
Unit 5.3: QDialog 自定义对话框
学习目标:
  1. 掌握 QDialog 的生命周期: 创建、exec()、结果处理
  2. 学会 setModal(), setWindowModality() 控制模态
  3. 理解 QDialog.accept() / QDialog.reject() 关闭对话框的语义
  4. 掌握通过属性或信号从对话框传回数据

关键概念:
  - QDialog: 对话框基类
  - exec(): 模态运行，返回 QDialog.Accepted 或 QDialog.Rejected
  - accept() / reject(): 设置结果码并关闭对话框
  - done(int): 设置自定义结果码并关闭
  - 返回数据: 通过属性、信号或 QDialog.result() 传递

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qdialog.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QLineEdit, QDialog,
    QDialogButtonBox, QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt


class LoginDialog(QDialog):
    """
    自定义登录对话框
    通过属性传递数据回主窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("用户登录")
        self.setFixedSize(320, 200)

        layout = QVBoxLayout(self)

        # 输入表单
        form = QFormLayout()

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("请输入用户名")
        form.addRow("用户名:", self.username_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("请输入密码")
        form.addRow("密码:", self.password_edit)

        layout.addLayout(form)

        # 标准按钮框
        # QDialogButtonBox: 自动处理对话框按钮布局与信号
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # 存储用户输入
        self.username = ""
        self.password = ""

    def _on_accept(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        if not username or not password:
            # 简单验证: 必填
            self.username_edit.setFocus()
            return
        self.username = username
        self.password = password
        self.accept()  # 设置结果为 Accepted 并关闭

    def get_credentials(self):
        return self.username, self.password


class PreferencesDialog(QDialog):
    """
    自定义首选项对话框
    通过信号传回数据
    """

    pass

    def __init__(self, parent=None, current_name="", current_value=0):
        super().__init__(parent)
        self.setWindowTitle("首选项设置")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.name_edit = QLineEdit(current_name)
        form.addRow("应用名称:", self.name_edit)

        from PyQt6.QtWidgets import QSpinBox
        self.value_spin = QSpinBox()
        self.value_spin.setRange(0, 100)
        self.value_spin.setValue(current_value)
        form.addRow("缩放比例 (%):", self.value_spin)

        from PyQt6.QtWidgets import QCheckBox
        self.dark_check = QCheckBox("夜间模式")
        form.addRow("", self.dark_check)

        layout.addLayout(form)

        layout.addStretch()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(
            self._restore_defaults
        )
        layout.addWidget(buttons)

    def _restore_defaults(self):
        self.name_edit.setText("MyApp")
        self.value_spin.setValue(50)
        self.dark_check.setChecked(False)

    def get_preferences(self):
        return {
            "name": self.name_edit.text(),
            "value": self.value_spin.value(),
            "dark_mode": self.dark_check.isChecked(),
        }


class CustomDialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义 QDialog 演示")
        self.resize(500, 400)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # 使用说明
        title = QLabel("自定义对话框示例")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title)

        # 登录按钮
        login_group = QGroupBox("登录对话框 (属性传值)")
        login_layout = QVBoxLayout(login_group)

        login_btn = QPushButton("打开登录对话框")
        login_btn.clicked.connect(self._open_login_dialog)
        login_layout.addWidget(login_btn)

        self.login_status = QLabel("未登录")
        login_layout.addWidget(self.login_status)

        main_layout.addWidget(login_group)

        # 首选项按钮
        pref_group = QGroupBox("首选项对话框 (返回值传递)")
        pref_layout = QVBoxLayout(pref_group)

        pref_btn = QPushButton("打开首选项对话框")
        pref_btn.clicked.connect(self._open_preferences_dialog)
        pref_layout.addWidget(pref_btn)

        self.pref_display = QLabel("当前设置: 暂无")
        pref_layout.addWidget(self.pref_display)

        main_layout.addWidget(pref_group)

        # 日志
        log_group = QGroupBox("操作日志")
        log_layout = QVBoxLayout(log_group)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(100)
        log_layout.addWidget(self.log)

        main_layout.addWidget(log_group)

        self.setCentralWidget(central)

    def _append_log(self, msg):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"[{ts}] {msg}")

    def _open_login_dialog(self):
        dialog = LoginDialog(self)
        # exec(): 以模态方式显示，返回 Accepted 或 Rejected
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, password = dialog.get_credentials()
            self.login_status.setText(f"已登录: {username}")
            self._append_log(f"用户 {username} 登录成功")
        else:
            self.login_status.setText("登录已取消")
            self._append_log("用户取消了登录")

    def _open_preferences_dialog(self):
        # 传入当前值
        current = {"name": "MyApp", "value": 50}
        dialog = PreferencesDialog(self, current["name"], current["value"])
        if dialog.exec() == QDialog.DialogCode.Accepted:
            prefs = dialog.get_preferences()
            dark = "暗色" if prefs["dark_mode"] else "亮色"
            self.pref_display.setText(
                f"应用: {prefs['name']}, 缩放: {prefs['value']}%, 主题: {dark}"
            )
            self._append_log(f"首选项已保存: {prefs}")
        else:
            self._append_log("首选项设置已取消")


def main():
    app = QApplication(sys.argv)
    window = CustomDialogDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
