from PyQt6.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QDialogButtonBox, QComboBox
from database import get_car_details, update_car, add_car

class CarEditDialog(QDialog):
    def __init__(self, car_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin xe")
        self.car_id = car_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        car_details = get_car_details(self.car_id)

        self.name_edit = QLineEdit(car_details[0])
        self.produced_year_edit = QLineEdit(str(car_details[1]))
        self.color_edit = QLineEdit(car_details[2])
        self.size_edit = QLineEdit(car_details[3])
        self.fuel_capacity_edit = QLineEdit(f"{car_details[4]}L")
        self.material_consumption_edit = QLineEdit(car_details[5])
        self.seat_num_edit = QLineEdit(str(car_details[6]))
        self.engine_edit = QLineEdit(car_details[7])
        self.price_edit = QLineEdit(str(car_details[8]))
        self.vin_edit = QLineEdit(car_details[9])
        self.warranty_year_edit = QLineEdit(str(car_details[10]))
        self.status_edit = QComboBox()
        self.status_edit.addItems(["Chưa bán", "Đã bán", "Chờ mở bán"])
        self.status_edit.setCurrentText(car_details[11])

        layout.addWidget(QLabel("Tên xe:"), 0, 0)
        layout.addWidget(self.name_edit, 0, 1)
        layout.addWidget(QLabel("Năm sản xuất:"), 0, 2)
        layout.addWidget(self.produced_year_edit, 0, 3)

        layout.addWidget(QLabel("Màu sắc:"), 1, 0)
        layout.addWidget(self.color_edit, 1, 1)
        layout.addWidget(QLabel("Kích thước:"), 1, 2)
        layout.addWidget(self.size_edit, 1, 3)

        layout.addWidget(QLabel("Dung tích nhiên liệu:"), 2, 0)
        layout.addWidget(self.fuel_capacity_edit, 2, 1)
        layout.addWidget(QLabel("Tiêu thụ nhiên liệu:"), 2, 2)
        layout.addWidget(self.material_consumption_edit, 2, 3)

        layout.addWidget(QLabel("Số ghế:"), 3, 0)
        layout.addWidget(self.seat_num_edit, 3, 1)
        layout.addWidget(QLabel("Động cơ:"), 3, 2)
        layout.addWidget(self.engine_edit, 3, 3)

        layout.addWidget(QLabel("Giá:"), 4, 0)
        layout.addWidget(self.price_edit, 4, 1)
        layout.addWidget(QLabel("VIN:"), 4, 2)
        layout.addWidget(self.vin_edit, 4, 3)

        layout.addWidget(QLabel("Bảo hành:"), 5, 0)
        layout.addWidget(self.warranty_year_edit, 5, 1)
        layout.addWidget(QLabel("Trạng thái:"), 5, 2)
        layout.addWidget(self.status_edit, 5, 3)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 6, 0, 1, 4)

    def accept(self):
        update_car(
            self.car_id,
            self.name_edit.text(),
            int(self.produced_year_edit.text()),
            self.color_edit.text(),
            self.size_edit.text(),
            self.fuel_capacity_edit.text().replace('L', '').strip(),
            self.material_consumption_edit.text(),
            int(self.seat_num_edit.text()),
            self.engine_edit.text(),
            float(self.price_edit.text()),
            self.vin_edit.text(),
            int(self.warranty_year_edit.text()),
            self.status_edit.currentText()
        )
        super().accept()

