from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PartnerList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Hãng xe đối tác')
        layout.addWidget(label)
        self.setLayout(layout)
