"""
Unit 8: 实战项目 —— 任务管理桌面应用 (TaskFlow)

项目概述:
  使用 PyQt6 构建一个完整的任务管理桌面应用，涵盖:
  - 任务列表的增删改查
  - 优先级管理 (高/中/低) 和状态管理 (待办/进行中/已完成)
  - Model/View 架构数据展示
  - QSS 主题美化
  - 搜索过滤功能
  - 任务数据 JSON 文件持久化
  - 菜单栏、工具栏、状态栏
  - 关于对话框

技术覆盖:
  - Unit 1: QApplication, QMainWindow, 窗口生命周期
  - Unit 2: QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QTabWidget
  - Unit 3: 内置信号/槽, 自定义 pyqtSignal, 事件处理
  - Unit 4: QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QTextEdit
  - Unit 5: QMessageBox, QFileDialog, QInputDialog, 自定义 QDialog
  - Unit 6: QAbstractTableModel, QSortFilterProxyModel, QSS 美化
  - Unit 7: QTimer (自动保存), 事件循环

运行方式:
  python main.py

依赖:
  PyQt6 (>= 6.5)
"""
import sys
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QComboBox, QCheckBox, QSpinBox, QDateEdit,
    QTableView, QHeaderView, QMessageBox,
    QFileDialog, QDialog, QDialogButtonBox,
    QGroupBox
)
from PyQt6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex,
    QSortFilterProxyModel, QTimer, QDate
)
from PyQt6.QtGui import QAction, QColor, QBrush

# ============================================================
# 全局 QSS 样式
# ============================================================

APP_QSS = """
QMainWindow {
    background-color: #F5F5F5;
}

QGroupBox {
    border: 1px solid #BDBDBD;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 14px;
    font-weight: bold;
    font-size: 13px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #424242;
}

QPushButton {
    background-color: #1976D2;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 12px;
}

QPushButton:hover { background-color: #1565C0; }
QPushButton:pressed { background-color: #0D47A1; }
QPushButton:disabled {
    background-color: #BDBDBD;
    color: #757575;
}

QPushButton#danger_btn {
    background-color: #D32F2F;
}
QPushButton#danger_btn:hover { background-color: #C62828; }

QPushButton#success_btn {
    background-color: #388E3C;
}
QPushButton#success_btn:hover { background-color: #2E7D32; }

QPushButton#warning_btn {
    background-color: #F57C00;
}
QPushButton#warning_btn:hover { background-color: #E65100; }

QPushButton#toolbar_btn {
    background-color: transparent;
    color: #424242;
    padding: 4px 10px;
    border-radius: 2px;
}
QPushButton#toolbar_btn:hover {
    background-color: #E0E0E0;
}

QTableView {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    gridline-color: #E0E0E0;
    background-color: white;
    alternate-background-color: #FAFAFA;
    selection-background-color: #BBDEFB;
    selection-color: #212121;
}

QTableView::item {
    padding: 6px 8px;
}

QHeaderView::section {
    background-color: #EEEEEE;
    border: none;
    border-bottom: 2px solid #BDBDBD;
    padding: 6px 8px;
    font-weight: bold;
}

QLineEdit, QComboBox, QSpinBox, QDateEdit, QTextEdit {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    padding: 6px 8px;
    font-size: 12px;
    background-color: white;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {
    border-color: #1976D2;
    border-width: 2px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #BDBDBD;
}

QTabWidget::pane {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    background-color: white;
}

QTabBar::tab {
    background-color: #E0E0E0;
    border: 1px solid #BDBDBD;
    padding: 6px 14px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom-color: white;
}

QStatusBar {
    background-color: #EEEEEE;
    border-top: 1px solid #BDBDBD;
}

QMenuBar {
    background-color: #FAFAFA;
    border-bottom: 1px solid #E0E0E0;
}

QMenuBar::item:selected {
    background-color: #E3F2FD;
}

QToolBar {
    background-color: #FAFAFA;
    border-bottom: 1px solid #E0E0E0;
    spacing: 4px;
    padding: 2px;
}
"""


# ============================================================
# 数据模型
# ============================================================

