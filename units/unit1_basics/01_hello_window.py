"""
Unit 1.1: PyQt6 第一个窗口
学习目标:
  1. 理解 QApplication 的作用 —— 管理 GUI 应用程序的控制流和主要设置
  2. 理解 QWidget 的作用 —— 所有 GUI 控件的基类
  3. 理解事件循环 app.exec() —— 等待并分发用户交互事件
  4. 理解 sys.exit() 包裹 app.exec() 的原因 —— 传递退出码给操作系统

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qapplication.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qwidget.html
"""
import sys
from PyQt6.QtWidgets import QApplication, QWidget


def main():
    # data 参数: 命令行参数列表，Qt 内部会解析 --style 等内置选项
    app = QApplication(sys.argv)

    # QWidget 是最基础的窗口容器，没有菜单栏、状态栏等
    window = QWidget()

    # resize(width, height): 设置窗口的初始大小 (像素)
    window.resize(400, 300)

    # move(x, y): 设置窗口左上角在屏幕上的位置 (像素)
    window.move(200, 200)

    # setWindowTitle(title): 设置窗口标题栏文字
    window.setWindowTitle("Hello PyQt6 - 我的第一个窗口")

    # show(): 将窗口显示到屏幕上 (默认是隐藏的)
    window.show()

    # app.exec(): 进入 Qt 事件循环
    # - 等待用户操作 (鼠标点击、键盘输入等)
    # - 将事件分发给对应的控件处理
    # - 当最后一个窗口关闭时返回退出码
    # sys.exit(): 将 Qt 的退出码传递给 Python 进程
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
