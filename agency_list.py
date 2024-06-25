from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class AgencyList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Danh sách đại lý')
        layout.addWidget(label)
        self.setLayout(layout)
