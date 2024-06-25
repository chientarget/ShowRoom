# order_forms.py
from PyQt6.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QDialogButtonBox, QComboBox
from Order.order import Order

class OrderEditDialog(QDialog):
    def __init__(self, order_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin đơn hàng")
        self.order_id = order_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        order = Order.get_order_by_id(self.order_id)

        self.customer_id_edit = QLineEdit(str(order.customer_id))
        self.total_price_edit = QLineEdit(str(order.total_price))
        self.car_id_edit = QLineEdit(str(order.car_id))
        self.human_resource_id_edit = QLineEdit(str(order.human_resource_id))
        self.dealer_id_edit = QLineEdit(str(order.dealer_id))

        layout.addWidget(QLabel("Customer ID:"), 0, 0)
        layout.addWidget(self.customer_id_edit, 0, 1)

        layout.addWidget(QLabel("Total Price:"), 1, 0)
        layout.addWidget(self.total_price_edit, 1, 1)

        layout.addWidget(QLabel("Car ID:"), 2, 0)
        layout.addWidget(self.car_id_edit, 2, 1)

        layout.addWidget(QLabel("Human_resources ID:"), 3, 0)
        layout.addWidget(self.human_resource_id_edit, 3, 1)

        layout.addWidget(QLabel("Dealer ID:"), 4, 0)
        layout.addWidget(self.dealer_id_edit, 4, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 5, 0, 1, 2)

    def accept(self):
        order = Order(
            self.order_id,
            int(self.customer_id_edit.text()),
            float(self.total_price_edit.text()),
            int(self.car_id_edit.text()),
            int(self.human_resource_id_edit.text()),
            int(self.dealer_id_edit.text())
        )
        order.update()
        super().accept()

class OrderInfoDialog(QDialog):
    def __init__(self, order_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin đơn hàng")
        self.order_id = order_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        order = Order.get_order_by_id(self.order_id)

        layout.addWidget(QLabel("Customer ID:"), 0, 0)
        layout.addWidget(QLabel(str(order.customer_id)), 0, 1)

        layout.addWidget(QLabel("Total Price:"), 1, 0)
        layout.addWidget(QLabel(str(order.total_price)), 1, 1)

        layout.addWidget(QLabel("Car ID:"), 2, 0)
        layout.addWidget(QLabel(str(order.car_id)), 2, 1)

        layout.addWidget(QLabel("Human_resources ID:"), 3, 0)
        layout.addWidget(QLabel(str(order.human_resource_id)), 3, 1)

        layout.addWidget(QLabel("Dealer ID:"), 4, 0)
        layout.addWidget(QLabel(str(order.dealer_id)), 4, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        layout.addWidget(self.button_box, 5, 0, 1, 2)

class OrderAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm đơn hàng mới")
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        self.customer_id_edit = QLineEdit()
        self.total_price_edit = QLineEdit()
        self.car_id_edit = QLineEdit()
        self.human_resource_id_edit = QLineEdit()
        self.dealer_id_edit = QLineEdit()

        layout.addWidget(QLabel("Customer ID:"), 0, 0)
        layout.addWidget(self.customer_id_edit, 0, 1)

        layout.addWidget(QLabel("Total Price:"), 1, 0)
        layout.addWidget(self.total_price_edit, 1, 1)

        layout.addWidget(QLabel("Car ID:"), 2, 0)
        layout.addWidget(self.car_id_edit, 2, 1)

        layout.addWidget(QLabel("Human_resources ID:"), 3, 0)
        layout.addWidget(self.human_resource_id_edit, 3, 1)

        layout.addWidget(QLabel("Dealer ID:"), 4, 0)
        layout.addWidget(self.dealer_id_edit, 4, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 5, 0, 1, 2)

    def accept(self):
        order = Order(
            None,
            int(self.customer_id_edit.text()),
            float(self.total_price_edit.text()),
            int(self.car_id_edit.text()),
            int(self.human_resource_id_edit.text()),
            int(self.dealer_id_edit.text())
        )
        order.save()
        super().accept()
