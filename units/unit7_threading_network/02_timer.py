"""
Unit 7.2: QTimer 与异步调度
学习目标:
  1. 掌握 QTimer 创建定时器: singleShot 和周期性定时器
  2. 理解 QTimer 在事件循环中的工作方式
  3. 学会使用 QTimer 实现倒计时、轮询、动画
  4. 理解 QTimer 精度受事件循环繁忙程度影响

关键概念:
  - QTimer.singleShot(ms, slot): 单次触发，ms 毫秒后执行 slot
  - QTimer.start(ms): 每 ms 毫秒发射 timeout 信号
  - QTimer.stop(): 停止定时器
  - setInterval(ms): 修改间隔
  - timerId(): 获取定时器 ID (用于 killTimer)
  - Python 的 threading.Timer 与 QTimer 的区别:
    QTimer 在事件循环中运行，线程安全地与 UI 交互

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qtimer.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QProgressBar,
    QSpinBox, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QColor


class TimerDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTimer 定时器演示")
        self.resize(500, 500)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # === 倒计时器 ===
        countdown_group = QGroupBox("1. 倒计时器 (周期性 QTimer)")
        countdown_layout = QVBoxLayout(countdown_group)

        ctrl_row = QHBoxLayout()
        ctrl_row.addWidget(QLabel("倒计时 (秒):"))
        self.countdown_spin = QSpinBox()
        self.countdown_spin.setRange(1, 120)
        self.countdown_spin.setValue(30)
        ctrl_row.addWidget(self.countdown_spin)
        countdown_layout.addLayout(ctrl_row)

        self.countdown_label = QLabel("30 秒")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet(
            "font-size: 28px; font-weight: bold; "
            "background-color: #FFF3E0; padding: 15px; border-radius: 8px;"
        )
        countdown_layout.addWidget(self.countdown_label)

        self.countdown_bar = QProgressBar()
        self.countdown_bar.setRange(0, 100)
        self.countdown_bar.setValue(100)
        countdown_layout.addWidget(self.countdown_bar)

        btn_row = QHBoxLayout()
        self.start_cd_btn = QPushButton("开始倒计时")
        self.start_cd_btn.clicked.connect(self._start_countdown)
        btn_row.addWidget(self.start_cd_btn)

        self.stop_cd_btn = QPushButton("停止")
        self.stop_cd_btn.setEnabled(False)
        self.stop_cd_btn.clicked.connect(self._stop_countdown)
        btn_row.addWidget(self.stop_cd_btn)
        countdown_layout.addLayout(btn_row)

        main_layout.addWidget(countdown_group)

        # 创建倒计时器
        self._countdown_timer = QTimer(self)
        self._countdown_timer.timeout.connect(self._on_countdown_tick)
        self._countdown_remaining = 0  # 剩余倒计时秒数
        self._countdown_total = 0      # 倒计时总秒数（用于计算进度条百分比）

        # === 实时时钟 ===
        clock_group = QGroupBox("2. 实时时钟 (每秒更新)")
        clock_layout = QHBoxLayout(clock_group)

        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; font-family: Menlo;"
        )
        clock_layout.addWidget(self.clock_label)

        main_layout.addWidget(clock_group)

        # 创建时钟定时器
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(1000)  # 每 1000ms 触发
        self._update_clock()

        # === QTimer.singleShot 用法 ===
        single_group = QGroupBox("3. QTimer.singleShot 一次性延时")
        single_layout = QVBoxLayout(single_group)

        single_btn = QPushButton("点击后 3 秒弹出提示")
        single_btn.clicked.connect(self._do_singleshot)
        single_layout.addWidget(single_btn)

        self.single_status = QLabel("等待点击...")
        single_layout.addWidget(self.single_status)

        main_layout.addWidget(single_group)

        # === 动画进度条 (QTimer 模拟) ===
        anim_group = QGroupBox("4. 动画进度条 (QTimer 模拟匀速动画)")
        anim_layout = QVBoxLayout(anim_group)

        self.anim_bar = QProgressBar()
        self.anim_bar.setRange(0, 100)
        self.anim_bar.setValue(0)
        self.anim_bar.setStyleSheet(
            "QProgressBar::chunk { background-color: #9C27B0; }"
        )
        anim_layout.addWidget(self.anim_bar)

        anim_btn_row = QHBoxLayout()

        self.anim_start_btn = QPushButton("开始动画")
        self.anim_start_btn.clicked.connect(self._start_animation)
        anim_btn_row.addWidget(self.anim_start_btn)

        self.anim_reset_btn = QPushButton("重置")
        self.anim_reset_btn.clicked.connect(self._reset_animation)
        anim_btn_row.addWidget(self.anim_reset_btn)

        anim_layout.addLayout(anim_btn_row)
        main_layout.addWidget(anim_group)

        # 动画定时器
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._on_anim_tick)
        self._anim_value = 0

        # === 日志 ===
        log_group = QGroupBox("定时器日志")
        log_layout = QVBoxLayout(log_group)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(80)
        log_layout.addWidget(self.log_output)

        main_layout.addWidget(log_group)

        self.setCentralWidget(central)

    def _append_log(self, msg):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{ts}] {msg}")

    # --- 倒计时 ---
    def _start_countdown(self):
        self._countdown_total = self.countdown_spin.value()
        self._countdown_remaining = self._countdown_total
        self._update_countdown_display()
        self._countdown_timer.start(1000)  # 每 1 秒触发
        self.start_cd_btn.setEnabled(False)
        self.stop_cd_btn.setEnabled(True)
        self._append_log(f"倒计时 {self._countdown_total} 秒开始")

    def _stop_countdown(self):
        self._countdown_timer.stop()
        self.start_cd_btn.setEnabled(True)
        self.stop_cd_btn.setEnabled(False)
        self._append_log("倒计时已停止")

    def _on_countdown_tick(self):
        self._countdown_remaining -= 1
        self._update_countdown_display()

        if self._countdown_remaining <= 0:
            self._countdown_timer.stop()
            self.start_cd_btn.setEnabled(True)
            self.stop_cd_btn.setEnabled(False)
            self.countdown_label.setStyleSheet(
                "font-size: 28px; font-weight: bold; "
                "background-color: #C8E6C9; padding: 15px; border-radius: 8px;"
            )
            self.countdown_label.setText("时间到!")
            self._append_log("倒计时结束!")

    def _update_countdown_display(self):
        remaining = self._countdown_remaining
        total = self._countdown_total
        self.countdown_label.setText(f"{remaining} 秒")
        self.countdown_bar.setValue(int(remaining / total * 100))

    # --- 实时时钟 ---
    def _update_clock(self):
        current = QTime.currentTime()
        self.clock_label.setText(current.toString("hh:mm:ss"))

    # --- singleShot ---
    def _do_singleshot(self):
        self.single_status.setText("已触发, 等待 3 秒...")
        self._append_log("设置了 3 秒后的一次性定时器")

        # QTimer.singleShot(ms, callable): ms 毫秒后执行一次
        QTimer.singleShot(3000, self._on_singleshot_done)

    def _on_singleshot_done(self):
        self.single_status.setText("3 秒已到! 你可以再次点击。")
        self._append_log("singleShot 已触发!")

    # --- 动画 ---
    def _start_animation(self):
        self._anim_value = 0
        self.anim_bar.setValue(0)
        self._anim_timer.start(50)  # 每 50ms 更新一次 (约 5 秒完成 100%)
        self.anim_start_btn.setEnabled(False)
        self._append_log("动画开始")

    def _reset_animation(self):
        self._anim_timer.stop()
        self._anim_value = 0
        self.anim_bar.setValue(0)
        self.anim_start_btn.setEnabled(True)
        self._append_log("动画已重置")

    def _on_anim_tick(self):
        self._anim_value += 1
        self.anim_bar.setValue(self._anim_value)
        if self._anim_value >= 100:
            self._anim_timer.stop()
            self.anim_start_btn.setEnabled(True)
            self._append_log("动画完成")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = TimerDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