class TaskModel(QAbstractTableModel):
    """
    自定义任务数据模型
    列: 完成?, 标题, 优先级, 状态, 截止日期, 分类
    """

    COLUMNS = ("", "标题", "优先级", "状态", "截止日期", "分类")
    PRIORITY_ORDER = {"高": 0, "中": 1, "低": 2}

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tasks = []
        self._next_id = 1

    def rowCount(self, parent=QModelIndex()):
        return len(self._tasks)

    def columnCount(self, parent=QModelIndex()):
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        task = self._tasks[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 1:
                return task["title"]
            elif col == 2:
                return task["priority"]
            elif col == 3:
                return task["status"]
            elif col == 4:
                return task["due_date"]
            elif col == 5:
                return task["category"]

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return int(Qt.AlignmentFlag.AlignCenter)

        elif role == Qt.ItemDataRole.ForegroundRole:
            if col == 2:
                colors = {"高": QColor("#D32F2F"), "中": QColor("#F57F17"), "低": QColor("#388E3C")}
                return QBrush(colors.get(task["priority"], QColor("#000000")))
            if col == 3:
                colors = {"已完成": QColor("#2E7D32"), "进行中": QColor("#1565C0"), "待办": QColor("#757575")}
                return QBrush(colors.get(task["status"], QColor("#000000")))

        elif role == Qt.ItemDataRole.BackgroundRole:
            if task["status"] == "已完成":
                return QBrush(QColor("#E8F5E9"))

        elif role == Qt.ItemDataRole.ToolTipRole:
            return task.get("description", "")

        elif role == Qt.ItemDataRole.CheckStateRole:
            if col == 0:
                return Qt.CheckState.Checked if task["status"] == "已完成" else Qt.CheckState.Unchecked

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.COLUMNS[section]
        return None

    def flags(self, index):
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.column() == 0:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        return flags

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid():
            return False

        row = index.row()
        col = index.column()

        if role == Qt.ItemDataRole.CheckStateRole and col == 0:
            task = self._tasks[row]
            if value == Qt.CheckState.Checked.value:
                task["status"] = "已完成"
            else:
                task["status"] = "待办"
            self.dataChanged.emit(index, index, [role])
            top_left = self.index(row, 0)
            bottom_right = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right)
            return True

        return False

    def add_task(self, title, priority, status, due_date, category, description):
        row = len(self._tasks)
        self.beginInsertRows(QModelIndex(), row, row)
        self._tasks.append({
            "id": self._next_id,
            "title": title,
            "priority": priority,
            "status": status,
            "due_date": due_date,
            "category": category,
            "description": description,
            "created_at": datetime.now().isoformat(),
        })
        self._next_id += 1
        self.endInsertRows()

    def update_task(self, row, title, priority, status, due_date, category, description):
        if 0 <= row < len(self._tasks):
            task = self._tasks[row]
            task["title"] = title
            task["priority"] = priority
            task["status"] = status
            task["due_date"] = due_date
            task["category"] = category
            task["description"] = description
            top_left = self.index(row, 0)
            bottom_right = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right)

    def remove_task(self, row):
        if 0 <= row < len(self._tasks):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._tasks[row]
            self.endRemoveRows()

    def get_task(self, row):
        if 0 <= row < len(self._tasks):
            return self._tasks[row]
        return None

    def get_statistics(self):
        total = len(self._tasks)
        done = sum(1 for t in self._tasks if t["status"] == "已完成")
        in_progress = sum(1 for t in self._tasks if t["status"] == "进行中")
        pending = total - done - in_progress
        return {"total": total, "done": done, "in_progress": in_progress, "pending": pending}

    def to_json(self):
        return json.dumps(self._tasks, ensure_ascii=False, indent=2)

    def from_json(self, data):
        self.beginResetModel()
        self._tasks = json.loads(data)
        if self._tasks:
            self._next_id = max(t.get("id", 0) for t in self._tasks) + 1
        self.endResetModel()


# ============================================================
# 任务编辑对话框
# ============================================================

