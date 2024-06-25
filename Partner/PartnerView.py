# PartnerView.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Partner import Partner

class PartnerEditDialog(QDialog):
    def __init__(self, partner_id=None, view_only=False):
        super().__init__()
        self.partner_id = partner_id
        self.view_only = view_only
        self.init_ui()
        if partner_id:
            self.load_partner_details()

    def init_ui(self):
        self.setWindowTitle("Chi tiết đối tác" if self.view_only else "Sửa đối tác")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.address_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        form_layout.addRow("Tên đối tác:", self.name_input)
        form_layout.addRow("Địa chỉ:", self.address_input)
        form_layout.addRow("Số điện thoại:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)

        layout.addLayout(form_layout)

        if not self.view_only:
            self.save_button = QPushButton("Lưu")
            self.save_button.clicked.connect(self.save_partner)
            layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_partner_details(self):
        partner = Partner.get_partner_details(self.partner_id)
        if partner:
            self.name_input.setText(partner[0])
            self.address_input.setText(partner[1])
            self.phone_input.setText(partner[2])
            self.email_input.setText(partner[3])
            if self.view_only:
                self.disable_inputs()

    def disable_inputs(self):
        self.name_input.setReadOnly(True)
        self.address_input.setReadOnly(True)
        self.phone_input.setReadOnly(True)
        self.email_input.setReadOnly(True)

    def save_partner(self):
        name = self.name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        Partner.update_partner(self.partner_id, name, address, phone, email)
        self.accept()
