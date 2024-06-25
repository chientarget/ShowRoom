# OrderView.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Order import Order

class OrderEditDialog(QDialog):
    def __init__(self, order_id=None, view_only=False):
        super().__init__()
        self.order_id = order_id
        self.view_only = view_only
        self.init_ui()
        if order_id:
            self.load_order_details()

    def init_ui(self):
        self.setWindowTitle("Chi tiết đơn hàng" if self.view_only else "Sửa đơn hàng")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.customer_id_input = QLineEdit()
        self.total_price_input = QLineEdit()
        self.car_id_input = QLineEdit()
        self.human_resource_id_input = QLineEdit()
        self.dealer_id_input = QLineEdit()

        form_layout.addRow("Khách hàng:", self.customer_id_input)
        form_layout.addRow("Tổng giá:", self.total_price_input)
        form_layout.addRow("Xe:", self.car_id_input)
        form_layout.addRow("Nhân viên bán hàng:", self.human_resource_id_input)
        form_layout.addRow("Đại lý:", self.dealer_id_input)

        layout.addLayout(form_layout)

        if not self.view_only:
            self.save_button = QPushButton("Lưu")
            self.save_button.clicked.connect(self.save_order)
            layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_order_details(self):
        order = Order.get_order_details(self.order_id)
        if order:
            self.customer_id_input.setText(str(order[0]))
            self.total_price_input.setText(str(order[1]))
            self.car_id_input.setText(str(order[2]))
            self.human_resource_id_input.setText(str(order[3]))
            self.dealer_id_input.setText(str(order[4]))
            if self.view_only:
                self.disable_inputs()

    def disable_inputs(self):
        self.customer_id_input.setReadOnly(True)
        self.total_price_input.setReadOnly(True)
        self.car_id_input.setReadOnly(True)
        self.human_resource_id_input.setReadOnly(True)
        self.dealer_id_input.setReadOnly(True)

    def save_order(self):
        customer_id = self.customer_id_input.text()
        total_price = self.total_price_input.text()
        car_id = self.car_id_input.text()
        human_resource_id = self.human_resource_id_input.text()
        dealer_id = self.dealer_id_input.text()

        Order.update_order(self.order_id, customer_id, total_price, car_id, human_resource_id, dealer_id)
        self.accept()
