# HumanResourcesGUI.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from HumanResources import HumanResources
from HumanResourcesView import HumanResourcesEditDialog

class HumanResourcesGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Quản lý nhân viên")
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên", "Số điện thoại", "Email", "Địa chỉ", "Giới tính", "Ngày sinh", "Vị trí", "Phòng ban"
        ])
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        self.view_button = QPushButton("Xem thông tin")
        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")
        button_layout.addWidget(self.view_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Load data
        self.load_data()

        # Connect buttons
        self.view_button.clicked.connect(self.view_employee)
        self.edit_button.clicked.connect(self.edit_employee)
        self.delete_button.clicked.connect(self.delete_employee)

    def load_data(self):
        employees = HumanResources.get_all_employees()
        self.table.setRowCount(len(employees))
        for row_idx, employee in enumerate(employees):
            for col_idx, value in enumerate(employee):
                item = QTableWidgetItem(str(value))
                if col_idx == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def view_employee(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            employee_id = int(self.table.item(selected_row, 0).text())
            dialog = HumanResourcesEditDialog(employee_id, view_only=True)
            dialog.exec()

    def edit_employee(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            employee_id = int(self.table.item(selected_row, 0).text())
            dialog = HumanResourcesEditDialog(employee_id)
            dialog.exec()
            self.load_data()

    def delete_employee(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            employee_id = int(self.table.item(selected_row, 0).text())
            HumanResources.delete_employee(employee_id)
            self.load_data()
