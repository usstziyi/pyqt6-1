"""
Unit 3.3: 事件处理器 (Event Handler)
学习目标:
  1. 理解事件 (Event) 与信号 (Signal) 的区别
  2. 掌握常见的重写事件方法: keyPressEvent, mousePressEvent, closeEvent 等
  3. 理解事件过滤器 eventFilter() 的用法
  4. 了解事件传播机制: 事件可以被子控件拦截

关键概念:
  - 信号: 高级抽象, 如 "按钮被点击" (Qt 内部事件处理后发射)
  - 事件: 底层原始事件, 如 "鼠标按下了" (操作系统传递)
  - 通常使用信号即可, 事件处理器用于需要底层控制的场景
  - eventFilter(obj, event): 拦截目标对象的事件, 可修改或阻止

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qobject.html#eventFilter
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QLineEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QCloseEvent


class EventHandlerDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("事件处理器演示")
        self.resize(450, 350)

        central = QWidget()
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("1. 键盘事件 (keyPressEvent) - 按任意键试试:"))

        self.key_label = QLabel("等待按键...")
        # padding 是 CSS（在这里是 Qt 的 QSS）属性，表示 控件内容与边框之间的内边距。
        self.key_label.setStyleSheet(
            "background-color: #34C759; padding: 10px; border-radius: 4px;"
        )
        layout.addWidget(self.key_label)

        layout.addWidget(QLabel("2. 鼠标事件 (mousePressEvent) - 点击下方区域:"))

        self.mouse_label = QLabel("点击这里")
        self.mouse_label.setStyleSheet(
            "background-color: #E1BEE7; padding: 20px; border-radius: 4px;"
        )
        self.mouse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.mouse_label)

        layout.addWidget(QLabel("3. 关闭事件 (closeEvent) - 尝试关闭窗口:"))
        self.close_label = QLabel("关闭前会弹出确认对话框")
        layout.addWidget(self.close_label)

        # 测试
        myLineEdit = QLineEdit()
        layout.addWidget(myLineEdit)

        layout.addStretch()

        self.setCentralWidget(central)

        """
        正常流程：  你按下键盘  →  输入框收到字符  →  显示在输入框里

        安装过滤器后：
        你按下键盘  →  【主窗口先截胡检查】→  是数字? →  放行给输入框
                                            →  不是?   →  拦截，不传给输入框
        """
        # 安装事件过滤器: 让 self 拦截 QLineEdit 的事件
        # 事件过滤器允许在其他对象之前处理事件
        self.filtered_edit = QLineEdit()
        self.filtered_edit.setPlaceholderText("输入时只允许数字 (事件过滤器拦截)")
        # installEventFilter(): 将 self 注册为 filtered_edit 的事件过滤器
        # 也可以把别的QObject对象注册为事件过路器
        # 让主窗口拦截它的键盘事件
        # 这个 self = EventHandlerDemo 实例 = 主窗口
        self.filtered_edit.installEventFilter(self)
        layout.insertWidget(3, QLabel("4. 事件过滤器 - 只允许输入数字:"))
        layout.insertWidget(4, self.filtered_edit)



    # --- 键盘事件 ---
    def keyPressEvent(self, event: QKeyEvent):
        # key(): 返回按下的键的枚举值
        # QKeyCombination 需用 key() 提取键值
        key = event.key()
        # Key_XXX: Qt.Key 枚举值
        # 修饰不可见字符，保留可见字符
        key_name = {
            Qt.Key.Key_Return: "Enter",
            Qt.Key.Key_Escape: "Escape",
            Qt.Key.Key_Space: "Space",
            Qt.Key.Key_Backspace: "Backspace",
        }.get(key, event.text())

        print(key_name)

        # 返回一个 位掩码整数 ，每个修饰键占一个 bit
        modifiers = event.modifiers()
        mod_str = ""
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            mod_str += "Ctrl+"
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            mod_str += "Shift+"
        if modifiers & Qt.KeyboardModifier.AltModifier:
            mod_str += "Alt+"

        self.key_label.setText(f"按键: {mod_str}{key_name} (code={key})")
        # 调用父类方法确保默认行为正常
        super().keyPressEvent(event)

    # --- 鼠标事件 ---
    def mousePressEvent(self, event: QMouseEvent):
        # position(): 返回鼠标在控件内的坐标
        pos = event.position()
        button_map = {
            Qt.MouseButton.LeftButton: "左键",
            Qt.MouseButton.RightButton: "右键",
            Qt.MouseButton.MiddleButton: "中键",
        }
        button = button_map.get(event.button(), "未知")
        self.mouse_label.setText(
            f"鼠标 {button} 点击在 (x={int(pos.x())}, y={int(pos.y())})"
        )
        super().mousePressEvent(event)

    # --- 关闭事件 ---
    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(
            self,
            "确认退出",
            "确定要关闭窗口吗?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close_label.setText("窗口即将关闭...")
            event.accept()  # 接受关闭事件
        else:
            self.close_label.setText("关闭已取消")
            event.ignore()  # 忽略关闭事件，阻止窗口关闭

    # --- 事件过滤器 ---
    """
    当 eventFilter 被触发时， obj 是 filtered_edit （输入框），
    而执行 eventFilter 方法的是 self （主窗口实例）。
    eventFilter 相当于在 EventHandlerDemo （主窗口）和 QLineEdit （输入框）之间插入了一道检查站：
    注意：注册过滤器时不一定都用主窗口的，还可以自定义。
    那么就不用重写主窗口的 eventFilter。
    """
    def eventFilter(self, obj, event):
        # 只拦截 KeyPress 事件
        if obj is self.filtered_edit and event.type() == QEvent.Type.KeyPress:
            key = event.key()
            # 允许: 数字、退格、方向键
            allowed = {
                Qt.Key.Key_0, Qt.Key.Key_1, Qt.Key.Key_2,
                Qt.Key.Key_3, Qt.Key.Key_4, Qt.Key.Key_5,
                Qt.Key.Key_6, Qt.Key.Key_7, Qt.Key.Key_8,
                Qt.Key.Key_9,
                Qt.Key.Key_Backspace, Qt.Key.Key_Left,
                Qt.Key.Key_Right, Qt.Key.Key_Delete,
                Qt.Key.Key_Home, Qt.Key.Key_End,
            }
            if key not in allowed:
                # 返回 True 表示事件已被处理，不再传递给目标控件obj
                # 事件被self主窗口拦截
                print("吞噬")
                return True
        # 返回 False 或调用父类，让事件继续传播
        # 把事件交给QMainWindow，走正常流程
        return super().eventFilter(obj, event)


def main():
    app = QApplication(sys.argv)
    window = EventHandlerDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
