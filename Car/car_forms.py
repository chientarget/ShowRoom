# car_forms.py
from PyQt6.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QDialogButtonBox, QComboBox
from Car.car import Car
from database import get_car_details, add_car


class CarEditDialog(QDialog):
    def __init__(self, car_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin xe")
        self.car_id = car_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        car = Car.get_car_by_id(self.car_id)

        self.ten_xe_edit = QLineEdit(car.name)
        self.nam_san_xuat_edit = QLineEdit(str(car.produced_year))
        self.mau_sac_edit = QLineEdit(car.color)
        self.loai_xe_edit = QLineEdit(car.car_type)
        self.dung_tich_nhien_lieu_edit = QLineEdit(f"{car.fuel_capacity}L")
        self.tieu_thu_nhien_lieu_edit = QLineEdit(car.material_consumption)
        self.so_ghe_edit = QLineEdit(str(car.seat_num))
        self.dong_co_edit = QLineEdit(car.engine)
        self.gia_edit = QLineEdit(str(car.price))
        self.vin_edit = QLineEdit(car.vin)
        self.nam_bao_hanh_edit = QLineEdit(str(car.warranty_year))
        self.trang_thai_edit = QComboBox()
        self.trang_thai_edit.addItems(["Chưa bán", "Đã bán", "Chờ mở bán", "Đặt cọc"])
        self.trang_thai_edit.setCurrentText(car.status)

        color ="background-color: #F2F2F2; padding: 5px 10px 5px 10px;  border-radius: 15px;"
        self.ten_xe_edit.setStyleSheet(color)
        self.nam_san_xuat_edit.setStyleSheet(color)
        self.mau_sac_edit.setStyleSheet(color)
        self.loai_xe_edit.setStyleSheet(color)
        self.dung_tich_nhien_lieu_edit.setStyleSheet(color)
        self.tieu_thu_nhien_lieu_edit.setStyleSheet(color)
        self.so_ghe_edit.setStyleSheet(color)
        self.dong_co_edit.setStyleSheet(color)
        self.gia_edit.setStyleSheet(color)
        self.vin_edit.setStyleSheet(color)
        self.nam_bao_hanh_edit.setStyleSheet(color)


        layout.addWidget(QLabel("Tên xe:"), 0, 0)
        layout.addWidget(self.ten_xe_edit, 0, 1)

        layout.addWidget(QLabel("Năm sản xuất:"), 0, 2)
        layout.addWidget(self.nam_san_xuat_edit, 0, 3)

        layout.addWidget(QLabel("Màu sắc:"), 1, 0)
        layout.addWidget(self.mau_sac_edit, 1, 1)
        layout.addWidget(QLabel("Dòng xe:"), 1, 2)
        layout.addWidget(self.loai_xe_edit, 1, 3)

        layout.addWidget(QLabel("Dung tích nhiên liệu:"), 2, 0)
        layout.addWidget(self.dung_tich_nhien_lieu_edit, 2, 1)
        layout.addWidget(QLabel("Tiêu thụ nhiên liệu:"), 2, 2)
        layout.addWidget(self.tieu_thu_nhien_lieu_edit, 2, 3)

        layout.addWidget(QLabel("Số ghế:"), 3, 0)
        layout.addWidget(self.so_ghe_edit, 3, 1)
        layout.addWidget(QLabel("Động cơ:"), 3, 2)
        layout.addWidget(self.dong_co_edit, 3, 3)

        layout.addWidget(QLabel("Giá:"), 4, 0)
        layout.addWidget(self.gia_edit, 4, 1)
        layout.addWidget(QLabel("VIN:"), 4, 2)
        layout.addWidget(self.vin_edit, 4, 3)

        layout.addWidget(QLabel("Bảo hành:"), 5, 0)
        layout.addWidget(self.nam_bao_hanh_edit, 5, 1)
        layout.addWidget(QLabel("Trạng thái:"), 5, 2)
        layout.addWidget(self.trang_thai_edit, 5, 3)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        save_button = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px;  background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box, 6, 0, 1, 4)

    def accept(self):
        car = Car(
            self.car_id,
            self.ten_xe_edit.text(),
            int(self.nam_san_xuat_edit.text()),
            self.mau_sac_edit.text(),
            self.loai_xe_edit.text(),
            self.dung_tich_nhien_lieu_edit.text().replace('L', '').strip(),
            self.tieu_thu_nhien_lieu_edit.text(),
            int(self.so_ghe_edit.text()),
            self.dong_co_edit.text(),
            float(self.gia_edit.text()),
            self.vin_edit.text(),
            int(self.nam_bao_hanh_edit.text()),
            self.trang_thai_edit.currentText()
        )
        car.update()
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
        layout.addWidget(QLabel("Dòng xe:"), 1, 2)
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

        self.ten_xe_edit = QLineEdit()
        self.nam_san_xuat_edit = QLineEdit()
        self.mau_sac_edit = QLineEdit()
        self.loai_xe_edit = QLineEdit()
        self.dung_tich_nhien_lieu_edit = QLineEdit()
        self.tieu_thu_nhien_lieu_edit = QLineEdit()
        self.so_ghe_edit = QLineEdit()
        self.dong_co_edit = QLineEdit()
        self.gia_edit = QLineEdit()
        self.vin_edit = QLineEdit()
        self.nam_bao_hanh_edit = QLineEdit()
        self.trang_thai_edit = QComboBox()
        self.trang_thai_edit.addItems(["Chưa bán", "Đã bán", "Chờ mở bán", "Đặt cọc"])

        layout.addWidget(QLabel("Tên xe:"), 0, 0)
        layout.addWidget(self.ten_xe_edit, 0, 1)
        layout.addWidget(QLabel("Năm sản xuất:"), 0, 2)
        layout.addWidget(self.nam_san_xuat_edit, 0, 3)

        layout.addWidget(QLabel("Màu sắc:"), 1, 0)
        layout.addWidget(self.mau_sac_edit, 1, 1)
        layout.addWidget(QLabel("Dòng xe:"), 1, 2)
        layout.addWidget(self.loai_xe_edit, 1, 3)

        layout.addWidget(QLabel("Dung tích nhiên liệu:"), 2, 0)
        layout.addWidget(self.dung_tich_nhien_lieu_edit, 2, 1)
        layout.addWidget(QLabel("Tiêu thụ nhiên liệu:"), 2, 2)
        layout.addWidget(self.tieu_thu_nhien_lieu_edit, 2, 3)

        layout.addWidget(QLabel("Số ghế:"), 3, 0)
        layout.addWidget(self.so_ghe_edit, 3, 1)
        layout.addWidget(QLabel("Động cơ:"), 3, 2)
        layout.addWidget(self.dong_co_edit, 3, 3)

        layout.addWidget(QLabel("Giá:"), 4, 0)
        layout.addWidget(self.gia_edit, 4, 1)
        layout.addWidget(QLabel("VIN:"), 4, 2)
        layout.addWidget(self.vin_edit, 4, 3)

        layout.addWidget(QLabel("Bảo hành:"), 5, 0)
        layout.addWidget(self.nam_bao_hanh_edit, 5, 1)
        layout.addWidget(QLabel("Trạng thái:"), 5, 2)
        layout.addWidget(self.trang_thai_edit, 5, 3)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 6, 0, 1, 4)

    def accept(self):
        add_car(
            self.ten_xe_edit.text(),
            int(self.nam_san_xuat_edit.text()),
            self.mau_sac_edit.text(),
            self.loai_xe_edit.text(),
            self.dung_tich_nhien_lieu_edit.text().replace('L', '').strip(),
            self.tieu_thu_nhien_lieu_edit.text(),
            int(self.so_ghe_edit.text()),
            self.dong_co_edit.text(),
            float(self.gia_edit.text()),
            self.vin_edit.text(),
            int(self.nam_bao_hanh_edit.text()),
            self.trang_thai_edit.currentText()
        )
        super().accept()

