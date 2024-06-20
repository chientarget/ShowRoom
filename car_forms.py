from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QLabel, QDialogButtonBox
from database import get_car_details, update_car

class CarEditDialog(QDialog):
    def __init__(self, car_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin xe")
        self.car_id = car_id
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        car_details = get_car_details(self.car_id)

        self.name_edit = QLineEdit(car_details[0])
        self.type_edit = QLineEdit(car_details[1])
        self.year_edit = QLineEdit(str(car_details[2]))
        self.color_edit = QLineEdit(car_details[3])
        self.size_edit = QLineEdit(car_details[4])
        self.engine_edit = QLineEdit(car_details[5])
        self.max_power_edit = QLineEdit(car_details[6])
        self.fuel_capacity_edit = QLineEdit(car_details[7])
        self.transmission_edit = QLineEdit(car_details[8])
        self.fuel_consumption_edit = QLineEdit(car_details[9])
        self.drivetrain_edit = QLineEdit(car_details[10])
        self.seats_edit = QLineEdit(str(car_details[11]))
        self.airbags_edit = QLineEdit(str(car_details[12]))
        self.warranty_edit = QLineEdit(car_details[13])
        self.price_edit = QLineEdit(car_details[14])
        self.dealer_edit = QLineEdit(car_details[15])
        self.status_edit = QLineEdit(car_details[16])

        layout.addRow("Tên xe:", self.name_edit)
        layout.addRow("Loại xe:", self.type_edit)
        layout.addRow("Năm sản xuất:", self.year_edit)
        layout.addRow("Màu sắc:", self.color_edit)
        layout.addRow("Kích thước:", self.size_edit)
        layout.addRow("Động cơ:", self.engine_edit)
        layout.addRow("Công suất tối đa:", self.max_power_edit)
        layout.addRow("Dung tích nhiên liệu:", self.fuel_capacity_edit)
        layout.addRow("Hộp số:", self.transmission_edit)
        layout.addRow("Mức tiêu thụ nhiên liệu:", self.fuel_consumption_edit)
        layout.addRow("Dẫn động:", self.drivetrain_edit)
        layout.addRow("Số ghế:", self.seats_edit)
        layout.addRow("Túi khí:", self.airbags_edit)
        layout.addRow("Bảo hành:", self.warranty_edit)
        layout.addRow("Giá:", self.price_edit)
        layout.addRow("Đại lý:", self.dealer_edit)
        layout.addRow("Trạng thái:", self.status_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def accept(self):
        update_car(
            self.car_id,
            self.name_edit.text(),
            self.type_edit.text(),
            int(self.year_edit.text()),
            self.color_edit.text(),
            self.size_edit.text(),
            self.engine_edit.text(),
            self.max_power_edit.text(),
            self.fuel_capacity_edit.text(),
            self.transmission_edit.text(),
            self.fuel_consumption_edit.text(),
            self.drivetrain_edit.text(),
            int(self.seats_edit.text()),
            int(self.airbags_edit.text()),
            self.warranty_edit.text(),
            self.price_edit.text(),
            self.dealer_edit.text(),
            self.status_edit.text()
        )
        super().accept()

class CarInfoDialog(QDialog):
    def __init__(self, car_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin xe")
        self.car_id = car_id
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        car_details = get_car_details(self.car_id)

        layout.addRow("Tên xe:", QLabel(car_details[0]))
        layout.addRow("Loại xe:", QLabel(car_details[1]))
        layout.addRow("Năm sản xuất:", QLabel(str(car_details[2])))
        layout.addRow("Màu sắc:", QLabel(car_details[3]))
        layout.addRow("Kích thước:", QLabel(car_details[4]))
        layout.addRow("Động cơ:", QLabel(car_details[5]))
        layout.addRow("Công suất tối đa:", QLabel(car_details[6]))
        layout.addRow("Dung tích nhiên liệu:", QLabel(car_details[7]))
        layout.addRow("Hộp số:", QLabel(car_details[8]))
        layout.addRow("Mức tiêu thụ nhiên liệu:", QLabel(car_details[9]))
        layout.addRow("Dẫn động:", QLabel(car_details[10]))
        layout.addRow("Số ghế:", QLabel(str(car_details[11])))
        layout.addRow("Túi khí:", QLabel(str(car_details[12])))
        layout.addRow("Bảo hành:", QLabel(car_details[13]))
        layout.addRow("Giá:", QLabel(car_details[14]))
        layout.addRow("Đại lý:", QLabel(car_details[15]))
        layout.addRow("Trạng thái:", QLabel(car_details[16]))

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        layout.addWidget(self.button_box)