class TaskDialog(QDialog):
    """添加 / 编辑任务的对话框"""

    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.setWindowTitle("编辑任务" if task else "新建任务")
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        form.setSpacing(10)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("输入任务标题...")
        form.addRow("标题:", self.title_edit)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["中", "高", "低"])
        form.addRow("优先级:", self.priority_combo)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["待办", "进行中", "已完成"])
        form.addRow("状态:", self.status_combo)

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDate(QDate.currentDate().addDays(7))
        self.due_date_edit.setDisplayFormat("yyyy-MM-dd")
        form.addRow("截止日期:", self.due_date_edit)

        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems(["工作", "个人", "学习", "健康", "其他"])
        form.addRow("分类:", self.category_combo)

        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("任务描述 (可选)...")
        self.desc_edit.setMaximumHeight(100)
        form.addRow("描述:", self.desc_edit)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # 如果是编辑模式，填充已有数据
        if task:
            self.title_edit.setText(task.get("title", ""))
            self.priority_combo.setCurrentText(task.get("priority", "中"))
            self.status_combo.setCurrentText(task.get("status", "待办"))
            if task.get("due_date"):
                self.due_date_edit.setDate(QDate.fromString(task["due_date"], "yyyy-MM-dd"))
            self.category_combo.setCurrentText(task.get("category", ""))
            self.desc_edit.setPlainText(task.get("description", ""))

    def _on_accept(self):
        title = self.title_edit.text().strip()
        if not title:
            self.title_edit.setFocus()
            return
        self.accept()

    def get_task_data(self):
        return {
            "title": self.title_edit.text().strip(),
            "priority": self.priority_combo.currentText(),
            "status": self.status_combo.currentText(),
            "due_date": self.due_date_edit.date().toString("yyyy-MM-dd"),
            "category": self.category_combo.currentText().strip(),
            "description": self.desc_edit.toPlainText().strip(),
        }


# ============================================================
# 主窗口
# ============================================================

class TaskFlowMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskFlow - 任务管理")
        self.resize(900, 600)

        self._data_file = "tasks.json"
        self._auto_save_timer = QTimer(self)
        self._auto_save_timer.timeout.connect(self._auto_save)
        self._auto_save_timer.start(30000)  # 每 30 秒自动保存
        self._dirty = False

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        self._create_central_widget()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        # 文件菜单
        file_menu = menu_bar.addMenu("文件(&F)")

        import_action = QAction("导入(&I)...", self)
        import_action.triggered.connect(self._import_data)
        file_menu.addAction(import_action)

        export_action = QAction("导出(&E)...", self)
        export_action.triggered.connect(self._export_data)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 任务菜单
        task_menu = menu_bar.addMenu("任务(&T)")

        new_action = QAction("新建任务(&N)", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._add_task)
        task_menu.addAction(new_action)

        edit_action = QAction("编辑任务(&E)", self)
        edit_action.setShortcut("Ctrl+E")
        edit_action.triggered.connect(self._edit_task)
        task_menu.addAction(edit_action)

        delete_action = QAction("删除任务(&D)", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self._delete_task)
        task_menu.addAction(delete_action)

        task_menu.addSeparator()

        toggle_action = QAction("切换完成状态(&T)", self)
        toggle_action.setShortcut("Ctrl+T")
        toggle_action.triggered.connect(self._toggle_status)
        task_menu.addAction(toggle_action)

        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助(&H)")
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_tool_bar(self):
        tool_bar = self.addToolBar("主工具栏")
        tool_bar.setMovable(False)

        new_btn = QPushButton("＋ 新建")
        new_btn.setObjectName("toolbar_btn")
        new_btn.clicked.connect(self._add_task)
        tool_bar.addWidget(new_btn)

        edit_btn = QPushButton("✎ 编辑")
        edit_btn.setObjectName("toolbar_btn")
        edit_btn.clicked.connect(self._edit_task)
        tool_bar.addWidget(edit_btn)

        del_btn = QPushButton("✕ 删除")
        del_btn.setObjectName("toolbar_btn")
        del_btn.clicked.connect(self._delete_task)
        tool_bar.addWidget(del_btn)

        tool_bar.addSeparator()

        save_btn = QPushButton("💾 保存")
        save_btn.setObjectName("toolbar_btn")
        save_btn.clicked.connect(self._save_data)
        tool_bar.addWidget(save_btn)

    def _create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("就绪")

        # 永久显示统计
        self.stats_label = QLabel("任务: 0 | 完成: 0 | 进行中: 0 | 待办: 0")
        self.stats_label.setStyleSheet("padding-right: 10px;")
        self.status_bar.addPermanentWidget(self.stats_label)

    def _create_central_widget(self):
        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # --- 搜索栏 ---
        search_layout = QHBoxLayout()

        search_layout.addWidget(QLabel("搜索:"))

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入关键词过滤任务...")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.textChanged.connect(self._on_search)
        search_layout.addWidget(self.search_edit, 1)

        search_layout.addWidget(QLabel("状态:"))

        self.status_filter = QComboBox()
        self.status_filter.addItems(["全部", "待办", "进行中", "已完成"])
        self.status_filter.currentTextChanged.connect(self._on_search)
        search_layout.addWidget(self.status_filter)

        search_layout.addWidget(QLabel("优先级:"))

        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["全部", "高", "中", "低"])
        self.priority_filter.currentTextChanged.connect(self._on_search)
        search_layout.addWidget(self.priority_filter)

        main_layout.addLayout(search_layout)

        # --- TableView ---
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)
        self.table_view.setShowGrid(True)

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(0, 40)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(2, 80)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(3, 80)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(4, 100)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(5, 80)

        self.table_view.verticalHeader().setVisible(False)

        # 双击编辑
        self.table_view.doubleClicked.connect(self._on_double_click)

        main_layout.addWidget(self.table_view, 1)

        # --- 底部按钮 ---
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("新建任务")
        add_btn.setObjectName("success_btn")
        add_btn.clicked.connect(self._add_task)
        btn_layout.addWidget(add_btn)

        btn_layout.addStretch()

        del_btn = QPushButton("删除选中")
        del_btn.setObjectName("danger_btn")
        del_btn.clicked.connect(self._delete_task)
        btn_layout.addWidget(del_btn)

        refresh_btn = QPushButton("刷新统计")
        refresh_btn.setObjectName("warning_btn")
        refresh_btn.clicked.connect(self._update_stats)
        btn_layout.addWidget(refresh_btn)

        main_layout.addLayout(btn_layout)

        self.setCentralWidget(central)

        # --- Model & Proxy ---
        self.model = TaskModel(self)
        self.model.dataChanged.connect(self._on_data_changed)
        self.model.rowsInserted.connect(lambda: self._on_data_changed())
        self.model.rowsRemoved.connect(lambda: self._on_data_changed())

        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(-1)
        self.proxy_model.setFilterRole(Qt.ItemDataRole.DisplayRole)

        self.table_view.setModel(self.proxy_model)

    # --- 搜索过滤 ---
    def _on_search(self):
        text = self.search_edit.text().strip()
        self.proxy_model.setFilterFixedString(text)

        status = self.status_filter.currentText()
        priority = self.priority_filter.currentText()

        # 自定义过滤: 状态 + 优先级
        for row in range(self.proxy_model.rowCount()):
            source_index = self.proxy_model.mapToSource(
                self.proxy_model.index(row, 0)
            )
            task = self.model.get_task(source_index.row())
            show = True
            if status != "全部" and task and task["status"] != status:
                show = False
            if priority != "全部" and task and task["priority"] != priority:
                show = False
            self.table_view.setRowHidden(row, not show)

    # --- 任务 CRUD ---
    def _add_task(self):
        dialog = TaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_task_data()
            self.model.add_task(**data)
            self._update_stats()
            self._dirty = True
            self.status_bar.showMessage(f"已添加任务: {data['title']}", 3000)

    def _edit_task(self):
        row = self._selected_source_row()
        if row < 0:
            QMessageBox.information(self, "提示", "请先选中一个任务。")
            return

        task = self.model.get_task(row)
        dialog = TaskDialog(self, task)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_task_data()
            self.model.update_task(row, **data)
            self._update_stats()
            self._dirty = True
            self.status_bar.showMessage(f"已更新任务: {data['title']}", 3000)

    def _delete_task(self):
        row = self._selected_source_row()
        if row < 0:
            return

        task = self.model.get_task(row)
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除任务 '{task['title']}' 吗?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.model.remove_task(row)
            self._update_stats()
            self._dirty = True
            self.status_bar.showMessage(f"已删除任务: {task['title']}", 3000)

    def _toggle_status(self):
        row = self._selected_source_row()
        if row < 0:
            return
        task = self.model.get_task(row)
        new_status = "已完成" if task["status"] != "已完成" else "待办"
        task["status"] = new_status
        top_left = self.model.index(row, 0)
        bottom_right = self.model.index(row, self.model.columnCount() - 1)
        self.model.dataChanged.emit(top_left, bottom_right)
        self._update_stats()
        self._dirty = True

    def _on_double_click(self, index):
        self._edit_task()

    def _selected_source_row(self):
        proxy_indexes = self.table_view.selectionModel().selectedRows()
        if not proxy_indexes:
            return -1
        source_index = self.proxy_model.mapToSource(proxy_indexes[0])
        return source_index.row()

    # --- 数据持久化 ---
    def _auto_save(self):
        if self._dirty:
            self._save_data(silent=True)

    def _save_data(self, silent=False):
        try:
            with open(self._data_file, "w", encoding="utf-8") as f:
                f.write(self.model.to_json())
            self._dirty = False
            if not silent:
                self.status_bar.showMessage("数据已保存", 2000)
        except Exception as e:
            self.status_bar.showMessage(f"保存失败: {e}")

    def _load_data(self):
        if not os.path.exists(self._data_file):
            return
        try:
            with open(self._data_file, "r", encoding="utf-8") as f:
                self.model.from_json(f.read())
            self._update_stats()
            self.status_bar.showMessage("数据已加载", 2000)
        except Exception as e:
            self.status_bar.showMessage(f"加载数据失败: {e}")

    def _import_data(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "导入任务数据", "", "JSON 文件 (*.json);;所有文件 (*)"
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.model.from_json(f.read())
                self._update_stats()
                self._dirty = True
                self.status_bar.showMessage(f"已从 {os.path.basename(path)} 导入", 3000)
            except Exception as e:
                QMessageBox.critical(self, "导入失败", f"无法读取文件:\n{e}")

    def _export_data(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "导出任务数据", "tasks_export.json",
            "JSON 文件 (*.json);;所有文件 (*)"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.model.to_json())
                self.status_bar.showMessage(f"已导出到 {os.path.basename(path)}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "导出失败", f"无法写入文件:\n{e}")

    # --- 统计与状态 ---
    def _update_stats(self):
        stats = self.model.get_statistics()
        self.stats_label.setText(
            f"任务: {stats['total']} | 完成: {stats['done']} "
            f"| 进行中: {stats['in_progress']} | 待办: {stats['pending']}"
        )

    def _on_data_changed(self, *args):
        self._dirty = True
        self._update_stats()

    def _show_about(self):
        QMessageBox.about(
            self, "关于 TaskFlow",
            "<h2>TaskFlow 任务管理</h2>"
            "<p>使用 PyQt6 构建的桌面任务管理应用</p>"
            "<p><b>涵盖技术:</b></p>"
            "<ul>"
            "<li>QMainWindow 框架 + 菜单/工具栏/状态栏</li>"
            "<li>Model/View 架构 + QSortFilterProxyModel</li>"
            "<li>自定义 QDialog 对话框</li>"
            "<li>QSS 样式美化</li>"
            "<li>JSON 数据持久化</li>"
            "<li>QTimer 自动保存</li>"
            "</ul>"
            "<p>PyQt6 学习教程实战项目</p>"
        )

    # --- 窗口关闭 ---
    def closeEvent(self, event):
        if self._dirty:
            reply = QMessageBox.question(
                self, "未保存的更改",
                "任务数据已修改，是否保存后退出?",
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save,
            )
            if reply == QMessageBox.StandardButton.Save:
                self._save_data(silent=True)
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(APP_QSS)

    window = TaskFlowMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
