"""
Unit 6.2: 自定义 Model —— QAbstractTableModel 子类
学习目标:
  1. 掌握 QAbstractTableModel 的 3 个必须重写方法: rowCount, columnCount, data
  2. 理解 Qt.ItemDataRole (DisplayRole, EditRole, ToolTipRole 等)
  3. 学会 headerData() 自定义表头
  4. 掌握 flags() 控制单元格的可编辑性和可选性
  5. 学会 setData() 实现可编辑模型

关键概念:
  - QAbstractTableModel 是最常用的自定义模型基类
  - data(index, role) 返回不同角色的数据
  - index() 方法由父类实现，用于定位数据
  - beginInsertRows / endInsertRows 通知 View 数据变更

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qabstracttablemodel.html
"""
import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableView,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex
)
from PyQt6.QtGui import QColor, QBrush


class TodoTableModel(QAbstractTableModel):
    """
    自定义 QAbstractTableModel: 待办事项数据模型
    """

    # 列定义
    COLUMNS = ("ID", "任务描述", "优先级", "完成")

    def __init__(self, parent=None):
        # 把「父控件/父对象」传给父类的构造函数
        # 翻译成人话： 调用父类的构造函数，并告诉父类"我的父对象是谁"。
        # Qt 这边类似，只是 Qt 把"主人"直接交给了基类去管理
        # Qt 在 QObject 层面把 parent 记录下来了
        # 此后 parent 销毁时，Qt 会自动销毁它
        # parent->children.append(this);
        # 把自己加入父对象的 children 列表
        super().__init__(parent)
        # 内部数据存储: list of dict
        self._todos = []
        self._next_id = 1

        # 初始化示例数据
        sample = [
            ("学习 PyQt6 Model/View", "高"),
            ("完成项目文档编写", "中"),
            ("代码审查", "高"),
            ("修复 Bug #42", "低"),
            ("周会准备", "中"),
        ]
        for desc, priority in sample:
            self.add_todo(desc, priority)

    def rowCount(self, parent=QModelIndex()):
        # 行数
        return len(self._todos)

    def columnCount(self, parent=QModelIndex()):
        # 列数
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        Model 的核心方法: 返回指定 index 和 role ，View 想要的"数据类型"

        data() 被调用得 非常频繁 ——每次滚动、重绘、鼠标悬停都会反复调用。所以关键原则是：
        data() 里的 self._todos[row] 必须是 O(1) 操作
        """
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        todo = self._todos[row] # Qt 完全不关心你怎么存，只要 data() 能返回正确的值就行

        if role == Qt.ItemDataRole.DisplayRole:
            # 展示文本
            if col == 0:
                return str(todo["id"])
            elif col == 1:
                return todo["desc"]
            elif col == 2:
                return todo["priority"]
            elif col == 3:
                return "是" if todo["done"] else "否"

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # 对齐方式
            if col in (0, 2, 3):
                return int(Qt.AlignmentFlag.AlignCenter)
            return int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        elif role == Qt.ItemDataRole.ForegroundRole:
            # 前景色
            if col == 2:
                if todo["priority"] == "高":
                    return QBrush(QColor("#D32F2F"))
                elif todo["priority"] == "中":
                    return QBrush(QColor("#F57F17"))
            elif col == 3 and todo["done"]:
                return QBrush(QColor("#2E7D32"))

        elif role == Qt.ItemDataRole.BackgroundRole:
            # 背景色: 完成的任务行用浅绿色背景
            if todo["done"]:
                return QBrush(QColor("#E8F5E9"))

        elif role == Qt.ItemDataRole.CheckStateRole:
            if col == 3:
                return Qt.CheckState.Checked.value if todo["done"] else Qt.CheckState.Unchecked.value

        elif role == Qt.ItemDataRole.ToolTipRole:
            if col == 1:
                status = "完成" if todo["done"] else "未完成"
                return f"{todo['desc']} [{status}]"

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        # 处理水平表头（列标题）：返回对应列的名称
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.COLUMNS[section]
        # 处理垂直表头（行号）：返回行号（从1开始计数）
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return str(section + 1)
        return None

    def flags(self, index):
        # 控制单元格的操作权限
        default_flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.column() == 1:  # 任务描述列可编辑
            return default_flags | Qt.ItemFlag.ItemIsEditable
        elif index.column() == 3:  # 完成列: 可勾选切换
            return default_flags | Qt.ItemFlag.ItemIsUserCheckable
        return default_flags  # ID 和优先级不可编辑

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """
        编辑数据时的回调
        """
        if not index.isValid():
            return False

        row = index.row()
        col = index.column()
        todo = self._todos[row]

        if role == Qt.ItemDataRole.EditRole:
            if col == 1:
                todo["desc"] = str(value)
                # dataChanged 信号通知 View 刷新
                """
                View 收到的信号 → dataChanged(cell(row,1), cell(row,1), [EditRole])
                                       ↓
                View 重新调用 → model.data(index, DisplayRole)    ← 从 EditRole 自动转换而来
                            model.data(index, ForegroundRole)  ← 没变，可能跳过
                            model.data(index, BackgroundRole)  ← 没变，可能跳过
                """
                self.dataChanged.emit(index, index, [role])
                return True

        elif role == Qt.ItemDataRole.CheckStateRole:
            if col == 3:
                todo["done"] = (value == Qt.CheckState.Checked.value)
                top_left = self.index(row, 0)
                bottom_right = self.index(row, self.columnCount() - 1)
                # 省略 roles 参数 = 告诉 View "所有角色都变了" ，
                # View 会重新查询 BackgroundRole、DisplayRole、ForegroundRole 等
                self.dataChanged.emit(top_left, bottom_right)
                return True

        return False

    def add_todo(self, desc, priority="中"):
        # 表中已有多少行
        row_count = len(self._todos)
        # beginInsertRows / endInsertRows: 通知 View 即将/已完成插入
        self.beginInsertRows(
            QModelIndex(), # 插入到 顶层 （不是某个树的子节点）。这是一个 表格模型 ，没有父子层级，所以 parent 为空
            row_count, # 新行插入的 起始位置 。比如已有 5 行， row_count=5 ，新行插在第 5 行（索引从 0 开始）
            row_count # 新行插入的 结束位置 。只插入 1 行，所以 first == last
        ) # 冻结视图
        self._todos.append({
            "id": self._next_id,
            "desc": desc,
            "priority": priority,
            "done": False,
        })
        self._next_id += 1
        self.endInsertRows() # 通知重绘

    def remove_todo(self, row):
        if 0 <= row < len(self._todos):
            # beginRemoveRows / endRemoveRows: 通知 View 即将/已完成删除
            self.beginRemoveRows(QModelIndex(), row, row)
            # 这是 Python 的 del 语句，删除列表元素
            del self._todos[row]
            self.endRemoveRows()

    def toggle_todo(self, row):
        if 0 <= row < len(self._todos):
            self._todos[row]["done"] = not self._todos[row]["done"]
            # 构造一个矩形范围
            top_left = self.index(row, 0) # 行号、列号
            bottom_right = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right) # 左上角、右下角

    def get_todo(self, row):
        if 0 <= row < len(self._todos):
            return self._todos[row]
        return None


class CustomModelDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义 QAbstractTableModel 演示")
        self.resize(650, 450)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # TableView
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        # 启用交替行背景色，使表格更易读
        self.table_view.setAlternatingRowColors(True)
        self.table_view.horizontalHeader().setVisible(True)
        self.table_view.verticalHeader().setVisible(True)
        # 设置列宽
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        # 创建模型并绑定
        # 当 QMainWindow 窗口关闭被销毁时， TodoTableModel 也会被自动销毁，你不需要手动 del model ，也不会造成内存泄漏。
        self.model = TodoTableModel(self) # QAbstractTableModel
        self.table_view.setModel(self.model)

        main_layout.addWidget(self.table_view)

        # 操作按钮
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("添加任务")
        add_btn.clicked.connect(self._add_todo)
        btn_layout.addWidget(add_btn)

        del_btn = QPushButton("删除任务")
        del_btn.clicked.connect(self._delete_todo)
        btn_layout.addWidget(del_btn)

        toggle_btn = QPushButton("切换完成状态")
        toggle_btn.clicked.connect(self._toggle_todo)
        btn_layout.addWidget(toggle_btn)

        stats_btn = QPushButton("统计")
        stats_btn.clicked.connect(self._show_stats)
        btn_layout.addWidget(stats_btn)

        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        self.status_label = QLabel(f"共 {self.model.rowCount()} 个任务")
        main_layout.addWidget(self.status_label)

        # 监听模型变化
        self.model.dataChanged.connect(self._on_data_changed)
        self.model.rowsInserted.connect(
            lambda: self.status_label.setText(f"共 {self.model.rowCount()} 个任务")
        )
        self.model.rowsRemoved.connect(
            lambda: self.status_label.setText(f"共 {self.model.rowCount()} 个任务")
        )

        self.setCentralWidget(central)

    def _add_todo(self):
        import random
        priorities = ["高", "中", "低"]
        descs = [
            "新增功能模块", "编写单元测试", "优化性能",
            "更新文档", "会议纪要整理", "设计评审"
        ]
        desc = random.choice(descs)
        priority = random.choice(priorities)
        self.model.add_todo(desc, priority)

    def _delete_todo(self):
        indexes = self.table_view.selectionModel().selectedRows()
        if indexes:
            self.model.remove_todo(indexes[0].row())

    def _toggle_todo(self):
        indexes = self.table_view.selectionModel().selectedRows()
        if indexes:
            self.model.toggle_todo(indexes[0].row())

    def _show_stats(self):
        total = self.model.rowCount()
        done = sum(1 for t in self.model._todos if t["done"])
        high = sum(1 for t in self.model._todos if t["priority"] == "高")
        QMessageBox.information(
            self, "任务统计",
            f"总计: {total} 个任务\n"
            f"已完成: {done} 个\n"
            f"未完成: {total - done} 个\n"
            f"高优先级: {high} 个"
        )

    def _on_data_changed(self, topLeft, bottomRight):
        for row in range(topLeft.row(), bottomRight.row() + 1):
            todo = self.model.get_todo(row)
            if todo and todo["done"]:
                self.status_label.setText(
                    f"共 {self.model.rowCount()} 个任务 | "
                    f"'{todo['desc']}' 已完成!"
                )
                return


def main():
    app = QApplication(sys.argv)
    window = CustomModelDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
