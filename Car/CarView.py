# CarView.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Car import Car

class CarEditDialog(QDialog):
    def __init__(self, car_id=None, view_only=False):
        super().__init__()
        self.car_id = car_id
        self.view_only = view_only
        self.init_ui()
        if car_id:
            self.load_car_details()

    def init_ui(self):
        self.setWindowTitle("Chi tiết xe" if self.view_only else "Sửa xe")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.produced_year_input = QLineEdit()
        self.color_input = QLineEdit()
        self.car_type_input = QLineEdit()
        self.fuel_capacity_input = QLineEdit()
        self.material_consumption_input = QLineEdit()
        self.seat_num_input = QLineEdit()
        self.engine_input = QLineEdit()
        self.price_input = QLineEdit()
        self.vin_input = QLineEdit()
        self.warranty_year_input = QLineEdit()
        self.status_input = QLineEdit()

        form_layout.addRow("Tên xe:", self.name_input)
        form_layout.addRow("Năm sản xuất:", self.produced_year_input)
        form_layout.addRow("Màu:", self.color_input)
        form_layout.addRow("Loại xe:", self.car_type_input)
        form_layout.addRow("Dung tích nhiên liệu:", self.fuel_capacity_input)
        form_layout.addRow("Mức tiêu thụ nhiên liệu:", self.material_consumption_input)
        form_layout.addRow("Số ghế:", self.seat_num_input)
        form_layout.addRow("Động cơ:", self.engine_input)
        form_layout.addRow("Giá:", self.price_input)
        form_layout.addRow("VIN:", self.vin_input)
        form_layout.addRow("Năm bảo hành:", self.warranty_year_input)
        form_layout.addRow("Trạng thái:", self.status_input)

        layout.addLayout(form_layout)

        if not self.view_only:
            self.save_button = QPushButton("Lưu")
            self.save_button.clicked.connect(self.save_car)
            layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_car_details(self):
        car = Car.get_car_details(self.car_id)
        if car:
            self.name_input.setText(car[0])
            self.produced_year_input.setText(str(car[1]))
            self.color_input.setText(car[2])
            self.car_type_input.setText(car[3])
            self.fuel_capacity_input.setText(str(car[4]))
            self.material_consumption_input.setText(str(car[5]))
            self.seat_num_input.setText(str(car[6]))
            self.engine_input.setText(car[7])
            self.price_input.setText(str(car[8]))
            self.vin_input.setText(car[9])
            self.warranty_year_input.setText(str(car[10]))
            self.status_input.setText(car[11])
            if self.view_only:
                self.disable_inputs()

    def disable_inputs(self):
        self.name_input.setReadOnly(True)
        self.produced_year_input.setReadOnly(True)
        self.color_input.setReadOnly(True)
        self.car_type_input.setReadOnly(True)
        self.fuel_capacity_input.setReadOnly(True)
        self.material_consumption_input.setReadOnly(True)
        self.seat_num_input.setReadOnly(True)
        self.engine_input.setReadOnly(True)
        self.price_input.setReadOnly(True)
        self.vin_input.setReadOnly(True)
        self.warranty_year_input.setReadOnly(True)
        self.status_input.setReadOnly(True)

    def save_car(self):
        name = self.name_input.text()
        produced_year = int(self.produced_year_input.text())
        color = self.color_input.text()
        car_type = self.car_type_input.text()
        fuel_capacity = float(self.fuel_capacity_input.text())
        material_consumption = float(self.material_consumption_input.text())
        seat_num = int(self.seat_num_input.text())
        engine = self.engine_input.text()
        price = float(self.price_input.text())
        vin = self.vin_input.text()
        warranty_year = int(self.warranty_year_input.text())
        status = self.status_input.text()

        Car.update_car(self.car_id, name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status)
        self.accept()
