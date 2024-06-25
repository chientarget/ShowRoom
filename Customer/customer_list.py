# customer_list.py
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from Customer.customer import Customer
from Customer.customer_forms import CustomerEditDialog, CustomerInfoDialog, CustomerAddDialog

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info_icon_path = os.path.join(base_dir, "img", "img_crud", "info.svg")
edit_icon_path = os.path.join(base_dir, "img", "img_crud", "edit.svg")
delete_icon_path = os.path.join(base_dir, "img", "img_crud", "delete.svg")

class CustomerListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("Danh sách khách hàng")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        layout.addWidget(header)

        self.button_layout = QHBoxLayout()
        self.add_customer_button = QPushButton("+   Thêm khách hàng")
        self.add_customer_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_customer_button.setFixedSize(150, 40)
        self.add_customer_button.clicked.connect(self.add_customer)
        self.add_customer_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        self.button_layout.addWidget(self.add_customer_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(self.button_layout)

        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(7)  # Add 3 columns for the buttons
        self.customer_table.setHorizontalHeaderLabels(["Customer ID", "Name", "Address", "Phone", "Email", "", "", ""])
        self.customer_table.verticalHeader().setVisible(False)
        self.customer_table.horizontalHeader().setStretchLastSection(True)
        self.customer_table.setAlternatingRowColors(True)
        self.customer_table.setStyleSheet("""
            QHeaderView::section { background-color: #09AD90; color: white; font-size: 16px;  font-weight: bold; font-family: Roboto;}
            QTableWidget::item { font-size: 30px; font-family: Roboto; }
        """)
        layout.addWidget(self.customer_table)

        self.setLayout(layout)
        self.load_customers()

    def load_customers(self):
        self.customer_table.setRowCount(0)
        customers = Customer.get_all_customers()

        for customer in customers:
            row_position = self.customer_table.rowCount()
            self.customer_table.insertRow(row_position)
            self.customer_table.setItem(row_position, 0, QTableWidgetItem(str(customer.id)))
            self.customer_table.setItem(row_position, 1, QTableWidgetItem(customer.name))
            self.customer_table.setItem(row_position, 2, QTableWidgetItem(customer.address))
            self.customer_table.setItem(row_position, 3, QTableWidgetItem(customer.phone))
            self.customer_table.setItem(row_position, 4, QTableWidgetItem(customer.email))

            # Add buttons for details, edit, delete with icons
            info_button = QPushButton()
            info_button.setIcon(QIcon(info_icon_path))
            info_button.setStyleSheet("background-color: transparent;")
            info_button.clicked.connect(lambda _, customer_id=customer.id: self.show_customer_info(customer_id))
            self.customer_table.setCellWidget(row_position, 5, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.clicked.connect(lambda _, customer_id=customer.id: self.edit_customer(customer_id))
            self.customer_table.setCellWidget(row_position, 6, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.clicked.connect(lambda _, customer_id=customer.id: self.delete_customer(customer_id))
            self.customer_table.setCellWidget(row_position, 7, delete_button)

        self.customer_table.resizeColumnsToContents()

    def add_customer(self):
        dialog = CustomerAddDialog(self)
        if dialog.exec():
            self.load_customers()

    def delete_customer(self, customer_id):
        Customer.delete(customer_id)
        QMessageBox.information(self, "Deleted", f"Customer ID '{customer_id}' has been deleted.")
        self.load_customers()

    def show_customer_info(self, customer_id):
        dialog = CustomerInfoDialog(customer_id, self)
        dialog.exec()

    def edit_customer(self, customer_id):
        dialog = CustomerEditDialog(customer_id, self)
        if dialog.exec():
            self.load_customers()
