"""
Unit 4.2: QComboBox, QSpinBox, QSlider, QCheckBox, QRadioButton
学习目标:
  1. 掌握 QComboBox 的可编辑模式与数据角色
  2. 理解 QSpinBox / QDoubleSpinBox 的范围、步长和前缀/后缀
  3. 学会 QSlider 的方向、刻度线和步长控制
  4. 掌握 QCheckBox 三态模式和 QRadioButton 互斥分组
  5. 使用 QButtonGroup 管理互斥单选按钮

关键概念:
  - QComboBox: 下拉选择或可编辑组合框
  - QSpinBox: 整数微调框, QDoubleSpinBox 浮点数微调框
  - QSlider: 滑块控件，可水平或垂直
  - QCheckBox: 复选框，支持三态 (未选/选中/部分选中)
  - QRadioButton: 单选按钮，同组内互斥

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qcombobox.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qspinbox.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QComboBox, QSpinBox, QDoubleSpinBox,
    QSlider, QCheckBox, QRadioButton, QButtonGroup,
    QLabel, QPushButton
)
from PyQt6.QtCore import Qt


class SelectionWidgetsDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("选择类控件演示")
        self.resize(500, 600)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # === QComboBox ===
        combo_group = QGroupBox("QComboBox 下拉框")
        combo_layout = QVBoxLayout(combo_group)

        # 基础下拉框
        normal_combo = QComboBox()
        normal_combo.addItems(["Python", "JavaScript", "Go", "Rust", "C++"])
        normal_combo.setCurrentIndex(0)
        normal_combo.currentTextChanged.connect(
            lambda t: self._update_status(f"选择了: {t}")
        )
        combo_layout.addWidget(QLabel("编程语言:"))
        combo_layout.addWidget(normal_combo)

        # 可编辑下拉框
        editable_combo = QComboBox()
        # setEditable(True): 允许用户直接输入
        editable_combo.setEditable(True)
        editable_combo.addItems(["北京", "上海", "广州", "深圳"])
        editable_combo.setCurrentText("请输入或选择城市")
        editable_combo.currentTextChanged.connect(
            lambda t: self._update_status(f"城市: {t}")
        )
        combo_layout.addWidget(QLabel("城市 (可编辑):"))
        combo_layout.addWidget(editable_combo)

        # 带用户数据的下拉框
        data_combo = QComboBox()
        # addItem(text, userData): 存储隐藏的用户数据
        data_combo.addItem("低优先级", 0)
        data_combo.addItem("中优先级", 1)
        data_combo.addItem("高优先级", 2)
        data_combo.currentIndexChanged.connect(
            lambda i: self._update_status(
                f"优先级: {data_combo.currentText()} (值={data_combo.currentData()})"
            )
        )
        combo_layout.addWidget(QLabel("优先级 (带数据):"))
        combo_layout.addWidget(data_combo)

        main_layout.addWidget(combo_group)

        # === QSpinBox / QDoubleSpinBox ===
        spin_group = QGroupBox("QSpinBox / QDoubleSpinBox 微调框")
        spin_layout = QFormLayout(spin_group)

        self.int_spin = QSpinBox()
        self.int_spin.setRange(0, 100)
        self.int_spin.setValue(25)
        # setSingleStep: 每次点击箭头的增减量
        self.int_spin.setSingleStep(5)
        # setPrefix: 设置前缀文字
        self.int_spin.setPrefix("年龄: ")
        self.int_spin.setSuffix(" 岁")
        self.int_spin.valueChanged.connect(
            lambda v: self._update_status(f"年龄设为: {v}")
        )
        spin_layout.addRow(QLabel("整数微调:"), self.int_spin)

        self.double_spin = QDoubleSpinBox()
        self.double_spin.setRange(0.0, 10.0)
        self.double_spin.setValue(3.14)
        self.double_spin.setSingleStep(0.01)
        # setDecimals: 小数位数
        self.double_spin.setDecimals(2)
        self.double_spin.setPrefix("数值: ")
        self.double_spin.valueChanged.connect(
            lambda v: self._update_status(f"浮点设为: {v:.2f}")
        )
        spin_layout.addRow(QLabel("浮点微调:"), self.double_spin)

        main_layout.addWidget(spin_group)

        # === QSlider ===
        slider_group = QGroupBox("QSlider 滑块")
        slider_layout = QVBoxLayout(slider_group)

        slider_row = QHBoxLayout()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        # setTickPosition: 显示刻度标记
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        # setTickInterval: 刻度线间隔
        self.slider.setTickInterval(10)
        slider_row.addWidget(QLabel("0"))
        slider_row.addWidget(self.slider)
        slider_row.addWidget(QLabel("100"))
        slider_layout.addLayout(slider_row)

        self.slider_value_label = QLabel("当前值: 50")
        self.slider.valueChanged.connect(
            lambda v: self.slider_value_label.setText(f"当前值: {v}")
        )
        slider_layout.addWidget(self.slider_value_label)

        main_layout.addWidget(slider_group)

        # === QCheckBox ===
        check_group = QGroupBox("QCheckBox 复选框")
        check_layout = QVBoxLayout(check_group)

        self.check1 = QCheckBox("功能 A")
        self.check1.stateChanged.connect(
            lambda s: self._update_status(
                f"A: {'启用' if s == Qt.CheckState.Checked.value else '禁用'}"
            )
        )
        check_layout.addWidget(self.check1)

        self.check2 = QCheckBox("功能 B")
        self.check2.setChecked(True)
        check_layout.addWidget(self.check2)

        # 三态复选框
        self.tristate_check = QCheckBox("三态复选 (部分选中)")
        # setTristate(True): 启用第三态 (部分选中，常用于"全选/部分选")
        self.tristate_check.setTristate(True)
        self.tristate_check.setCheckState(Qt.CheckState.PartiallyChecked)
        self.tristate_check.stateChanged.connect(
            lambda s: self._update_status(f"三态: {s}")
        )
        check_layout.addWidget(self.tristate_check)

        main_layout.addWidget(check_group)

        # === QRadioButton + QButtonGroup ===
        radio_group = QGroupBox("QRadioButton 单选按钮 + QButtonGroup")
        radio_layout = QVBoxLayout(radio_group)

        # QButtonGroup: 将多个单选按钮归为一组，组内互斥
        self.button_group = QButtonGroup(self)

        options = ["选项 1: 方案 A", "选项 2: 方案 B", "选项 3: 方案 C"]
        for i, text in enumerate(options):
            radio = QRadioButton(text)
            if i == 0:
                radio.setChecked(True)
            self.button_group.addButton(radio, i)
            radio_layout.addWidget(radio)

        # idClicked(int): 发射被点击按钮的 ID
        self.button_group.idClicked.connect(
            lambda i: self._update_status(f"选中选项 {i+1}")
        )

        main_layout.addWidget(radio_group)

        # 状态栏
        self.status_label = QLabel("选择一个控件试试")
        self.status_label.setStyleSheet(
            "background-color: #E3F2FD; padding: 10px; border-radius: 4px;"
        )
        main_layout.addWidget(self.status_label)

        self.setCentralWidget(central)

    def _update_status(self, message):
        self.status_label.setText(message)


def main():
    app = QApplication(sys.argv)
    window = SelectionWidgetsDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
