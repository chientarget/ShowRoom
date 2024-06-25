# CustomerView.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Customer import Customer

class CustomerEditDialog(QDialog):
    def __init__(self, customer_id=None, view_only=False):
        super().__init__()
        self.customer_id = customer_id
        self.view_only = view_only
        self.init_ui()
        if customer_id:
            self.load_customer_details()

    def init_ui(self):
        self.setWindowTitle("Chi tiết khách hàng" if self.view_only else "Sửa khách hàng")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.date_of_birth_input = QLineEdit()
        self.customer_type_input = QLineEdit()

        form_layout.addRow("Tên:", self.name_input)
        form_layout.addRow("Số điện thoại:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Địa chỉ:", self.address_input)
        form_layout.addRow("Giới tính:", self.gender_input)
        form_layout.addRow("Ngày sinh:", self.date_of_birth_input)
        form_layout.addRow("Loại khách hàng:", self.customer_type_input)

        layout.addLayout(form_layout)

        if not self.view_only:
            self.save_button = QPushButton("Lưu")
            self.save_button.clicked.connect(self.save_customer)
            layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_customer_details(self):
        customer = Customer.get_customer_details(self.customer_id)
        if customer:
            self.name_input.setText(customer[0])
            self.phone_input.setText(customer[1])
            self.email_input.setText(customer[2])
            self.address_input.setText(customer[3])
            self.gender_input.setText(customer[4])
            self.date_of_birth_input.setText(customer[5])
            self.customer_type_input.setText(customer[6])
            if self.view_only:
                self.disable_inputs()

    def disable_inputs(self):
        self.name_input.setReadOnly(True)
        self.phone_input.setReadOnly(True)
        self.email_input.setReadOnly(True)
        self.address_input.setReadOnly(True)
        self.gender_input.setReadOnly(True)
        self.date_of_birth_input.setReadOnly(True)
        self.customer_type_input.setReadOnly(True)

    def save_customer(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        gender = self.gender_input.text()
        date_of_birth = self.date_of_birth_input.text()
        customer_type = self.customer_type_input.text()

        Customer.update_customer(self.customer_id, name, phone, email, address, gender, date_of_birth, customer_type)
        self.accept()
