from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from database import add_order, update_order

class OrderEditDialog(QDialog):
    def __init__(self, order=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm / Sửa Đơn Hàng")
        self.order = order

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.customer_id_input = QLineEdit(self)
        self.total_price_input = QLineEdit(self)
        self.car_id_input = QLineEdit(self)
        self.human_resource_id_input = QLineEdit(self)
        self.dealer_id_input = QLineEdit(self)

        self.form_layout.addRow("Customer ID:", self.customer_id_input)
        self.form_layout.addRow("Total Price:", self.total_price_input)
        self.form_layout.addRow("Car ID:", self.car_id_input)
        self.form_layout.addRow("Human Resources ID:", self.human_resource_id_input)
        self.form_layout.addRow("Dealer ID:", self.dealer_id_input)

        self.save_button = QPushButton("Lưu", self)
        self.save_button.clicked.connect(self.save_order)
        self.layout.addWidget(self.save_button)

        if self.order:
            self.customer_id_input.setText(str(self.order[1]))
            self.total_price_input.setText(str(self.order[2]))
            self.car_id_input.setText(str(self.order[3]))
            self.human_resource_id_input.setText(str(self.order[4]))
            self.dealer_id_input.setText(str(self.order[5]))

    def save_order(self):
        customer_id = int(self.customer_id_input.text())
        total_price = int(self.total_price_input.text())
        car_id = int(self.car_id_input.text())
        human_resource_id = int(self.human_resource_id_input.text())
        dealer_id = int(self.dealer_id_input.text())

        if self.order:
            order_id = self.order[0]
            update_order(order_id, customer_id, total_price, car_id, human_resource_id, dealer_id)
        else:
            add_order(customer_id, total_price, car_id, human_resource_id, dealer_id)

        self.accept()
