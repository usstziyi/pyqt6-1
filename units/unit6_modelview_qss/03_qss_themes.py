"""
Unit 6.3: QSS (Qt Style Sheets) —— 主题与美化
学习目标:
  1. 理解 QSS 语法: 选择器 { 属性: 值; }
  2. 掌握控件级别的 setStyleSheet() 和全局级别 app.setStyleSheet()
  3. 学会伪状态选择器: :hover, :pressed, :checked, :disabled 等
  4. 掌握 QSS 子控件选择器: QComboBox::drop-down 等
  5. 理解级联和继承规则

关键概念:
  - QSS 语法类似 CSS，支持选择器、伪状态、子控件
  - setStyleSheet() 可作用于 QApplication 或单个 QWidget
  - 子控件的 QSS 会继承父控件的样式但可被覆盖
  - Qt 内置主题: Fusion, Windows, macOS 等 (app.setStyle("Fusion"))

API 参考:
  https://doc.qt.io/qt-6/stylesheet-reference.html
  https://doc.qt.io/qt-6/stylesheet-syntax.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QLineEdit, QComboBox,
    QProgressBar, QSlider, QCheckBox, QRadioButton,
    QTabWidget, QTextEdit, QSpinBox
)
from PyQt6.QtCore import Qt


# 定义全局 QSS 主题样式
LIGHT_THEME_QSS = """
/* === 全局样式 === */
QMainWindow {
    background-color: #F5F5F5;
}

QGroupBox {
    border: 1px solid #BDBDBD;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #424242;
}

/* === QPushButton === */
QPushButton {
    background-color: #1976D2;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #1565C0;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #BDBDBD;
    color: #757575;
}

/* === 危险按钮 (通过 objectName 选择) === */
QPushButton#danger_btn {
    background-color: #D32F2F;
}

QPushButton#danger_btn:hover {
    background-color: #C62828;
}

QPushButton#danger_btn:pressed {
    background-color: #B71C1C;
}

/* === 成功按钮 === */
QPushButton#success_btn {
    background-color: #388E3C;
}

QPushButton#success_btn:hover {
    background-color: #2E7D32;
}

QPushButton#success_btn:pressed {
    background-color: #1B5E20;
}

/* === QLineEdit === */
QLineEdit {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    padding: 6px 8px;
    font-size: 13px;
    background-color: white;
}

QLineEdit:focus {
    border-color: #1976D2;
    border-width: 2px;
}

/* === QComboBox === */
QComboBox {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    padding: 6px 8px;
    background-color: white;
    min-width: 100px;
}

QComboBox:hover {
    border-color: #1976D2;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #BDBDBD;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

/* === QSlider === */
QSlider::groove:horizontal {
    height: 6px;
    background: #E0E0E0;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    width: 18px;
    height: 18px;
    margin: -6px 0;
    background: #1976D2;
    border-radius: 9px;
}

QSlider::sub-page:horizontal {
    background: #64B5F6;
    border-radius: 3px;
}

/* === QProgressBar === */
QProgressBar {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    text-align: center;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #43A047;
    border-radius: 3px;
}

/* === QCheckBox === */
QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #757575;
    border-radius: 2px;
}

QCheckBox::indicator:checked {
    background-color: #1976D2;
    border-color: #1976D2;
}

/* === QTabWidget === */
QTabWidget::pane {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    background-color: white;
}

QTabBar::tab {
    background-color: #E0E0E0;
    border: 1px solid #BDBDBD;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom-color: white;
}

QTabBar::tab:hover:!selected {
    background-color: #EEEEEE;
}

/* === QTextEdit === */
QTextEdit {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    padding: 4px;
    background-color: white;
}

/* === QRadioButton === */
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #757575;
}

