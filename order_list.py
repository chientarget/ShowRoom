from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class OrderList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Danh sách đơn hàng')
        layout.addWidget(label)
        self.setLayout(layout)
