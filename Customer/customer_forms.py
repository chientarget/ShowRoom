# customer_forms.py
from PyQt6.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QDialogButtonBox
from Customer.customer import Customer

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
