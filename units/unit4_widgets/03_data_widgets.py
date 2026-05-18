"""
Unit 4.3: QListWidget, QTreeWidget, QTableWidget —— 数据展示控件
学习目标:
  1. 掌握 QListWidget 的各项操作: 添加/删除/多选/排序
  2. 理解 QTreeWidget 的树形结构与父子关系
  3. 学会 QTableWidget 的单元格操作、行列管理、表头设置

关键概念:
  - QListWidget: 基于项的列表控件
  - QTreeWidget: 树形控件，支持展开/折叠和层级数据
  - QTableWidget: 表格控件，适用于数据集展示
  - 这三个是便捷控件 (item-based)，Unit 6 将学习更强大的 Model/View 架构

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qlistwidget.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qtreewidget.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qtablewidget.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTabWidget,
    QListWidget, QListWidgetItem,
    QTreeWidget, QTreeWidgetItem,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class DataWidgetsDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据展示控件演示")
        self.resize(650, 500)

        tabs = QTabWidget()

        tabs.addTab(self._create_list_tab(), "QListWidget 列表")
        tabs.addTab(self._create_tree_tab(), "QTreeWidget 树形")
        tabs.addTab(self._create_table_tab(), "QTableWidget 表格")

        self.setCentralWidget(tabs)

    def _create_list_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 输入区域
        input_row = QHBoxLayout()
        self.list_input = QLineEdit()
        self.list_input.setPlaceholderText("输入新项目...")
        input_row.addWidget(self.list_input)

        add_btn = QPushButton("添加")
        add_btn.clicked.connect(self._add_list_item)
        input_row.addWidget(add_btn)

        del_btn = QPushButton("删除选中")
        del_btn.clicked.connect(self._del_list_item)
        input_row.addWidget(del_btn)

        sort_btn = QPushButton("排序")
        sort_btn.clicked.connect(lambda: self.list_widget.sortItems())
        input_row.addWidget(sort_btn)

        layout.addLayout(input_row)

        # QListWidget: 基于项的列表
        self.list_widget = QListWidget()
        # setSelectionMode: 支持多选
        self.list_widget.setSelectionMode(
            QListWidget.SelectionMode.ExtendedSelection
        )
        # 添加初始项
        for item_text in ["Python", "TypeScript", "Rust", "Go", "Kotlin"]:
            item = QListWidgetItem(f"  {item_text}")
            # QListWidgetItem 支持设置图标、颜色、标志等
            self.list_widget.addItem(item)

        # itemClicked(item) 信号: 项被点击时发射
        self.list_widget.itemClicked.connect(
            lambda item: self._update_tab_status(
                "list", f"点击了: {item.text().strip()}"
            )
        )
        layout.addWidget(self.list_widget)

        # 状态标签
        self.list_status = QLabel()
        layout.addWidget(self.list_status)

        return tab

    def _add_list_item(self):
        text = self.list_input.text().strip()
        if text:
            item = QListWidgetItem(f"  {text}")
            self.list_widget.addItem(item)
            self.list_input.clear()

    def _del_list_item(self):
        # selectedItems(): 返回所有选中项的列表
        for item in self.list_widget.selectedItems():
            # takeItem(row): 移除并返回指定行的项
            row = self.list_widget.row(item)
            self.list_widget.takeItem(row)

    def _create_tree_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # QTreeWidget: 树形控件
        self.tree = QTreeWidget()
        # setHeaderLabels: 设置列标题
        self.tree.setHeaderLabels(["名称", "大小", "类型"])
        # 设置列宽模式: 第一列拉伸
        self.tree.header().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )

        # 创建根节点
        root = QTreeWidgetItem(self.tree, ["项目代码", "", "目录"])
        root.setExpanded(True)  # 展开根节点

        # 创建子节点
        src = QTreeWidgetItem(root, ["src", "", "目录"])
        QTreeWidgetItem(src, ["main.py", "2.3 KB", "Python 文件"])
        QTreeWidgetItem(src, ["utils.py", "1.1 KB", "Python 文件"])

        tests = QTreeWidgetItem(root, ["tests", "", "目录"])
        QTreeWidgetItem(tests, ["test_main.py", "3.5 KB", "Python 文件"])

        docs = QTreeWidgetItem(root, ["docs", "", "目录"])
        QTreeWidgetItem(docs, ["readme.md", "1.8 KB", "Markdown"])

        # 设置背景色示例
        for i in range(src.childCount()):
            child = src.child(i)
            child.setBackground(0, QColor("#E8F5E9"))

        # itemClicked: 项被点击
        self.tree.itemClicked.connect(
            lambda item, col: self._update_tab_status(
                "tree", f"点击: {item.text(0)} (列 {col})"
            )
        )
        layout.addWidget(self.tree)

        self.tree_status = QLabel()
        layout.addWidget(self.tree_status)

        return tab

    def _create_table_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 工具栏
        tool_row = QHBoxLayout()

        self.table_name_edit = QLineEdit()
        self.table_name_edit.setPlaceholderText("姓名")
        tool_row.addWidget(self.table_name_edit)

        self.table_age_edit = QLineEdit()
        self.table_age_edit.setPlaceholderText("年龄")
        tool_row.addWidget(self.table_age_edit)

        add_row_btn = QPushButton("添加行")
        add_row_btn.clicked.connect(self._add_table_row)
        tool_row.addWidget(add_row_btn)

        del_row_btn = QPushButton("删除行")
        del_row_btn.clicked.connect(self._del_table_row)
        tool_row.addWidget(del_row_btn)

        layout.addLayout(tool_row)

        # QTableWidget: 表格控件
        self.table = QTableWidget()
        self.table.setRowCount(0)      # 初始 0 行
        self.table.setColumnCount(3)   # 3 列
        self.table.setHorizontalHeaderLabels(["姓名", "年龄", "状态"])

        # 设置列宽模式
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        # 设置选中行为: 选中整行
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        # 预置数据
        preset_data = [
            ("张三", "28", "在职"),
            ("李四", "35", "在职"),
            ("王五", "42", "休假"),
            ("赵六", "24", "在职"),
        ]
        for name, age, status in preset_data:
            self._insert_table_row(self.table.rowCount(), name, age, status)

        # cellClicked: 单元格被点击
        self.table.cellClicked.connect(
            lambda r, c: self._update_tab_status(
                "table",
                f"点击: [{r},{c}] = {self.table.item(r, c).text() if self.table.item(r, c) else ''}"
            )
        )
        layout.addWidget(self.table)

        self.table_status = QLabel()
        layout.addWidget(self.table_status)

        return tab

    def _insert_table_row(self, row, name, age, status):
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(age))
        self.table.setItem(row, 2, QTableWidgetItem(status))

    def _add_table_row(self):
        name = self.table_name_edit.text().strip()
        age = self.table_age_edit.text().strip()
        if name and age:
            self._insert_table_row(self.table.rowCount(), name, age, "在职")
            self.table_name_edit.clear()
            self.table_age_edit.clear()

    def _del_table_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    def _update_tab_status(self, which, msg):
        if which == "list":
            self.list_status.setText(msg)
        elif which == "tree":
            self.tree_status.setText(msg)
        elif which == "table":
            self.table_status.setText(msg)


def main():
    app = QApplication(sys.argv)
    window = DataWidgetsDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
