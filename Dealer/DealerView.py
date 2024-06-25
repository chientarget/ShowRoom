# DealerView.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Dealer import Dealer

class DealerEditDialog(QDialog):
    def __init__(self, dealer_id=None, view_only=False):
        super().__init__()
        self.dealer_id = dealer_id
        self.view_only = view_only
        self.init_ui()
        if dealer_id:
            self.load_dealer_details()

    def init_ui(self):
        self.setWindowTitle("Chi tiết đại lý" if self.view_only else "Sửa đại lý")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.address_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        form_layout.addRow("Tên đại lý:", self.name_input)
        form_layout.addRow("Địa chỉ:", self.address_input)
        form_layout.addRow("Số điện thoại:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)

        layout.addLayout(form_layout)

        if not self.view_only:
            self.save_button = QPushButton("Lưu")
            self.save_button.clicked.connect(self.save_dealer)
            layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_dealer_details(self):
        dealer = Dealer.get_dealer_details(self.dealer_id)
        if dealer:
            self.name_input.setText(dealer[0])
            self.address_input.setText(dealer[1])
            self.phone_input.setText(dealer[2])
            self.email_input.setText(dealer[3])
            if self.view_only:
                self.disable_inputs()

    def disable_inputs(self):
        self.name_input.setReadOnly(True)
        self.address_input.setReadOnly(True)
        self.phone_input.setReadOnly(True)
        self.email_input.setReadOnly(True)

    def save_dealer(self):
        name = self.name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        Dealer.update_dealer(self.dealer_id, name, address, phone, email)
        self.accept()
