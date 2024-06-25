# dealer_forms.py
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QVBoxLayout, QDialogButtonBox


class DealerForm(QDialog):
    def __init__(self, dealer=None):
        super().__init__()
        self.dealer = dealer
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dealer Form")
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit(self.dealer.name if self.dealer else "")
        self.address_input = QLineEdit(self.dealer.address if self.dealer else "")
        self.phone_input = QLineEdit(self.dealer.phone if self.dealer else "")
        self.email_input = QLineEdit(self.dealer.email if self.dealer else "")

        self.form_layout.addRow("Name", self.name_input)
        self.form_layout.addRow("Address", self.address_input)
        self.form_layout.addRow("Phone", self.phone_input)
        self.form_layout.addRow("Email", self.email_input)

        self.layout.addLayout(self.form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def get_dealer_data(self):
        return {
            "name": self.name_input.text(),
            "address": self.address_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text()
        }
