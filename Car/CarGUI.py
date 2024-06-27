# CarGUI.py
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

        search_layout = QGridLayout()

        # Search by VIN
        search_vin_label = QLabel("Tìm theo VIN:")
        self.search_vin = QLineEdit()
        self.search_vin.setPlaceholderText("Tìm theo VIN")
        self.search_vin.setFixedHeight(35)
        search_layout.addWidget(search_vin_label, 0, 0)
        search_layout.addWidget(self.search_vin, 1, 0)
        self.search_vin.textChanged.connect(self.load_cars)

        # Search by name
        search_name_label = QLabel("Tìm theo tên:")
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Tìm theo tên")
        self.search_name.setFixedHeight(35)
        search_layout.addWidget(search_name_label, 0, 1)
        search_layout.addWidget(self.search_name, 1, 1)
        self.search_name.textChanged.connect(self.load_cars)

        # Search by color
        search_color_label = QLabel("Tìm theo màu sắc:")
        self.search_color = QComboBox()
        colors = self.get_all_colors()
        self.search_color.addItems(["Tất cả"] + colors)
        self.search_color.setFixedHeight(35)
        search_layout.addWidget(search_color_label, 0, 2)
        search_layout.addWidget(self.search_color, 1, 2)
        self.search_color.currentIndexChanged.connect(self.load_cars)

        # Search by price range
        search_price_range_label = QLabel("Tìm theo giá:")
        self.search_price_range = QComboBox()
        self.search_price_range.addItems(["Tất cả", "Dưới 500 triệu", "500 triệu - 1 tỷ", "Trên 1 tỷ"])
        self.search_price_range.setFixedHeight(35)
        search_layout.addWidget(search_price_range_label, 0, 3)
        search_layout.addWidget(self.search_price_range, 1, 3)
        self.search_price_range.currentIndexChanged.connect(self.load_cars)

        # Search by car type
        search_car_type_label = QLabel("Tìm theo dòng xe:")
        self.search_car_type = QComboBox()
        car_types = Car.get_foreign_key_data("Car_Type")
        self.search_car_type.addItems(["Tất cả"] + list(car_types.values()))
        self.search_car_type.setFixedHeight(35)
        search_layout.addWidget(search_car_type_label, 0, 4)
        search_layout.addWidget(self.search_car_type, 1, 4)
        self.search_car_type.currentIndexChanged.connect(self.load_cars)

        # Search by dealer
        search_dealer_label = QLabel("Tìm theo đại lý:")
        self.search_dealer = QComboBox()
        dealers = Car.get_foreign_key_data("Dealer")
        self.search_dealer.addItems(["Tất cả"] + list(dealers.values()))
        self.search_dealer.setFixedHeight(35)
        search_layout.addWidget(search_dealer_label, 0, 5)
        search_layout.addWidget(self.search_dealer, 1, 5)
        self.search_dealer.currentIndexChanged.connect(self.load_cars)

        # Search by status
        search_status_label = QLabel("Tìm theo trạng thái:")
        self.search_status = QComboBox()
        statuses = self.get_all_statuses()
        self.search_status.addItems(["Tất cả"] + statuses)
        self.search_status.setFixedHeight(35)
        search_layout.addWidget(search_status_label, 0, 6)
        search_layout.addWidget(self.search_status, 1, 6)
        self.search_status.currentIndexChanged.connect(self.load_cars)

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
        self.car_table.setHorizontalHeaderLabels([
            "VIN", "Tên xe", "Hãng xe", "Dòng xe", "Model", "Màu sắc",
            "Năm sản xuất", "Bảo hành", "Dung tích", "Giá", "Trạng thái",
            "", "", ""
        ])

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

    def get_all_colors(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT color FROM Car')
        colors = [row[0] for row in cursor.fetchall()]
        conn.close()
        return colors

    def get_all_statuses(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT status FROM Car')
        statuses = [row[0] for row in cursor.fetchall()]
        conn.close()
        return statuses

    def load_cars(self):
        self.car_table.setRowCount(0)
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()

        query = '''
            SELECT car.vin, car.name, dealer.name AS dealer_name, 
                   car_type.name AS car_type_name, model.name AS model_name, car.color, 
                   car.produced_year, car.warranty_year, car.fuel_capacity, 
                   car.price, car.status, engine.name AS engine_name
            FROM Car car
            JOIN Dealer dealer ON car.dealer_id = dealer.id
            JOIN Car_Type car_type ON car.car_type_id = car_type.id
            JOIN Model model ON car.model_id = model.id
            JOIN Engine engine ON car.engine_id = engine.id
            WHERE 1=1
        '''
        params = []

        if self.search_vin.text():
            query += " AND car.vin LIKE ?"
            params.append(f"%{self.search_vin.text()}%")

        if self.search_name.text():
            query += " AND car.name LIKE ?"
            params.append(f"%{self.search_name.text()}%")

        if self.search_color.currentText() != "Tất cả":
            query += " AND car.color = ?"
            params.append(self.search_color.currentText())

        if self.search_price_range.currentText() != "Tất cả":
            if self.search_price_range.currentText() == "Dưới 500 triệu":
                query += " AND car.price < 500000000"
            elif self.search_price_range.currentText() == "500 triệu - 1 tỷ":
                query += " AND car.price BETWEEN 500000000 AND 1000000000"
            elif self.search_price_range.currentText() == "Trên 1 tỷ":
                query += " AND car.price > 1000000000"

        if self.search_car_type.currentText() != "Tất cả":
            car_type_id = Car.get_id_by_name("Car_Type", self.search_car_type.currentText())
            query += " AND car.car_type_id = ?"
            params.append(car_type_id)

        if self.search_dealer.currentText() != "Tất cả":
            dealer_id = Car.get_id_by_name("Dealer", self.search_dealer.currentText())
            query += " AND car.dealer_id = ?"
            params.append(dealer_id)

        if self.search_status.currentText() != "Tất cả":
            query += " AND car.status = ?"
            params.append(self.search_status.currentText())

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
                try:
                    if column_number == 7:  # Bảo hành
                        table_item = QTableWidgetItem(format_warranty(int(data)))
                    elif column_number == 9:  # Giá
                        table_item = QTableWidgetItem(format_price(int(data)))
                    elif column_number == 8:  # Dung tích
                        table_item = QTableWidgetItem(format_capacity(float(data)))
                    else:
                        table_item = QTableWidgetItem(str(data))
                except ValueError:
                    table_item = QTableWidgetItem(str(data))
                table_item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # make cell read-only
                if column_number == 10:  # Trạng thái
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
            info_button.clicked.connect(lambda _, vin=car[0]: self.show_car_info(vin))
            self.car_table.setCellWidget(row_position, 11, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.clicked.connect(lambda _, vin=car[0]: self.edit_car(vin))
            self.car_table.setCellWidget(row_position, 12, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.clicked.connect(lambda _, vin=car[0]: self.delete_car(vin))
            self.car_table.setCellWidget(row_position, 13, delete_button)

            if car[10] == "Đã bán":
                sold_count += 1
            elif car[10] == "Chưa bán":
                not_sold_count += 1
            elif car[10] == "Đặt cọc":
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

    def delete_car(self, vin):
        reply = QMessageBox.question(self, 'Xác nhận xóa',
                                     f"Bạn có chắc chắn muốn xóa xe có VIN '{vin}' không?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            Car.delete_by_vin(vin)
            self.load_cars()

    def show_car_info(self, vin):
        dialog = CarInfoDialog(vin, self)
        dialog.exec()

    def edit_car(self, vin):
        dialog = CarEditDialog(vin, self)
        if dialog.exec():
            self.load_cars()


class CarEditDialog(QDialog):
    def __init__(self, vin, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin xe")
        self.vin = vin
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        car = Car.get_car_by_vin(self.vin)

        if car is None:
            QMessageBox.critical(self, "Error", f"Car with VIN {self.vin} not found.")
            self.reject()
            return

        # Get foreign key data
        self.dealers = Car.get_foreign_key_data("Dealer")
        self.partners = Car.get_foreign_key_data("Partner")
        self.engines = Car.get_foreign_key_data("Engine")
        self.models = Car.get_foreign_key_data("Model")
        self.car_types = Car.get_foreign_key_data("Car_Type")

        self.id_edit = QLineEdit(str(car.id))
        self.id_edit.setEnabled(False)
        self.name_edit = QLineEdit(car.name)
        self.produced_year_edit = QLineEdit(str(car.produced_year))
        self.color_edit = QLineEdit(car.color)
        self.car_type_edit = QComboBox()
        self.car_type_edit.addItems(list(self.car_types.values()))
        self.car_type_edit.setCurrentText(Car.get_name_by_id("Car_Type", car.car_type_id))
        self.fuel_capacity_edit = QLineEdit(str(car.fuel_capacity))
        self.material_consumption_edit = QLineEdit(car.material_consumption)
        self.seat_num_edit = QLineEdit(str(car.seat_num))
        self.engine_edit = QComboBox()
        self.engine_edit.addItems(list(self.engines.values()))
        self.engine_edit.setCurrentText(Car.get_name_by_id("Engine", car.engine_id))
        self.price_edit = QLineEdit(str(car.price))
        self.vin_edit = QLineEdit(car.vin)
        self.vin_edit.setEnabled(False)
        self.warranty_year_edit = QLineEdit(str(car.warranty_year))
        self.status_edit = QComboBox()
        self.status_edit.addItems(["Chưa bán", "Đã bán", "Đặt cọc"])
        self.status_edit.setCurrentText(car.status)
        self.dealer_edit = QComboBox()
        self.dealer_edit.addItems(list(self.dealers.values()))
        self.dealer_edit.setCurrentText(Car.get_name_by_id("Dealer", car.dealer_id))
        self.partner_edit = QComboBox()
        self.partner_edit.addItems(list(self.partners.values()))
        self.partner_edit.setCurrentText(Car.get_name_by_id("Partner", car.partner_id))
        self.model_edit = QComboBox()
        self.model_edit.addItems(list(self.models.values()))
        self.model_edit.setCurrentText(Car.get_name_by_id("Model", car.model_id))
        self.airbags_edit = QLineEdit(car.airbags)

        color = "background-color:#1e1e1e ; padding: 5px 10px 5px 10px;  border-radius: 15px; color: white;"
        for widget in [
            self.id_edit, self.name_edit, self.produced_year_edit, self.color_edit,
            self.car_type_edit, self.fuel_capacity_edit, self.material_consumption_edit,
            self.seat_num_edit, self.engine_edit, self.price_edit,
            self.vin_edit, self.warranty_year_edit, self.airbags_edit,
            self.status_edit, self.dealer_edit, self.partner_edit, self.model_edit
        ]:
            widget.setStyleSheet(color)

        layout.addWidget(QLabel("ID:"), 0, 0)
        layout.addWidget(self.id_edit, 0, 1)

        layout.addWidget(QLabel("Tên xe:"), 1, 0)
        layout.addWidget(self.name_edit, 1, 1)

        layout.addWidget(QLabel("Năm sản xuất:"), 2, 0)
        layout.addWidget(self.produced_year_edit, 2, 1)

        layout.addWidget(QLabel("Màu sắc:"), 3, 0)
        layout.addWidget(self.color_edit, 3, 1)

        layout.addWidget(QLabel("Dòng xe:"), 4, 0)
        layout.addWidget(self.car_type_edit, 4, 1)

        layout.addWidget(QLabel("Dung tích nhiên liệu:"), 5, 0)
        layout.addWidget(self.fuel_capacity_edit, 5, 1)

        layout.addWidget(QLabel("Tiêu thụ nhiên liệu:"), 0, 2)
        layout.addWidget(self.material_consumption_edit, 0, 3)

        layout.addWidget(QLabel("Số ghế:"), 1, 2)
        layout.addWidget(self.seat_num_edit, 1, 3)

        layout.addWidget(QLabel("Động cơ:"), 2, 2)
        layout.addWidget(self.engine_edit, 2, 3)

        layout.addWidget(QLabel("Giá:"), 3, 2)
        layout.addWidget(self.price_edit, 3, 3)

        layout.addWidget(QLabel("VIN:"), 4, 2)
        layout.addWidget(self.vin_edit, 4, 3)

        layout.addWidget(QLabel("Bảo hành:"), 5, 2)
        layout.addWidget(self.warranty_year_edit, 5, 3)

        layout.addWidget(QLabel("Trạng thái:"), 0, 4)
        layout.addWidget(self.status_edit, 0, 5)

        layout.addWidget(QLabel("Dealer:"), 1, 4)
        layout.addWidget(self.dealer_edit, 1, 5)

        layout.addWidget(QLabel("Partner:"), 2, 4)
        layout.addWidget(self.partner_edit, 2, 5)

        layout.addWidget(QLabel("Model:"), 3, 4)
        layout.addWidget(self.model_edit, 3, 5)

        layout.addWidget(QLabel("Airbags:"), 4, 4)
        layout.addWidget(self.airbags_edit, 4, 5)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        save_button = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box, 6, 0, 1, 6)

        self.setLayout(layout)

    def accept(self):
        car = Car(
            int(self.id_edit.text()),
            self.name_edit.text(),
            int(self.produced_year_edit.text()),
            self.color_edit.text(),
            Car.get_id_by_name("Car_Type", self.car_type_edit.currentText()),
            float(self.fuel_capacity_edit.text()),
            self.material_consumption_edit.text(),
            int(self.seat_num_edit.text()),
            Car.get_id_by_name("Engine", self.engine_edit.currentText()),
            float(self.price_edit.text()),
            self.vin_edit.text(),
            int(self.warranty_year_edit.text()),
            self.status_edit.currentText(),
            Car.get_id_by_name("Dealer", self.dealer_edit.currentText()),
            Car.get_id_by_name("Partner", self.partner_edit.currentText()),
            Car.get_id_by_name("Model", self.model_edit.currentText()),
            self.airbags_edit.text()
        )
        car.update()
        super().accept()


class CarAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm xe mới")
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        self.dealers = Car.get_foreign_key_data("Dealer")
        self.partners = Car.get_foreign_key_data("Partner")
        self.engines = Car.get_foreign_key_data("Engine")
        self.models = Car.get_foreign_key_data("Model")
        self.car_types = Car.get_foreign_key_data("Car_Type")

        self.name_edit = QLineEdit()
        self.produced_year_edit = QLineEdit()
        self.color_edit = QLineEdit()
        self.car_type_edit = QComboBox()
        self.car_type_edit.addItems(list(self.car_types.values()))
        self.fuel_capacity_edit = QLineEdit()
        self.material_consumption_edit = QLineEdit()
        self.seat_num_edit = QLineEdit()
        self.engine_edit = QComboBox()
        self.engine_edit.addItems(list(self.engines.values()))
        self.price_edit = QLineEdit()
        self.vin_edit = QLineEdit()
        self.warranty_year_edit = QLineEdit()
        self.status_edit = QComboBox()
        self.status_edit.addItems(["Chưa bán", "Đã bán", "Đặt cọc"])
        self.dealer_edit = QComboBox()
        self.dealer_edit.addItems(list(self.dealers.values()))
        self.partner_edit = QComboBox()
        self.partner_edit.addItems(list(self.partners.values()))
        self.model_edit = QComboBox()
        self.model_edit.addItems(list(self.models.values()))
        self.airbags_edit = QLineEdit()

        color = "background-color:#1e1e1e ; padding: 5px 10px 5px 10px;  border-radius: 15px; color: white;"
        for widget in [
            self.name_edit, self.produced_year_edit, self.color_edit,
            self.car_type_edit, self.fuel_capacity_edit, self.material_consumption_edit,
            self.seat_num_edit, self.engine_edit, self.price_edit,
            self.vin_edit, self.warranty_year_edit, self.airbags_edit,
            self.status_edit, self.dealer_edit, self.partner_edit, self.model_edit
        ]:
            widget.setStyleSheet(color)

        layout.addWidget(QLabel("Tên xe:"), 0, 0)
        layout.addWidget(self.name_edit, 0, 1)

        layout.addWidget(QLabel("Màu sắc:"), 1, 0)
        layout.addWidget(self.color_edit, 1, 1)

        layout.addWidget(QLabel("Dung tích nhiên liệu:"), 2, 0)
        layout.addWidget(self.fuel_capacity_edit, 2, 1)

        layout.addWidget(QLabel("Số ghế:"), 3, 0)
        layout.addWidget(self.seat_num_edit, 3, 1)

        layout.addWidget(QLabel("Giá:"), 4, 0)
        layout.addWidget(self.price_edit, 4, 1)

        layout.addWidget(QLabel("Bảo hành:"), 5, 0)
        layout.addWidget(self.warranty_year_edit, 5, 1)

        layout.addWidget(QLabel("Năm sản xuất:"), 0, 2)
        layout.addWidget(self.produced_year_edit, 0, 3)

        layout.addWidget(QLabel("Dòng xe:"), 1, 2)
        layout.addWidget(self.car_type_edit, 1, 3)

        layout.addWidget(QLabel("Tiêu thụ nhiên liệu:"), 2, 2)
        layout.addWidget(self.material_consumption_edit, 2, 3)

        layout.addWidget(QLabel("Động cơ:"), 3, 2)
        layout.addWidget(self.engine_edit, 3, 3)

        layout.addWidget(QLabel("VIN:"), 4, 2)
        layout.addWidget(self.vin_edit, 4, 3)

        layout.addWidget(QLabel("Trạng thái:"), 5, 2)
        layout.addWidget(self.status_edit, 5, 3)

        layout.addWidget(QLabel("Dealer:"), 0, 4)
        layout.addWidget(self.dealer_edit, 0, 5)

        layout.addWidget(QLabel("Partner:"), 1, 4)
        layout.addWidget(self.partner_edit, 1, 5)

        layout.addWidget(QLabel("Model:"), 2, 4)
        layout.addWidget(self.model_edit, 2, 5)

        layout.addWidget(QLabel("Airbags:"), 3, 4)
        layout.addWidget(self.airbags_edit, 3, 5)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        save_button = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box, 6, 0, 1, 6)

        self.setLayout(layout)

    def accept(self):
        Car.add_car(
            self.name_edit.text(),
            int(self.produced_year_edit.text()),
            self.color_edit.text(),
            Car.get_id_by_name("Car_Type", self.car_type_edit.currentText()),
            float(self.fuel_capacity_edit.text()),
            self.material_consumption_edit.text(),
            int(self.seat_num_edit.text()),
            Car.get_id_by_name("Engine", self.engine_edit.currentText()),
            float(self.price_edit.text()),
            self.vin_edit.text(),
            int(self.warranty_year_edit.text()),
            self.status_edit.currentText(),
            Car.get_id_by_name("Dealer", self.dealer_edit.currentText()),
            Car.get_id_by_name("Partner", self.partner_edit.currentText()),
            Car.get_id_by_name("Model", self.model_edit.currentText()),
            self.airbags_edit.text()
        )
        super().accept()


class CarInfoDialog(QDialog):
    def __init__(self, vin, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin xe")
        self.vin = vin
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        car_details = Car.get_car_details_by_vin(self.vin)

        if car_details is None:
            QMessageBox.critical(self, "Error", f"Car with VIN {self.vin} not found.")
            self.reject()
            return

        layout.addWidget(QLabel("Tên xe:"), 0, 0)
        layout.addWidget(QLabel(car_details[0]), 0, 1)
        layout.addWidget(QLabel("Năm sản xuất:"), 1, 0)
        layout.addWidget(QLabel(str(car_details[1])), 1, 1)
        layout.addWidget(QLabel("Màu sắc:"), 2, 0)
        layout.addWidget(QLabel(car_details[2]), 2, 1)

        layout.addWidget(QLabel("Dòng xe:"), 0, 2)
        layout.addWidget(QLabel(Car.get_name_by_id("Car_Type", car_details[3])), 0, 3)
        layout.addWidget(QLabel("Dung tích nhiên liệu:"), 1, 2)
        layout.addWidget(QLabel(f"{car_details[4]}L"), 1, 3)
        layout.addWidget(QLabel("Tiêu thụ nhiên liệu:"), 2, 2)
        layout.addWidget(QLabel(car_details[5]), 2, 3)

        layout.addWidget(QLabel("Số ghế:"), 0, 4)
        layout.addWidget(QLabel(str(car_details[6])), 0, 5)
        layout.addWidget(QLabel("Động cơ:"), 1, 4)
        layout.addWidget(QLabel(Car.get_name_by_id("Engine", car_details[7])), 1, 5)
        layout.addWidget(QLabel("Giá:"), 2, 4)
        layout.addWidget(QLabel(str(car_details[8])), 2, 5)

        layout.addWidget(QLabel("VIN:"), 3, 0)
        layout.addWidget(QLabel(car_details[9]), 3, 1)
        layout.addWidget(QLabel("Bảo hành:"), 3, 2)
        layout.addWidget(QLabel(str(car_details[10])), 3, 3)
        layout.addWidget(QLabel("Trạng thái:"), 3, 4)
        layout.addWidget(QLabel(car_details[11]), 3, 5)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box, 4, 0, 1, 6)

        self.setLayout(layout)
