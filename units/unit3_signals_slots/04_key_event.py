import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QLineEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QCloseEvent



class MyEditLine(QLineEdit):
    def __init__(self):
        super().__init__()
    
    """
    父控件、父类是不一样的
    """
    def keyPressEvent(self,event:QKeyEvent):
        # --------- MyEditLine先自己处理一下 -----------
        key = event.key()
        # 保留可显示字符,给不可显示键赋予名称
        key_name = {
            Qt.Key.Key_Return: "Enter",
            Qt.Key.Key_Escape: "Escape",
            Qt.Key.Key_Space: "Space",
            Qt.Key.Key_Backspace: "Backspace",
        }.get(key, event.text())

        # 假如：Space 处理不了，不传给父类，提前就交给父控件处理
        if key_name=='Space':
            event.ignore() # 交给父控件处理
            return

        print(f"MyEditLine:{key_name}")
    
       
        # ----------把event交给父类QMainWindow 继续处理------------
        # 经测试，数字、字母 父类都会显示进编辑框，其他按键全都不处理，ignore给了 父控件
        super().keyPressEvent(event)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(450, 350)

        central = QWidget()
        layout = QVBoxLayout(central)

        myLineEdit = MyEditLine()
        layout.addWidget(myLineEdit)

    
        self.setCentralWidget(central)


    # --- 键盘事件 ---
    def keyPressEvent(self, event: QKeyEvent):

        # ----------MainWindow 先处理一下 -------------
        key = event.key()
        key_name = {
            Qt.Key.Key_Return: "Enter",
            Qt.Key.Key_Escape: "Escape",
            Qt.Key.Key_Space: "Space",
            Qt.Key.Key_Backspace: "Backspace",
        }.get(key, event.text())
        print(f" MainWindow:{key_name}")

        # ----------QMainWindow 再处理一下 -------------
        super().keyPressEvent(event)



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
