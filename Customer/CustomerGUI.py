import os
from PyQt6.QtWidgets import*
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from Customer.Customer import Customer

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info_icon_path = os.path.join(base_dir, "img", "img_crud", "info.svg")
edit_icon_path = os.path.join(base_dir, "img", "img_crud", "edit.svg")
delete_icon_path = os.path.join(base_dir, "img", "img_crud", "delete.svg")


class CustomerGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sort_order = Qt.SortOrder.DescendingOrder
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("Danh sách khách hàng")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        layout.addWidget(header)

        search_layout = QHBoxLayout()

        self.search_name_edit = QLineEdit()
        self.search_name_edit.setPlaceholderText("Tìm theo tên")
        self.search_name_edit.setFixedWidth(180)
        self.search_name_edit.textChanged.connect(self.load_customers)
        search_layout.addWidget(self.search_name_edit)

        self.search_address_edit = QLineEdit()
        self.search_address_edit.setPlaceholderText("Tìm theo địa chỉ")
        self.search_address_edit.setFixedWidth(180)
        self.search_address_edit.textChanged.connect(self.load_customers)
        search_layout.addWidget(self.search_address_edit)

        self.search_phone_edit = QLineEdit()
        self.search_phone_edit.setPlaceholderText("Tìm theo điện thoại")
        self.search_phone_edit.setFixedWidth(180)
        self.search_phone_edit.textChanged.connect(self.load_customers)
        search_layout.addWidget(self.search_phone_edit)

        self.search_email_edit = QLineEdit()
        self.search_email_edit.setPlaceholderText("Tìm theo email")
        self.search_email_edit.setFixedWidth(180)
        self.search_email_edit.textChanged.connect(self.load_customers)
        search_layout.addWidget(self.search_email_edit)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.sort_button = QPushButton("Sắp xếp")
        self.sort_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.sort_button.setFixedHeight(50)
        self.sort_button.clicked.connect(self.sort_customers)
        self.sort_button.setStyleSheet("padding: 10px 20px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 18px;")
        button_layout.addWidget(self.sort_button , alignment=Qt.AlignmentFlag.AlignRight)

        self.add_customer_button = QPushButton("+ Thêm khách hàng")
        self.add_customer_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_customer_button.setFixedHeight(50)
        self.add_customer_button.clicked.connect(self.add_customer)
        self.add_customer_button.setStyleSheet("padding: 10px 20px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 18px;")
        button_layout.addWidget(self.add_customer_button , alignment=Qt.AlignmentFlag.AlignRight)

        search_layout.addLayout(button_layout)
        layout.addLayout(search_layout)

        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(9)  # Update to include new columns
        self.customer_table.setHorizontalHeaderLabels(["ID khách hàng", "Tên", "Địa chỉ", "Điện thoại", "Email", "Số lượng xe đã mua", "Tổng giá trị mua hàng", "Chỉnh sửa", "Xóa"])
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
        customers = Customer.get_all_customers_with_total_purchase()

        search_name = self.search_name_edit.text().lower()
        search_address = self.search_address_edit.text().lower()
        search_phone = self.search_phone_edit.text().lower()
        search_email = self.search_email_edit.text().lower()

        for customer in customers:
            if (search_name and search_name not in customer[1].lower()) or \
                    (search_address and search_address not in customer[2].lower()) or \
                    (search_phone and search_phone not in customer[3].lower()) or \
                    (search_email and search_email not in customer[4].lower()):
                continue

            row_position = self.customer_table.rowCount()
            self.customer_table.insertRow(row_position)
            id_item = QTableWidgetItem(str(customer[0]))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.customer_table.setItem(row_position, 0, id_item)

            self.customer_table.setItem(row_position, 1, QTableWidgetItem(customer[1]))
            self.customer_table.setItem(row_position, 2, QTableWidgetItem(customer[2]))
            self.customer_table.setItem(row_position, 3, QTableWidgetItem(customer[3]))
            self.customer_table.setItem(row_position, 4, QTableWidgetItem(customer[4]))

            purchased_item = QTableWidgetItem(str(Customer.get_purchased_car_count(customer[0])))
            purchased_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.customer_table.setItem(row_position, 5, purchased_item)

            total_purchase_item = QTableWidgetItem(f"{customer[5]:,}")
            total_purchase_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.customer_table.setItem(row_position, 6, total_purchase_item)

            # Add buttons for details, edit, delete with icons
            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setMinimumWidth(50)
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.clicked.connect(lambda _, customer_id=customer[0]: self.edit_customer(customer_id))
            self.customer_table.setCellWidget(row_position, 7, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setMinimumWidth(50)
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.clicked.connect(lambda _, customer_id=customer[0]: self.delete_customer(customer_id))
            self.customer_table.setCellWidget(row_position, 8, delete_button)

        self.customer_table.resizeColumnsToContents()

    def sort_customers(self):
        self.sort_order = Qt.SortOrder.AscendingOrder if self.sort_order == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder
        self.customer_table.sortItems(6, self.sort_order)

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


class CustomerEditDialog(QDialog):
    def __init__(self, customer_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin khách hàng")
        self.customer_id = customer_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        customer = Customer.get_customer_by_id(self.customer_id)

        self.name_edit = QLineEdit(customer.name)
        self.address_edit = QLineEdit(customer.address)
        self.phone_edit = QLineEdit(customer.phone)
        self.email_edit = QLineEdit(customer.email)

        layout.addWidget(QLabel("Tên khách hàng:"), 0, 0)
        layout.addWidget(self.name_edit, 0, 1)
        layout.addWidget(QLabel("Địa chỉ:"), 1, 0)
        layout.addWidget(self.address_edit, 1, 1)
        layout.addWidget(QLabel("Số điện thoại:"), 2, 0)
        layout.addWidget(self.phone_edit, 2, 1)
        layout.addWidget(QLabel("Email:"), 3, 0)
        layout.addWidget(self.email_edit, 3, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        save_button = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box, 4, 0, 1, 2)

    def accept(self):
        customer = Customer(
            self.customer_id,
            self.name_edit.text(),
            self.address_edit.text(),
            self.phone_edit.text(),
            self.email_edit.text()
        )
        customer.update()
        super().accept()

class CustomerInfoDialog(QDialog):
    def __init__(self, customer_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin khách hàng")
        self.customer_id = customer_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        customer = Customer.get_customer_by_id(self.customer_id)

        layout.addWidget(QLabel("Tên khách hàng:"), 0, 0)
        layout.addWidget(QLabel(customer.name), 0, 1)
        layout.addWidget(QLabel("Địa chỉ:"), 1, 0)
        layout.addWidget(QLabel(customer.address), 1, 1)
        layout.addWidget(QLabel("Số điện thoại:"), 2, 0)
        layout.addWidget(QLabel(customer.phone), 2, 1)
        layout.addWidget(QLabel("Email:"), 3, 0)
        layout.addWidget(QLabel(customer.email), 3, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")

        layout.addWidget(self.button_box, 4, 0, 1, 2)

class CustomerAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm khách hàng mới")
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        self.name_edit = QLineEdit()
        self.address_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()

        layout.addWidget(QLabel("Tên khách hàng:"), 0, 0)
        layout.addWidget(self.name_edit, 0, 1)
        layout.addWidget(QLabel("Địa chỉ:"), 1, 0)
        layout.addWidget(self.address_edit, 1, 1)
        layout.addWidget(QLabel("Số điện thoại:"), 2, 0)
        layout.addWidget(self.phone_edit, 2, 1)
        layout.addWidget(QLabel("Email:"), 3, 0)
        layout.addWidget(self.email_edit, 3, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        save_button = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box, 4, 0, 1, 2)

    def accept(self):
        customer = Customer(
            None,
            self.name_edit.text(),
            self.address_edit.text(),
            self.phone_edit.text(),
            self.email_edit.text()
        )
        customer.save()
        super().accept()
