# CarGUI.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Car import Car
from CarView import CarEditDialog

class CarGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Quản lý xe")
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên xe", "Năm sản xuất", "Màu", "Loại xe", "Dung tích nhiên liệu",
            "Mức tiêu thụ nhiên liệu", "Số ghế", "Động cơ", "Giá", "Năm bảo hành", "Trạng thái"
        ])
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        self.view_button = QPushButton("Xem thông tin")
        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")
        button_layout.addWidget(self.view_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Load data
        self.load_data()

        # Connect buttons
        self.view_button.clicked.connect(self.view_car)
        self.edit_button.clicked.connect(self.edit_car)
        self.delete_button.clicked.connect(self.delete_car)

    def load_data(self):
        cars = Car.get_all_cars()
        self.table.setRowCount(len(cars))
        for row_idx, car in enumerate(cars):
            for col_idx, value in enumerate(car):
                item = QTableWidgetItem(str(value))
                if col_idx == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def view_car(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            car_id = int(self.table.item(selected_row, 0).text())
            dialog = CarEditDialog(car_id, view_only=True)
            dialog.exec()

    def edit_car(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            car_id = int(self.table.item(selected_row, 0).text())
            dialog = CarEditDialog(car_id)
            dialog.exec()
            self.load_data()

    def delete_car(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            car_id = int(self.table.item(selected_row, 0).text())
            Car.delete_car(car_id)
            self.load_data()
