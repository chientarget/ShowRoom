from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class EmployeeList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Danh sách nhân viên')
        layout.addWidget(label)
        self.setLayout(layout)
