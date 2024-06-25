# CustomerGUI.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Customer import Customer
from CustomerView import CustomerEditDialog

class CustomerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Quản lý khách hàng")
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên", "Số điện thoại", "Email", "Địa chỉ", "Giới tính", "Ngày sinh", "Loại khách hàng"
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
        self.view_button.clicked.connect(self.view_customer)
        self.edit_button.clicked.connect(self.edit_customer)
        self.delete_button.clicked.connect(self.delete_customer)

    def load_data(self):
        customers = Customer.get_all_customers()
        self.table.setRowCount(len(customers))
        for row_idx, customer in enumerate(customers):
            for col_idx, value in enumerate(customer):
                item = QTableWidgetItem(str(value))
                if col_idx == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def view_customer(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            customer_id = int(self.table.item(selected_row, 0).text())
            dialog = CustomerEditDialog(customer_id, view_only=True)
            dialog.exec()

    def edit_customer(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            customer_id = int(self.table.item(selected_row, 0).text())
            dialog = CustomerEditDialog(customer_id)
            dialog.exec()
            self.load_data()

    def delete_customer(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            customer_id = int(self.table.item(selected_row, 0).text())
            Customer.delete_customer(customer_id)
            self.load_data()
