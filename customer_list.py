from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class CustomerList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Danh sách khách hàng')
        layout.addWidget(label)
        self.setLayout(layout)
