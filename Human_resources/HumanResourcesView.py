# HumanResourcesView.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from HumanResources import HumanResources

class HumanResourcesEditDialog(QDialog):
    def __init__(self, employee_id=None, view_only=False):
        super().__init__()
        self.employee_id = employee_id
        self.view_only = view_only
        self.init_ui()
        if employee_id:
            self.load_employee_details()

    def init_ui(self):
        self.setWindowTitle("Chi tiết nhân viên" if self.view_only else "Sửa nhân viên")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.date_of_birth_input = QLineEdit()
        self.position_input = QLineEdit()
        self.department_input = QLineEdit()

        form_layout.addRow("Tên:", self.name_input)
        form_layout.addRow("Số điện thoại:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Địa chỉ:", self.address_input)
        form_layout.addRow("Giới tính:", self.gender_input)
        form_layout.addRow("Ngày sinh:", self.date_of_birth_input)
        form_layout.addRow("Vị trí:", self.position_input)
        form_layout.addRow("Phòng ban:", self.department_input)

        layout.addLayout(form_layout)

        if not self.view_only:
            self.save_button = QPushButton("Lưu")
            self.save_button.clicked.connect(self.save_employee)
            layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_employee_details(self):
        employee = HumanResources.get_employee_details(self.employee_id)
        if employee:
            self.name_input.setText(employee[0])
            self.phone_input.setText(employee[1])
            self.email_input.setText(employee[2])
            self.address_input.setText(employee[3])
            self.gender_input.setText(employee[4])
            self.date_of_birth_input.setText(employee[5])
            self.position_input.setText(employee[6])
            self.department_input.setText(employee[7])
            if self.view_only:
                self.disable_inputs()

    def disable_inputs(self):
        self.name_input.setReadOnly(True)
        self.phone_input.setReadOnly(True)
        self.email_input.setReadOnly(True)
        self.address_input.setReadOnly(True)
        self.gender_input.setReadOnly(True)
        self.date_of_birth_input.setReadOnly(True)
        self.position_input.setReadOnly(True)
        self.department_input.setReadOnly(True)

    def save_employee(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        gender = self.gender_input.text()
        date_of_birth = self.date_of_birth_input.text()
        position = self.position_input.text()
        department = self.department_input.text()

        HumanResources.update_employee(self.employee_id, name, phone, email, address, gender, date_of_birth, position, department)
        self.accept()
