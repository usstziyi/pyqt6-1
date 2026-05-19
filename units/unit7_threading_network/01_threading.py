"""
Unit 7.1: QThread 与 Worker 模式 —— 多线程编程
学习目标:
  1. 理解为什么需要在子线程执行耗时任务 —— 防止 UI 冻结
  2. 掌握 QObject.moveToThread() 的 Worker 模式
  3. 学会 QThread 子类化方式 (适用于简单场景)
  4. 理解线程间信号通信是线程安全的
  5. 掌握线程的 start(), quit(), wait(), finished 信号

关键概念:
  - GUI 线程 (主线程): 处理 UI 事件，不能阻塞
  - Worker 线程: 执行耗时任务，通过信号与主线程通信
  - 推荐模式: QObject + moveToThread (而非继承 QThread)
  - moveToThread 后，对象的所有槽函数在目标线程中执行
  - finished 信号: 线程执行完毕后发射

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qthread.html
"""
import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QProgressBar, QTextEdit,
    QStyle
)
from PyQt6.QtCore import (
    Qt, QThread, QObject, pyqtSignal
)


class HeavyTaskWorker(QObject):
    """
    Worker 对象: 将在子线程中执行耗时任务
    所有耗时操作都在这个对象的方法中
    """

    # 自定义信号, 用于线程间通信
    started = pyqtSignal()
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run_computation(self, complexity=10):
        """
        模拟耗时计算任务
        """
        self.started.emit()
        self.log.emit(f"开始计算任务 (复杂度={complexity})...")

        total = 0
        for i in range(complexity):
            # 模拟耗时操作
            time.sleep(0.3)
            total += (i + 1) ** 2
            progress_pct = int((i + 1) / complexity * 100)
            self.progress.emit(progress_pct)
            self.log.emit(f"步骤 {i + 1}/{complexity}: 当前累计 = {total}")

        self.log.emit(f"计算完成! 总计 = {total}")
        self.finished.emit()  # worker发出finished信号

    def run_file_processing(self, file_count=5):
        """
        模拟文件处理任务
        """
        self.started.emit()
        self.log.emit(f"开始处理 {file_count} 个文件...")

        for i in range(1, file_count + 1):
            time.sleep(0.5)
            self.progress.emit(int(i / file_count * 100))
            self.log.emit(f"处理文件 {i}/{file_count}...")

        self.log.emit("所有文件处理完成!")
        self.finished.emit()

    def run_data_fetch(self):
        """
        模拟网络数据获取任务
        """
        self.started.emit()
        self.log.emit("开始获取数据...")

        for i in range(1, 6):
            time.sleep(0.4)
            self.progress.emit(i * 20)
            self.log.emit(f"获取数据块 {i}/5...")

        self.log.emit("数据获取完成!")
        self.finished.emit()


class ThreadDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QThread + Worker 多线程演示")
        self.resize(550, 500)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # --- 任务控制区 ---
        task_group = QGroupBox("耗时任务 (子线程执行)")
        task_layout = QVBoxLayout(task_group)

        btn_layout = QHBoxLayout()

        self.compute_btn = QPushButton("计算任务")
        self.compute_btn.clicked.connect(lambda: self._start_task("compute"))
        btn_layout.addWidget(self.compute_btn)

        self.file_btn = QPushButton("文件处理")
        self.file_btn.clicked.connect(lambda: self._start_task("file"))
        btn_layout.addWidget(self.file_btn)

        self.fetch_btn = QPushButton("数据获取")
        self.fetch_btn.clicked.connect(lambda: self._start_task("fetch"))
        btn_layout.addWidget(self.fetch_btn)

        self.cancel_btn = QPushButton("取消任务")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._cancel_task)
        btn_layout.addWidget(self.cancel_btn)

        task_layout.addLayout(btn_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        task_layout.addWidget(self.progress_bar)

        main_layout.addWidget(task_group)

        # --- UI 响应测试区 ---
        ui_group = QGroupBox("UI 响应测试 (证明 UI 不阻塞)")
        ui_layout = QHBoxLayout(ui_group)

        self.ui_test_btn = QPushButton("点击我测试 UI 是否响应")
        self.ui_test_count = 0
        self.ui_test_btn.clicked.connect(self._on_ui_test)
        ui_layout.addWidget(self.ui_test_btn)

        self.counter_label = QLabel("点击次数: 0")
        ui_layout.addWidget(self.counter_label)

        main_layout.addWidget(ui_group)

        # --- 日志区 ---
        log_group = QGroupBox("任务日志")
        log_layout = QVBoxLayout(log_group)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)

        clear_btn = QPushButton("清空日志")
        clear_btn.clicked.connect(self.log_output.clear)
        log_layout.addWidget(clear_btn)

        main_layout.addWidget(log_group)

        self.setCentralWidget(central)

        # 线程和 Worker 管理
        self._thread = None
        self._worker = None

    def _append_log(self, msg):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{ts}] {msg}")



    """
        ----------标准流程----------
        self.thread = QThread()
        self.worker = Worker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run) # 跨线程信号-槽

        self.worker.finished.connect(self.worker.deleteLater) # 告诉子线程事件循环来回收worker
        self.worker.finished.connect(self.thread.quit)        # 告诉子线程事件循环关机

        self.thread.finished.connect(self.thread.deleteLater) # 告诉主线程事件循环来回收thread

        self.thread.start()
    """
    def _start_task(self, task_type):
        # 禁用按钮防止重复启动
        self._set_buttons_enabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setValue(0)

        # 1. 创建 QThread (子线程)
        self._thread = QThread() # 无parent

        # 2. 创建 Worker (无 parent, 稍后 moveToThread)
        self._worker = HeavyTaskWorker() # 无parent

        # 3. 将 Worker 移动到子线程
        # moveToThread 后, Worker 的所有槽函数在子线程中执行
        # Worker 以孤儿身份创建 → 搬运到子线程 → 再通过 deleteLater 信号链自行清理，全程不依赖 Qt 对象树。
        # thread affinity 对象属于哪个线程 决定槽函数在哪个线程执行、信号队列如何调度。
        # Worker 虽然运行在子线程的事件循环中，但它仍然是孤儿对象，
        # 所以最终依靠 worker.finished → worker.deleteLater() 这条信号链来自我清理。
        self._worker.moveToThread(self._thread)

        # 4. 连接信号与槽 (跨线程信号是线程安全的)
        self._worker.started.connect(lambda: self._append_log("任务已启动"))
        self._worker.progress.connect(self.progress_bar.setValue)
        self._worker.log.connect(self._append_log)
        self._worker.finished.connect(self._on_task_finished)

        # 5. 线程启动后自动调用 Worker 的方法
        if task_type == "compute":
            self._thread.started.connect(self._worker.run_computation)
        elif task_type == "file":
            self._thread.started.connect(self._worker.run_file_processing)
        elif task_type == "fetch":
            self._thread.started.connect(self._worker.run_data_fetch)


        """
        worker.finished 发射 (子线程中)

        deleteLater()          quit()
            │                     │
            ▼                     ▼
        向事件循环投递          告诉事件循环
        DeferredDelete 事件      "处理完就退出"
            │                     │
            └──────┬──────────────┘
                   ▼
            事件循环收尾时：
            先清空删除队列 (worker 析构)
            再 exec() 返回
            然后发送thread.finished
        """
        # 6. Worker 完成后退出线程
        self._worker.finished.connect(self._thread.quit)        # 告诉子线程的事件循环："处理完当前事件后就停止"
        self._worker.finished.connect(self._worker.deleteLater) # 由子线程事件循环回收
        # 告诉主线程：子线程事件循环已经关闭，开来回收子线程资源
        self._thread.finished.connect(self._thread.deleteLater) # 由主线程事件循环回收

        # 7. 启动线程
        self._thread.start()

    def _on_task_finished(self):
        self._append_log(">>> 所有任务完成!")
        self._set_buttons_enabled(True)
        self.cancel_btn.setEnabled(False)

    def _cancel_task(self):
        if self._thread and self._thread.isRunning():
            # quit() + wait(): 优雅退出线程
            # worker 里的 for 循环每一轮之间，不会自动把控制权还给 QThread.exec() 事件循环
            # quit() 不会停止你的 worker 函数
            # 只有等for循环结束，exec才能得到cpu
            self._thread.quit() 
            self._thread.wait()
            # 取消后立即更新 UI（按钮状态、进度条），此时如果子线程还在收尾，
            # 可能会同时修改共享状态，造成竞态条件。
            self._append_log("任务已取消")
            self._set_buttons_enabled(True)
            self.cancel_btn.setEnabled(False)
            self.progress_bar.setValue(0)

    def _set_buttons_enabled(self, enabled):
        self.compute_btn.setEnabled(enabled)
        self.file_btn.setEnabled(enabled)
        self.fetch_btn.setEnabled(enabled)

    def _on_ui_test(self):
        self.ui_test_count += 1
        self.counter_label.setText(f"点击次数: {self.ui_test_count}")
        self._append_log(f"UI 响应正常 (第 {self.ui_test_count} 次)")

    def closeEvent(self, event):
        # 窗口关闭时确保线程退出
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ThreadDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
