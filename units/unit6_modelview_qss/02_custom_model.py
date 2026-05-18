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
        Model 的核心方法: 返回指定 index 和 role 的数据
        """
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        todo = self._todos[row]

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

        elif role == Qt.ItemDataRole.ToolTipRole:
            # 工具提示
            if col == 1:
                status = "完成" if todo["done"] else "未完成"
                return f"{todo['desc']} [{status}]"

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        # 表头数据
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.COLUMNS[section]
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
                self.dataChanged.emit(index, index, [role])
                return True

        elif role == Qt.ItemDataRole.CheckStateRole:
            if col == 3:
                todo["done"] = (value == Qt.CheckState.Checked.value)
                self.dataChanged.emit(index, index, [role])
                # 当完成状态改变时，刷新整行 (因为背景色会变)
                top_left = self.index(row, 0)
                bottom_right = self.index(row, self.columnCount() - 1)
                self.dataChanged.emit(top_left, bottom_right, [role])
                return True

        return False

    def add_todo(self, desc, priority="中"):
        row_count = len(self._todos)
        # beginInsertRows / endInsertRows: 通知 View 即将/已完成插入
        self.beginInsertRows(QModelIndex(), row_count, row_count)
        self._todos.append({
            "id": self._next_id,
            "desc": desc,
            "priority": priority,
            "done": False,
        })
        self._next_id += 1
        self.endInsertRows()

    def remove_todo(self, row):
        if 0 <= row < len(self._todos):
            # beginRemoveRows / endRemoveRows: 通知 View 即将/已完成删除
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._todos[row]
            self.endRemoveRows()

    def toggle_todo(self, row):
        if 0 <= row < len(self._todos):
            self._todos[row]["done"] = not self._todos[row]["done"]
            top_left = self.index(row, 0)
            bottom_right = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right)

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
        self.table_view.setAlternatingRowColors(True)
        self.table_view.verticalHeader().setVisible(False)
        # 设置列宽
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        # 创建模型并绑定
        self.model = TodoTableModel(self)
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
