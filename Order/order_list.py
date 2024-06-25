# order_list.py
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from Order.order import Order
from Order.order_forms import OrderEditDialog, OrderInfoDialog, OrderAddDialog

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info_icon_path = os.path.join(base_dir, "img", "img_crud", "info.svg")
edit_icon_path = os.path.join(base_dir, "img", "img_crud", "edit.svg")
delete_icon_path = os.path.join(base_dir, "img", "img_crud", "delete.svg")

class OrderListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("Danh sách đơn hàng")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        layout.addWidget(header)

        self.button_layout = QHBoxLayout()
        self.add_order_button = QPushButton("+   Thêm đơn hàng")
        self.add_order_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_order_button.setFixedSize(150, 40)
        self.add_order_button.clicked.connect(self.add_order)
        self.add_order_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        self.button_layout.addWidget(self.add_order_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(self.button_layout)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(9)  # Add 3 columns for the buttons
        self.order_table.setHorizontalHeaderLabels(["Order ID", "Customer ID", "Total Price", "Car ID", "Human Resources", "Dealer ID", "", "", ""])
        self.order_table.verticalHeader().setVisible(False)
        self.order_table.horizontalHeader().setStretchLastSection(True)
        self.order_table.setAlternatingRowColors(True)
        self.order_table.setStyleSheet("""
            QHeaderView::section { background-color: #09AD90; color: white; font-size: 16px;  font-weight: bold; font-family: Roboto;}
            QTableWidget::item { font-size: 30px; font-family: Roboto; }
        """)
        layout.addWidget(self.order_table)

        self.setLayout(layout)
        self.load_orders()

    def load_orders(self):
        self.order_table.setRowCount(0)
        orders = Order.get_all_orders()

        for order in orders:
            row_position = self.order_table.rowCount()
            self.order_table.insertRow(row_position)
            self.order_table.setItem(row_position, 0, QTableWidgetItem(str(order.id)))
            self.order_table.setItem(row_position, 1, QTableWidgetItem(str(order.customer_id)))
            self.order_table.setItem(row_position, 2, QTableWidgetItem(str(order.total_price)))
            self.order_table.setItem(row_position, 3, QTableWidgetItem(str(order.car_id)))
            self.order_table.setItem(row_position, 4, QTableWidgetItem(str(order.human_resource_id)))
            self.order_table.setItem(row_position, 5, QTableWidgetItem(str(order.dealer_id)))

            # Add buttons for details, edit, delete with icons
            info_button = QPushButton()
            info_button.setIcon(QIcon(info_icon_path))
            info_button.setStyleSheet("background-color: transparent;")
            info_button.clicked.connect(lambda _, order_id=order.id: self.show_order_info(order_id))
            self.order_table.setCellWidget(row_position, 6, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.clicked.connect(lambda _, order_id=order.id: self.edit_order(order_id))
            self.order_table.setCellWidget(row_position, 7, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.clicked.connect(lambda _, order_id=order.id: self.delete_order(order_id))
            self.order_table.setCellWidget(row_position, 8, delete_button)

        self.order_table.resizeColumnsToContents()

    def add_order(self):
        dialog = OrderAddDialog(self)
        if dialog.exec():
            self.load_orders()

    def delete_order(self, order_id):
        Order.delete(order_id)
        QMessageBox.information(self, "Deleted", f"Order ID '{order_id}' has been deleted.")
        self.load_orders()

    def show_order_info(self, order_id):
        dialog = OrderInfoDialog(order_id, self)
        dialog.exec()

    def edit_order(self, order_id):
        dialog = OrderEditDialog(order_id, self)
        if dialog.exec():
            self.load_orders()
