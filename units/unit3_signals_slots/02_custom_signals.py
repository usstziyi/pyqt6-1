"""
Unit 3.2: 自定义信号 (pyqtSignal)
学习目标:
  1. 掌握 pyqtSignal() 创建自定义信号
  2. 理解信号参数类型声明 (pyqtSignal(int), pyqtSignal(str, int) 等)
  3. 学会 signal.emit() 发射自定义信号
  4. 理解信号在对象间解耦通信中的应用

关键概念:
  - pyqtSignal 必须定义为类属性 (不是实例属性)
  - 信号参数类型在 pyqtSignal 中声明，多参数用逗号分隔
  - emit() 的参数必须与声明类型匹配
  - 典型场景: Worker 发射进度信号 -> UI 更新进度条

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/signals_slots.html#defining-new-signals-with-pyqtsignal
"""
import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject


class TaskWorker(QObject):
    """
    自定义信号的工作组件
    必须在 QObject 子类中定义 pyqtSignal
    """

    # pyqtSignal 是类属性，不是实例属性
    # 声明信号: 无参数
    started = pyqtSignal()
    # 声明信号: 携带 int 参数 (如进度百分比)
    progress = pyqtSignal(int)
    # 声明信号: 携带 str 参数 (如日志消息)
    message = pyqtSignal(str)
    # 声明信号: 无参数
    finished = pyqtSignal()

    def do_work(self):
        self.started.emit()
        self.message.emit("任务开始执行...")

        total_steps = 5
        for i in range(total_steps):
            time.sleep(0.5)
            # pct全称percent
            progress_pct = int((i + 1) / total_steps * 100)
            # 发射信号，传递进度值
            self.progress.emit(progress_pct)
            self.message.emit(f"步骤 {i + 1}/{total_steps} 完成 ({progress_pct}%)")

        self.message.emit("任务全部完成!")
        self.finished.emit()


class CustomSignalDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义信号 pyqtSignal 演示")
        self.resize(500, 400)

        central = QWidget()
        layout = QVBoxLayout(central)

        # 进度条
        layout.addWidget(QLabel("任务进度:"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # 日志输出
        layout.addWidget(QLabel("日志:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        # 设置 self.log_output （一个 QTextEdit 控件）的 最大高度为 150 像素。
        # 无论布局怎么拉伸，这个文本框的高度都不会超过 150px。
        self.log_output.setMaximumHeight(150)
        layout.addWidget(self.log_output)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始任务")
        # 信号的参数比槽多时，PyQt 自动丢弃多余的参数 。这是 PyQt 信号槽机制的兼容性设计
        self.start_btn.clicked.connect(self._start_task)
        btn_layout.addWidget(self.start_btn)

        self.clear_btn = QPushButton("清空日志")
        self.clear_btn.clicked.connect(self.log_output.clear)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)

        # 状态标签
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setCentralWidget(central)

        self._worker = None

    def _start_task(self):
        self.start_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_output.clear()
        self.status_label.setText("运行中...")

        # 创建工作组件并连接信号
        self._worker = TaskWorker()

        # 使用不同的连接方式:
        # 1. 标准 connect
        self._worker.started.connect(self._on_worker_started)
        self._worker.progress.connect(self._on_progress)
        # 2. 直接连接到控件的方法 (参数匹配)
        self._worker.message.connect(self.log_output.append)
        # 3. 连接到 lambda (不带额外处理)
        self._worker.finished.connect(lambda:self._on_worker_finished())

        # 触发任务执行
        self._worker.do_work()

        # 注意: 这里同步调用 do_work() 会阻塞 UI
        # 在实际项目中应使用 QThread (见 Unit 7)
        # 这里为了演示信号机制而简化为同步

    def _on_worker_started(self):
        self.log_output.append(">>> Worker 启动")

    def _on_progress(self, value):
        self.progress_bar.setValue(value)

    def _on_worker_finished(self):
        self.status_label.setText("完成")
        self.start_btn.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = CustomSignalDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