QRadioButton::indicator:checked {
    background-color: #1976D2;
    border-color: #1976D2;
}
"""


class QSSDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSS 样式表演示")
        self.resize(650, 550)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # --- 主题切换 ---
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("主题:"))

        theme_combo = QComboBox()
        theme_combo.addItems(["Material Light (QSS)", "Fusion (Qt内置)", "默认"])
        # activated(int) 信号: 用户选择某项目
        theme_combo.activated.connect(self._switch_theme)
        theme_layout.addWidget(theme_combo)

        theme_layout.addStretch()

        refresh_btn = QPushButton("重新应用 QSS")
        refresh_btn.clicked.connect(self._apply_qss)
        theme_layout.addWidget(refresh_btn)

        main_layout.addLayout(theme_layout)

        # --- 按钮样式演示 ---
        btn_group = QGroupBox("按钮样式")
        btn_layout = QHBoxLayout(btn_group)

        normal_btn = QPushButton("普通按钮")
        btn_layout.addWidget(normal_btn)

        danger_btn = QPushButton("危险按钮")
        danger_btn.setObjectName("danger_btn")
        btn_layout.addWidget(danger_btn)

        success_btn = QPushButton("成功按钮")
        success_btn.setObjectName("success_btn")
        btn_layout.addWidget(success_btn)

        disabled_btn = QPushButton("禁用按钮")
        disabled_btn.setEnabled(False)
        btn_layout.addWidget(disabled_btn)

        main_layout.addWidget(btn_group)

        # --- 输入控件样式 ---
        input_group = QGroupBox("输入控件样式")
        input_layout = QHBoxLayout(input_group)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText("带 placeholder 的输入框")
        input_layout.addWidget(line_edit)

        combo = QComboBox()
        combo.addItems(["选项 A", "选项 B", "选项 C"])
        combo.setCurrentIndex(0)
        input_layout.addWidget(combo)

        spin = QSpinBox()
        spin.setRange(0, 100)
        spin.setValue(50)
        input_layout.addWidget(spin)

        main_layout.addWidget(input_group)

        # --- 滑块和进度条 ---
        prog_group = QGroupBox("滑块与进度条")
        prog_layout = QVBoxLayout(prog_group)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("音量:"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(75)
        self.slider.valueChanged.connect(
            lambda v: self.progress.setValue(v)
        )
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(QLabel("100"))

        prog_layout.addLayout(slider_layout)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(75)
        prog_layout.addWidget(self.progress)

        main_layout.addWidget(prog_group)

        # --- 复选和单选 ---
        check_group = QGroupBox("复选框与单选按钮")
        check_layout = QHBoxLayout(check_group)

        check1 = QCheckBox("启用通知")
        check1.setChecked(True)
        check_layout.addWidget(check1)

        check2 = QCheckBox("自动更新")
        check_layout.addWidget(check2)

        radio1 = QRadioButton("浅色")
        radio1.setChecked(True)
        check_layout.addWidget(radio1)

        radio2 = QRadioButton("深色")
        check_layout.addWidget(radio2)

        main_layout.addWidget(check_group)

        # --- 标签页 ---
        tab_group = QGroupBox("QTabWidget 样式")
        tab_layout = QVBoxLayout(tab_group)

        tabs = QTabWidget()
        for i in range(1, 5):
            page = QWidget()
            page_layout = QVBoxLayout(page)
            page_layout.addWidget(QLabel(f"标签页 {i} 的内容"))
            page_layout.addStretch()
            tabs.addTab(page, f"标签 {i}")
        tab_layout.addWidget(tabs)

        main_layout.addWidget(tab_group)

        # --- 文本区域 ---
        text_group = QGroupBox("QTextEdit 样式")
        text_layout = QVBoxLayout(text_group)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("这是用于测试样式的文本区域...")
        self.text_edit.setMaximumHeight(80)
        text_layout.addWidget(self.text_edit)

        main_layout.addWidget(text_group)

        self.setCentralWidget(central)

        # 初始应用 QSS
        self._apply_qss()

    def _apply_qss(self):
        # setStyleSheet: 可以作用于 QApplication 全局，也可作用于单个控件
        # 全局应用: app.setStyleSheet(qss)
        # 窗口级: self.setStyleSheet(qss)
        app = QApplication.instance()
        if app:
            app.setStyleSheet(LIGHT_THEME_QSS)

    def _switch_theme(self, index):
        app = QApplication.instance()
        if app is None:
            return

        if index == 0:
            # QSS 自定义主题
            app.setStyleSheet(LIGHT_THEME_QSS)
            app.setStyle("Fusion")
        elif index == 1:
            # Qt 内置 Fusion 主题 (无 QSS)
            app.setStyleSheet("")
            app.setStyle("Fusion")
        else:
            # 系统默认主题
            app.setStyleSheet("")
            app.setStyle("")


def main():
    app = QApplication(sys.argv)
    window = QSSDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
