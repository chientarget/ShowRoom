# dealer_list.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QMessageBox
from Dealer.dealer import Dealer
from Dealer.dealer_forms import DealerForm

class DealerListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_dealers()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.dealer_list = QListWidget()
        self.layout.addWidget(self.dealer_list)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Dealer")
        self.edit_button = QPushButton("Edit Dealer")
        self.delete_button = QPushButton("Delete Dealer")
        self.view_button = QPushButton("View Details")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.view_button)

        self.layout.addLayout(self.button_layout)

        self.add_button.clicked.connect(self.add_dealer)
        self.edit_button.clicked.connect(self.edit_dealer)
        self.delete_button.clicked.connect(self.delete_dealer)
        self.view_button.clicked.connect(self.view_dealer_details)

        self.setLayout(self.layout)

    def load_dealers(self):
        self.dealer_list.clear()
        dealers = Dealer.get_dealers()
        for dealer in dealers:
            self.dealer_list.addItem(f"{dealer.id} - {dealer}")

    def add_dealer(self):
        form = DealerForm()
        if form.exec():
            data = form.get_dealer_data()
            dealer = Dealer(**data)
            dealer.add_dealer()
            self.load_dealers()

    def edit_dealer(self):
        selected_item = self.dealer_list.currentItem()
        if selected_item:
            dealer_id = int(selected_item.text().split(" - ")[0])
            dealer = Dealer.get_dealer_details(dealer_id)
            form = DealerForm(dealer)
            if form.exec():
                data = form.get_dealer_data()
                dealer.name = data["name"]
                dealer.address = data["address"]
                dealer.phone = data["phone"]
                dealer.email = data["email"]
                dealer.update_dealer()
                self.load_dealers()

    def delete_dealer(self):
        selected_item = self.dealer_list.currentItem()
        if selected_item:
            dealer_id = int(selected_item.text().split(" - ")[0])
            Dealer.delete_dealer(dealer_id)
            self.load_dealers()

    def view_dealer_details(self):
        selected_item = self.dealer_list.currentItem()
        if selected_item:
            dealer_id = int(selected_item.text().split(" - ")[0])
            dealer = Dealer.get_dealer_details(dealer_id)
            QMessageBox.information(self, "Dealer Details", f"Name: {dealer.name}\nAddress: {dealer.address}\nPhone: {dealer.phone}\nEmail: {dealer.email}")
