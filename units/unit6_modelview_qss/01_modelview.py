"""
Unit 6.1: Model/View 架构 —— QTableView + QStandardItemModel
学习目标:
  1. 理解 Qt 的 Model/View 架构分离原则
  2. 掌握 QStandardItemModel 作为通用数据模型
  3. 学会 QTableView 与 Model 的绑定和配置
  4. 理解 QHeaderView 和列宽模式
  5. 学习 QSortFilterProxyModel 实现排序和过滤

关键概念:
  - Model (模型): 负责存储和访问数据 (QStandardItemModel, QAbstractTableModel 等)
  - View (视图): 负责展示数据 (QTableView, QListView, QTreeView)
  - Delegate (委托): 负责编辑和渲染 (QStyledItemDelegate)
  - 一个 Model 可以绑定多个 View
  - Proxy Model: 在 Model 和 View 之间插入过滤/排序逻辑

API 参考:
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/model-view-programming.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtgui/qstandarditemmodel.html
  https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qsortfilterproxymodel.html
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit,
    QTableView, QHeaderView, QMessageBox
)
from PyQt6.QtCore import (
    Qt, QSortFilterProxyModel, QModelIndex
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor


class ModelViewDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model/View 架构演示")
        self.resize(700, 500)

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # --- 搜索过滤栏 ---
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("搜索过滤:"))

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入关键词过滤...")
        self.search_edit.setClearButtonEnabled(True)
        # 实时过滤: 输入即过滤
        self.search_edit.textChanged.connect(self._on_search_text_changed)
        filter_layout.addWidget(self.search_edit)

        self.filter_column_label = QLabel("(全部列)")
        filter_layout.addWidget(self.filter_column_label)

        main_layout.addLayout(filter_layout)

        # --- QTableView ---
        self.table_view = QTableView()

        # 设置选中行为: 选中整行
        self.table_view.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        # 设置选中模式: 单行选中
        self.table_view.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )
        # 交替行颜色 (斑马线效果)
        self.table_view.setAlternatingRowColors(True)
        # 允许排序
        self.table_view.setSortingEnabled(True)
        # 隐藏垂直表头 (行号)
        self.table_view.verticalHeader().setVisible(False)
        # 最后一列自动拉伸
        self.table_view.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.table_view)

        # --- 操作按钮 ---
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("添加行")
        add_btn.clicked.connect(self._add_row)
        btn_layout.addWidget(add_btn)

        del_btn = QPushButton("删除选中行")
        del_btn.clicked.connect(self._delete_row)
        btn_layout.addWidget(del_btn)

        refresh_btn = QPushButton("刷新数据")
        refresh_btn.clicked.connect(self._refresh_data)
        btn_layout.addWidget(refresh_btn)

        show_data_btn = QPushButton("查看模型数据")
        show_data_btn.clicked.connect(self._show_model_data)
        btn_layout.addWidget(show_data_btn)

        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # --- 状态 ---
        self.status_label = QLabel(f"共 0 行")
        main_layout.addWidget(self.status_label)

        self.setCentralWidget(central)

        # --- 构建 Model ---
        self._setup_model()

    def _setup_model(self):
        # QStandardItemModel: 通用数据模型
        # QStandardItemModel(rows, columns, parent)
        self.model = QStandardItemModel(0, 5, self)

        # setHorizontalHeaderLabels: 设置列标题
        self.model.setHorizontalHeaderLabels([
            "ID", "姓名", "部门", "薪资", "入职日期"
        ])

        # 添加示例数据
        sample_data = [
            ("1001", "张三", "技术部", "15000", "2024-01-15"),
            ("1002", "李四", "市场部", "12000", "2024-02-20"),
            ("1003", "小王", "技术部", "18000", "2023-06-10"),
            ("1004", "赵六", "人事部", "11000", "2024-03-01"),
            ("1005", "孙七", "财务部", "14000", "2023-09-15"),
            ("1006", "周八", "技术部", "20000", "2022-11-01"),
            ("1007", "吴九", "市场部", "13000", "2024-04-10"),
        ]
        for data in sample_data:
            row_items = [QStandardItem(d) for d in data]
            # 设置部分单元格不可编辑
            row_items[0].setEditable(False)  # ID 不可编辑
            self.model.appendRow(row_items)

        # --- Proxy Model 实现过滤 ---
        self.proxy_model = QSortFilterProxyModel(self)
        # setSourceModel: 设置源模型
        self.proxy_model.setSourceModel(self.model)
        # 禁用代理模型的排序 (由 TableView 自己处理)
        self.proxy_model.setDynamicSortFilter(False)
        # 设置过滤角色: DisplayRole (以显示文本作为被搜索对象)
        self.proxy_model.setFilterRole(Qt.ItemDataRole.DisplayRole)
        # setFilterKeyColumn(-1): 搜索所有列
        self.proxy_model.setFilterKeyColumn(-1)

        # 将 View 绑定到 Proxy Model
        self.table_view.setModel(self.proxy_model)

        # 更新状态
        self._update_status()

    def _on_search_text_changed(self, text):
        # 设置过滤正则表达式
        # QSortFilterProxyModel 默认使用正则表达式
        self.proxy_model.setFilterRegularExpression(text)
        self._update_status()

    def _add_row(self):
        row = self.model.rowCount()
        new_id = str(1008 + row)  # 简单的 ID 生成
        row_items = [
            QStandardItem(new_id),
            QStandardItem("新员工"),
            QStandardItem("未分配"),
            QStandardItem("0"),
            QStandardItem("2024-06-01"),
        ]
        row_items[0].setEditable(False)
        self.model.appendRow(row_items)
        self._update_status()

    def _delete_row(self):
        # 因为 View 绑定的模型是 Proxy Model
        # 获取当前选中的索引 (来自 proxy model)
        # 这行代码获取 用户在 TableView 中当前选中的所有行
        # 获取用户在 TableView 中当前选中的所有行
        proxy_indexes = (
            self.table_view
            .selectionModel()  # 获取选择模型
            .selectedRows()     # 获取选中的行索引列表
        ) # 没有逗号，所以 () 只是续行，返回值就是 .selectedRows() 的结果：list[QModelIndex]
        if not proxy_indexes:
            return

        # 取第一个
        proxy_index = proxy_indexes[0]
        # 映射到源模型
        source_index = self.proxy_model.mapToSource(proxy_index)
        # 删除源模型中的行
        self.model.removeRow(source_index.row())
        self._update_status()

    def _refresh_data(self):
        # 更新所有薪资为随机值 (演示数据变更)
        import random
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 3)  # 薪资列
            if item:
                salary = random.randint(10000, 30000)
                item.setText(str(salary))
        self._update_status()
        self.status_label.setText(
            f"共 {self.model.rowCount()} 行 | 数据已刷新"
        )

    def _show_model_data(self):
        # 展示模型中的所有数据
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        lines = []
        for r in range(rows):
            row_data = []
            for c in range(cols):
                item = self.model.item(r, c)
                row_data.append(item.text() if item else "")
            lines.append(" | ".join(row_data))
        QMessageBox.information(
            self, "模型数据", "\n".join(lines[:20])
        )

    def _update_status(self):
        total = self.model.rowCount()      # 源模型的总行数（包含所有数据）
        visible = self.proxy_model.rowCount()  # 代理模型的可见行数（过滤后显示的行数）
        if total == visible:
            self.status_label.setText(f"共 {total} 行")
        else:
            self.status_label.setText(f"共 {total} 行 | 显示 {visible} 行 (已过滤)")


def main():
    app = QApplication(sys.argv)
    window = ModelViewDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