class CarInfoDialog(QDialog):
    def __init__(self, car_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin xe")
        self.car_id = car_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        car_details = get_car_details(self.car_id)

        layout.addWidget(QLabel("Tên xe:"), 0, 0)
        layout.addWidget(QLabel(car_details[0]), 0, 1)
        layout.addWidget(QLabel("Năm sản xuất:"), 0, 2)
        layout.addWidget(QLabel(str(car_details[1])), 0, 3)

        layout.addWidget(QLabel("Màu sắc:"), 1, 0)
        layout.addWidget(QLabel(car_details[2]), 1, 1)
        layout.addWidget(QLabel("Kích thước:"), 1, 2)
        layout.addWidget(QLabel(car_details[3]), 1, 3)

        layout.addWidget(QLabel("Dung tích nhiên liệu:"), 2, 0)
        layout.addWidget(QLabel(f"{car_details[4]}L"), 2, 1)
        layout.addWidget(QLabel("Tiêu thụ nhiên liệu:"), 2, 2)
        layout.addWidget(QLabel(car_details[5]), 2, 3)

        layout.addWidget(QLabel("Số ghế:"), 3, 0)
        layout.addWidget(QLabel(str(car_details[6])), 3, 1)
        layout.addWidget(QLabel("Động cơ:"), 3, 2)
        layout.addWidget(QLabel(car_details[7]), 3, 3)

        layout.addWidget(QLabel("Giá:"), 4, 0)
        layout.addWidget(QLabel(str(car_details[8])), 4, 1)
        layout.addWidget(QLabel("VIN:"), 4, 2)
        layout.addWidget(QLabel(car_details[9]), 4, 3)

        layout.addWidget(QLabel("Bảo hành:"), 5, 0)
        layout.addWidget(QLabel(str(car_details[10])), 5, 1)
        layout.addWidget(QLabel("Trạng thái:"), 5, 2)
        layout.addWidget(QLabel(car_details[11]), 5, 3)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        layout.addWidget(self.button_box, 6, 0, 1, 4)

class CarAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm xe mới")
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        self.name_edit = QLineEdit()
        self.produced_year_edit = QLineEdit()
        self.color_edit = QLineEdit()
        self.size_edit = QLineEdit()
        self.fuel_capacity_edit = QLineEdit()
        self.material_consumption_edit = QLineEdit()
        self.seat_num_edit = QLineEdit()
        self.engine_edit = QLineEdit()
        self.price_edit = QLineEdit()
        self.vin_edit = QLineEdit()
        self.warranty_year_edit = QLineEdit()
        self.status_edit = QComboBox()
        self.status_edit.addItems(["Chưa bán", "Đã bán", "Chờ mở bán"])

        layout.addWidget(QLabel("Tên xe:"), 0, 0)
        layout.addWidget(self.name_edit, 0, 1)
        layout.addWidget(QLabel("Năm sản xuất:"), 0, 2)
        layout.addWidget(self.produced_year_edit, 0, 3)

        layout.addWidget(QLabel("Màu sắc:"), 1, 0)
        layout.addWidget(self.color_edit, 1, 1)
        layout.addWidget(QLabel("Kích thước:"), 1, 2)
        layout.addWidget(self.size_edit, 1, 3)

        layout.addWidget(QLabel("Dung tích nhiên liệu:"), 2, 0)
        layout.addWidget(self.fuel_capacity_edit, 2, 1)
        layout.addWidget(QLabel("Tiêu thụ nhiên liệu:"), 2, 2)
        layout.addWidget(self.material_consumption_edit, 2, 3)

        layout.addWidget(QLabel("Số ghế:"), 3, 0)
        layout.addWidget(self.seat_num_edit, 3, 1)
        layout.addWidget(QLabel("Động cơ:"), 3, 2)
        layout.addWidget(self.engine_edit, 3, 3)

        layout.addWidget(QLabel("Giá:"), 4, 0)
        layout.addWidget(self.price_edit, 4, 1)
        layout.addWidget(QLabel("VIN:"), 4, 2)
        layout.addWidget(self.vin_edit, 4, 3)

        layout.addWidget(QLabel("Bảo hành:"), 5, 0)
        layout.addWidget(self.warranty_year_edit, 5, 1)
        layout.addWidget(QLabel("Trạng thái:"), 5, 2)
        layout.addWidget(self.status_edit, 5, 3)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 6, 0, 1, 4)

    def accept(self):
        add_car(
            self.name_edit.text(),
            int(self.produced_year_edit.text()),
            self.color_edit.text(),
            self.size_edit.text(),
            self.fuel_capacity_edit.text().replace('L', '').strip(),
            self.material_consumption_edit.text(),
            int(self.seat_num_edit.text()),
            self.engine_edit.text(),
            float(self.price_edit.text()),
            self.vin_edit.text(),
            int(self.warranty_year_edit.text()),
            self.status_edit.currentText()
        )
        super().accept()
