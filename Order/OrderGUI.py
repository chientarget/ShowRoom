# OrderGUI.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Order import Order
from OrderView import OrderEditDialog

class OrderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Quản lý đơn hàng")
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Khách hàng", "Tổng giá", "Xe", "Nhân viên bán hàng", "Đại lý"
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
        self.view_button.clicked.connect(self.view_order)
        self.edit_button.clicked.connect(self.edit_order)
        self.delete_button.clicked.connect(self.delete_order)

    def load_data(self):
        orders = Order.get_all_orders()
        self.table.setRowCount(len(orders))
        for row_idx, order in enumerate(orders):
            for col_idx, value in enumerate(order):
                item = QTableWidgetItem(str(value))
                if col_idx == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def view_order(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            order_id = int(self.table.item(selected_row, 0).text())
            dialog = OrderEditDialog(order_id, view_only=True)
            dialog.exec()

    def edit_order(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            order_id = int(self.table.item(selected_row, 0).text())
            dialog = OrderEditDialog(order_id)
            dialog.exec()
            self.load_data()

    def delete_order(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            order_id = int(self.table.item(selected_row, 0).text())
            Order.delete_order(order_id)
            self.load_data()
