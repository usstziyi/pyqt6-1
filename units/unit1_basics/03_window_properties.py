"""
Unit 1.3: 窗口属性与生命周期
学习目标:
  1. 掌握窗口位置、大小、状态的控制
  2. 理解窗口标志 (WindowFlags) 对窗口外观和行为的影响
  3. 理解窗口居中屏幕的常用算法
  4. 了解窗口最小/最大尺寸约束

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qt.html#WindowType-enum
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt


class CenteredWindow(QMainWindow):
    """
    演示如何在屏幕中央显示窗口
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口居中演示")
        self.resize(500, 350)
        self._center_on_screen()

        label = QLabel("这个窗口自动居中在屏幕中央")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = label.font()
        font.setPointSize(14)
        label.setFont(font)
        self.setCentralWidget(label)

    def _center_on_screen(self):
        # primaryScreen(): 获取主屏幕对象
        screen = QApplication.primaryScreen()
        if screen is None:
            return
        # availableGeometry(): 返回可用屏幕区域的 QRect (不含任务栏)
        screen_rect = screen.availableGeometry()
        # 计算窗口居中位置: 屏幕中心 - 窗口尺寸的一半
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.move(x, y)


class WindowFlagsDemo(QMainWindow):
    """
    演示不同窗口标志对窗口外观的影响
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口属性演示")
        self.resize(500, 400)

        central = QWidget()
        layout = QVBoxLayout(central)

        info_label = QLabel("当前窗口状态将在底部显示")
        layout.addWidget(info_label)

        # --- 窗口最小/最大尺寸约束 ---
        # setMinimumSize(w, h): 限制窗口最小尺寸，防止被缩得太小
        self.setMinimumSize(300, 200)
        # setMaximumSize(w, h): 限制窗口最大尺寸，防止被拉得太大
        self.setMaximumSize(800, 600)

        btn_min = QPushButton("最小化窗口")
        # showMinimized(): 将窗口最小化到任务栏
        btn_min.clicked.connect(self.showMinimized)
        layout.addWidget(btn_min)

        btn_max = QPushButton("最大化窗口")
        btn_max.clicked.connect(self.showMaximized)
        layout.addWidget(btn_max)

        btn_full = QPushButton("全屏显示")
        # showFullScreen(): 全屏模式 (隐藏标题栏和边框)
        btn_full.clicked.connect(self.showFullScreen)
        layout.addWidget(btn_full)

        btn_normal = QPushButton("恢复正常")
        # showNormal(): 从最大化/最小化/全屏恢复到正常状态
        btn_normal.clicked.connect(self.showNormal)
        layout.addWidget(btn_normal)

        btn_always_top = QPushButton("切换置顶状态")
        btn_always_top.clicked.connect(self._toggle_always_on_top)
        layout.addWidget(btn_always_top)

        btn_transparent = QPushButton("切换半透明")
        btn_transparent.clicked.connect(self._toggle_transparency)
        layout.addWidget(btn_transparent)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setCentralWidget(central)

        self._is_top = False
        self._is_transparent = False

    def _toggle_always_on_top(self):
        self._is_top = not self._is_top
        if self._is_top:
            # WindowStaysOnTopHint: 窗口始终保持在所有窗口之上
            self.setWindowFlags(
                self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
            )
            self.status_label.setText("状态: 置顶已开启")
        else:
            # 去掉置顶标志: ~ 是按位取反
            self.setWindowFlags(
                self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint
            )
            self.status_label.setText("状态: 置顶已关闭")
        # 修改窗口标志后需要重新 show() 才能生效
        self.show()

    def _toggle_transparency(self):
        self._is_transparent = not self._is_transparent
        if self._is_transparent:
            # setWindowOpacity(0.0~1.0): 设置窗口透明度，1.0 不透明，0.0 完全透明
            self.setWindowOpacity(0.6)
            self.status_label.setText("状态: 半透明 (60% 不透明度)")
        else:
            self.setWindowOpacity(1.0)
            self.status_label.setText("状态: 完全不透明")


def main():
    app = QApplication(sys.argv)

    window1 = CenteredWindow()
    window1.show()

    window2 = WindowFlagsDemo()
    window2.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
