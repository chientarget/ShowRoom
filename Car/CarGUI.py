import os
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtWidgets import *
from Car.Car import Car

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info_icon_path = os.path.join(base_dir, "img", "img_crud", "info.svg")
edit_icon_path = os.path.join(base_dir, "img", "img_crud", "edit.svg")
delete_icon_path = os.path.join(base_dir, "img", "img_crud", "delete.svg")


def format_price(price):
    if price >= 1_000_000_000:
        return f"{price / 1_000_000_000:.2f} Tỷ"
    elif price >= 1_000_000:
        return f"{price / 1_000_000:.0f} Triệu"
    else:
        return f"{price:,} vnđ"

def format_warranty(warranty):
    return f"{warranty} năm"


def format_capacity(capacity):
    return f"{capacity}L"


class CarGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("Danh sách xe")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        layout.addWidget(header)

        search_layout = QHBoxLayout()

        self.search_vin = QLineEdit()
        self.search_vin.setPlaceholderText("Tìm theo VIN")
        self.search_vin.setFixedHeight(35)
        search_layout.addWidget(self.search_vin)

        self.search_name_color = QLineEdit()
        self.search_name_color.setPlaceholderText("Tìm theo tên, màu sắc")
        self.search_name_color.setFixedHeight(35)
        search_layout.addWidget(self.search_name_color)

        self.search_year = QComboBox()
        self.search_year.addItems(["Tất cả"] + [str(year) for year in range(2000, 2025)])
        search_layout.addWidget(self.search_year)

        self.search_price_range = QComboBox()
        self.search_price_range.addItems(["Tất cả", "Dưới 500 triệu", "500 triệu - 1 tỷ", "Trên 1 tỷ"])
        search_layout.addWidget(self.search_price_range)

        self.search_car_type = QComboBox()
        self.search_car_type.addItems(["Tất cả", "SUV", "Sedan", "Hatchback", "Truck"])
        search_layout.addWidget(self.search_car_type)

        search_button = QPushButton("Tìm kiếm")
        search_button.clicked.connect(self.load_cars)
        search_layout.addWidget(search_button)

        layout.addLayout(search_layout)

        self.summary_layout = QHBoxLayout()
        self.summary_label = QLabel("")
        self.summary_label.setFont(QFont('Roboto', 11, QFont.Weight.Bold))
        self.summary_layout.addWidget(self.summary_label)

        add_car_button = QPushButton("+   Thêm xe")
        add_car_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        add_car_button.setFixedSize(120, 40)
        add_car_button.clicked.connect(self.add_car)
        add_car_button.setProperty("add_car_button", True)
        add_car_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        self.summary_layout.addWidget(add_car_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(self.summary_layout)

        self.car_table = QTableWidget()
        self.car_table.setColumnCount(14)
        self.car_table.setHorizontalHeaderLabels(["Tên xe", "Năm SX", "Màu sắc", "Dòng xe", "Bảo hành", "Giá", "Dung tích", "Trạng thái", "VIN", "Hãng xe", "Model", "", "", ""])
        self.car_table.verticalHeader().setVisible(False)
        self.car_table.horizontalHeader().setStretchLastSection(True)
        self.car_table.setAlternatingRowColors(True)
        self.car_table.setStyleSheet("""
            QHeaderView::section { background-color: #09AD90; color: white; font-size: 16px;  font-weight: bold; font-family: Roboto;}
            QTableWidget::item { font-size: 30px; font-family: Roboto; }
        """)
        layout.addWidget(self.car_table)

        self.setLayout(layout)
        self.load_cars()

    def load_cars(self):
        self.car_table.setRowCount(0)
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()

        query = '''
            SELECT car.name, car.produced_year, car.color, car.car_type, 
                   car.warranty_year, car.price, car.fuel_capacity, car.status, car.vin,
                   series.name AS series_name, model.name AS model_name
            FROM Car car
            JOIN Series series ON car.series_id = series.id
            JOIN Model model ON car.model_id = model.id
            WHERE 1=1
        '''
        params = []



        if self.search_vin.text():
            query += " AND car.vin LIKE ?"
            params.append(f"%{self.search_vin.text()}%")

        if self.search_name_color.text():
            query += " AND (car.name LIKE ? OR car.color LIKE ?)"
            params.extend([f"%{self.search_name_color.text()}%", f"%{self.search_name_color.text()}%"])

        if self.search_year.currentText() != "Tất cả":
            query += " AND car.produced_year = ?"
            params.append(int(self.search_year.currentText()))

        if self.search_price_range.currentText() != "Tất cả":
            if self.search_price_range.currentText() == "Dưới 500 triệu":
                query += " AND car.price < 500000000"
            elif self.search_price_range.currentText() == "500 triệu - 1 tỷ":
                query += " AND car.price BETWEEN 500000000 AND 1000000000"
            elif self.search_price_range.currentText() == "Trên 1 tỷ":
                query += " AND car.price > 1000000000"

        if self.search_car_type.currentText() != "Tất cả":
            query += " AND car.car_type = ?"
            params.append(self.search_car_type.currentText())

        cursor.execute(query, params)
        cars = cursor.fetchall()
        conn.close()

        sold_count = 0
        not_sold_count = 0
        reserved_count = 0

        for car in cars:
            row_position = self.car_table.rowCount()
            self.car_table.insertRow(row_position)
            for column_number, data in enumerate(car):
                table_item = QTableWidgetItem(str(data))
                if column_number == 7:  # Status column
                    if data == "Đã bán":
                        table_item.setBackground(QColor("#43BF5E"))
                    elif data == "Chưa bán":
                        table_item.setBackground(QColor("#8E8EE9"))
                    elif data == "Đặt cọc":
                        table_item.setBackground(QColor("#E9938E"))
                self.car_table.setItem(row_position, column_number, table_item)

            # Add buttons for details, edit, delete with icons
            info_button = QPushButton()
            info_button.setIcon(QIcon(info_icon_path))
            info_button.setStyleSheet("background-color: transparent;")
            info_button.clicked.connect(lambda _, car_id=car[0]: self.show_car_info(car_id))
            self.car_table.setCellWidget(row_position, 11, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.clicked.connect(lambda _, car_id=car[0]: self.edit_car(car_id))
            self.car_table.setCellWidget(row_position, 12, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.clicked.connect(lambda _, car_id=car[0]: self.delete_car(car_id))
            self.car_table.setCellWidget(row_position, 13, delete_button)

            if car[7] == "Đã bán":
                sold_count += 1
            elif car[7] == "Chưa bán":
                not_sold_count += 1
            elif car[7] == "Đặt cọc":
                reserved_count += 1



        self.car_table.resizeColumnsToContents()

        # Ensure button columns are only as wide as the buttons
        button_columns = [11, 12, 13]
        for col in button_columns:
            self.car_table.setColumnWidth(col, 40)

        # Update the summary labels
        self.summary_label.setText(f"Đã bán: {sold_count}   Chưa bán: {not_sold_count}   Đặt cọc: {reserved_count}")

    def add_car(self):
        dialog = CarAddDialog(self)
        if dialog.exec():
            self.load_cars()

    def delete_car(self, car_id):
        Car.delete(car_id)
        QMessageBox.information(self, "Deleted", f"Car ID '{car_id}' has been deleted.")
        self.load_cars()

    def show_car_info(self, car_id):
        dialog = CarInfoDialog(car_id, self)
        dialog.exec()

    def edit_car(self, car_id):
        dialog = CarEditDialog(car_id, self)
        if dialog.exec():
            self.load_cars()


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
        self.trang_thai_edit.addItems(["Chưa bán", "Đã bán", "Đặt cọc"])
        self.trang_thai_edit.setCurrentText(car.status)

        color = "background-color: #F2F2F2; padding: 5px 10px 5px 10px;  border-radius: 15px;"
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

        car_details = Car.get_car_details(self.car_id)

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

        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Drive")
        engines = cursor.fetchall()
        conn.close()

        self.ten_xe_edit = QLineEdit()
        self.nam_san_xuat_edit = QLineEdit()
        self.mau_sac_edit = QLineEdit()
        self.loai_xe_edit = QLineEdit()
        self.dung_tich_nhien_lieu_edit = QLineEdit()
        self.tieu_thu_nhien_lieu_edit = QLineEdit()
        self.so_ghe_edit = QLineEdit()
        self.dong_co_edit = QComboBox()
        self.dong_co_edit.addItems([f"{e[0]} - {e[1]}" for e in engines])
        self.gia_edit = QLineEdit()
        self.vin_edit = QLineEdit()
        self.nam_bao_hanh_edit = QLineEdit()
        self.trang_thai_edit = QComboBox()
        self.trang_thai_edit.addItems(["Chưa bán", "Đã bán", "Đặt cọc"])

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

        self.setLayout(layout)

    def accept(self):
        Car.add_car(
            self.ten_xe_edit.text(),
            int(self.nam_san_xuat_edit.text()),
            self.mau_sac_edit.text(),
            self.loai_xe_edit.text(),
            self.dung_tich_nhien_lieu_edit.text().replace('L', '').strip(),
            self.tieu_thu_nhien_lieu_edit.text(),
            int(self.so_ghe_edit.text()),
            self.dong_co_edit.currentText().split(' - ')[1],
            float(self.gia_edit.text()),
            self.vin_edit.text(),
            int(self.nam_bao_hanh_edit.text()),
            self.trang_thai_edit.currentText()
        )
        super().accept()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Showroom Vinfast")
        self.setGeometry(100, 100, 1500, 900)

        # Main container widget
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Left sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("<span style='color: #2DB4AE;'>Showroom</span><span style='color: #FBCE49;'> VinFast</span>")
        title.setFont(QFont('MulishRoman', 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2DB4AE;")  # Light green color
        sidebar_layout.addWidget(title)

        user_label = QLabel("Phạm nhật vượng\nID: 3456")
        user_label.setFont(QFont('MulishRoman', 12))
        user_label.setStyleSheet("color: #FFFFFF; background-color: #444444; padding: 10px;")
        sidebar_layout.addWidget(user_label)

        sidebar_buttons = [
            "Tổng quan", "Danh sách xe", "Danh sách đơn hàng",
            "Hãng xe đối tác", "Danh sách khách hàng", "Danh sách nhân viên",
            "Danh sách đại lý"
        ]
        sidebar_layout.addStretch()

        for button_text in sidebar_buttons:
            button = QPushButton(button_text)
            button.setFont(QFont('MulishRoman', 12, QFont.Weight.Bold))
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        logout_button = QPushButton("Đăng xuất")
        logout_button.setFont(QFont('MulishRoman', 12, QFont.Weight.Bold))
        sidebar_layout.addWidget(logout_button)

        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(sidebar)

        # Main content area
        content = QWidget()
        content_layout = QVBoxLayout(content)

        header = QLabel("Danh sách xe")
        header.setFont(QFont('MulishRoman', 16, QFont.Weight.Bold))
        content_layout.addWidget(header)

        self.car_table = QTableWidget()
        self.car_table.setColumnCount(10)
        self.car_table.setHorizontalHeaderLabels(["Tên xe", "Dòng xe", "Năm sản xuất", "Màu sắc", "Bảo hành", "Giá", "Trạng thái", "Thông tin", "Sửa", "Xóa"])
        self.car_table.horizontalHeader().setStretchLastSection(True)
        self.car_table.setAlternatingRowColors(True)
        self.car_table.setStyleSheet("QHeaderView::section { background-color: #2DB4AE; color: white; }")
        self.load_cars()
        content_layout.addWidget(self.car_table)

        add_car_button = QPushButton("+ Thêm xe")
        add_car_button.setFont(QFont('MulishRoman', 12))
        add_car_button.setFixedSize(120, 40)
        add_car_button.clicked.connect(self.add_car)
        content_layout.addWidget(add_car_button, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(content)

        self.setCentralWidget(main_widget)

    def load_cars(self):
        self.car_table.setRowCount(0)
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT car.name, car.produced_year, car.color, car.car_type, 
                   car.warranty_year, car.price, car.fuel_capacity, car.status, car.vin,
                   series.name AS series_name, model.name AS model_name
            FROM Car car
            JOIN Series series ON car.series_id = series.id
            JOIN Model model ON car.model_id = model.id
        ''')
        cars = cursor.fetchall()
        conn.close()

        sold_count = 0
        not_sold_count = 0
        reserved_count = 0

        for car in cars:
            row_position = self.car_table.rowCount()
            self.car_table.insertRow(row_position)
            for column_number, data in enumerate(car):
                if column_number == 4:  # Warranty column
                    data = format_warranty(data)
                elif column_number == 6:  # Capacity column
                    data = format_capacity(data)
                self.car_table.setItem(row_position, column_number, QTableWidgetItem(str(data)))

            # Add buttons for details, edit, delete with icons
            info_button = QPushButton()
            info_button.setIcon(QIcon(info_icon_path))
            info_button.setStyleSheet("background-color: transparent;")
            info_button.clicked.connect(lambda _, car_vin=car[8]: self.show_car_info(car_vin))
            self.car_table.setCellWidget(row_position, 11, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.clicked.connect(lambda _, car_vin=car[8]: self.edit_car(car_vin))
            self.car_table.setCellWidget(row_position, 12, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.clicked.connect(lambda _, car_vin=car[8]: self.delete_car(car_vin))
            self.car_table.setCellWidget(row_position, 13, delete_button)

        self.car_table.resizeColumnsToContents()

        # Adjust column widths to be slightly wider than content
        for col in range(10):  # Only adjust data columns
            current_width = self.car_table.columnWidth(col)
            self.car_table.setColumnWidth(col, current_width + 20)

        # Ensure button columns are only as wide as the buttons
        button_columns = [11, 12, 13]
        for col in button_columns:
            self.car_table.setColumnWidth(col, 40)

        # Update the summary labels
        sold_count = sum(1 for car in cars if car[7] == "Đã bán")
        not_sold_count = sum(1 for car in cars if car[7] == "Chưa bán")
        reserved_count = sum(1 for car in cars if car[7] == "Đặt cọc")
        self.summary_label.setText(f"Đã bán: {sold_count}   Chưa bán: {not_sold_count}   Đặt cọc: {reserved_count}")

    def add_car(self):
        # Logic to add a car to the database (could show a dialog to input car details)
        pass

    def delete_car(self, car_name):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cars WHERE name = ?', (car_name,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Deleted", f"Car '{car_name}' has been deleted.")
        self.load_cars()

    def show_car_info(self, car_name):
        # Logic to show car details (could show a dialog with car details)
        QMessageBox.information(self, "Thông tin xe", f"Thông tin chi tiết của xe '{car_name}'")

    def edit_car(self, car_name):
        # Logic to edit car details (could show a dialog to edit car details)
        QMessageBox.information(self, "Sửa thông tin xe", f"Sửa thông tin của xe '{car_name}'")