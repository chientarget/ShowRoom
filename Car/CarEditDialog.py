# CarEditDialog.py
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox
from car import Car

class CarEditDialog(QDialog):
    def __init__(self, car_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin xe")
        self.car_id = car_id
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        car = Car.get_car_by_id(self.car_id)

        self.name_edit = QLineEdit(car.name)
        self.produced_year_edit = QLineEdit(str(car.produced_year))
        self.color_edit = QLineEdit(car.color)
        self.car_type_edit = QLineEdit(car.car_type)
        self.warranty_year_edit = QLineEdit(car.warranty_year)
        self.price_edit = QLineEdit(car.price)
        self.status_edit = QLineEdit(car.status)

        layout.addRow("Tên xe:", self.name_edit)
        layout.addRow("Năm sản xuất:", self.produced_year_edit)
        layout.addRow("Màu sắc:", self.color_edit)
        layout.addRow("Loại xe:", self.car_type_edit)
        layout.addRow("Bảo hành:", self.warranty_year_edit)
        layout.addRow("Giá:", self.price_edit)
        layout.addRow("Trạng thái:", self.status_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def accept(self):
        car = Car(
            self.car_id,
            self.name_edit.text(),
            int(self.produced_year_edit.text()),
            self.color_edit.text(),
            self.car_type_edit.text(),
            self.warranty_year_edit.text(),
            self.price_edit.text(),
            self.status_edit.text()
        )
        car.update()
        super().accept()
