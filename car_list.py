from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy, QMessageBox
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from database import get_cars, delete_car
from car_forms import CarEditDialog, CarInfoDialog, CarAddDialog

def format_price(price):
    if price >= 1_000_000_000:
        formatted_price = f"{price / 1_000_000_000:.2f} Tỷ"
    elif price >= 1_000_000:
        formatted_price = f"{price / 1_000_000:.0f} Triệu"
    else:
        formatted_price = f"{price:,} vnđ"
    return formatted_price

class CarListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("Initializing CarListWidget")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("Danh sách xe")
        header.setFont(QFont('MulishRoman', 16, QFont.Weight.Bold))
        layout.addWidget(header)

        self.car_table = QTableWidget()
        self.car_table.setColumnCount(11)
        self.car_table.setHorizontalHeaderLabels(["Tên xe", "Năm sản xuất", "Màu sắc", "Loại xe", "Bảo hành (Năm)", "Giá", "Dung tích nhiên liệu", "Trạng thái", "Thông tin", "Sửa", "Xóa"])
        self.car_table.horizontalHeader().setStretchLastSection(True)
        self.car_table.setAlternatingRowColors(True)
        self.car_table.setStyleSheet("QHeaderView::section { background-color: #2DB4AE; color: white; }")
        layout.addWidget(self.car_table)

        add_car_button = QPushButton("+ Thêm xe")
        add_car_button.setFont(QFont('MulishRoman', 12))
        add_car_button.setFixedSize(120, 40)
        add_car_button.clicked.connect(self.add_car)
        layout.addWidget(add_car_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.load_cars()

    def load_cars(self):
        print("Loading cars")
        self.car_table.setRowCount(0)
        cars = get_cars()
        for car in cars:
            row_position = self.car_table.rowCount()
            self.car_table.insertRow(row_position)
            self.car_table.setItem(row_position, 0, QTableWidgetItem(car[1]))  # name
            self.car_table.setItem(row_position, 1, QTableWidgetItem(str(car[2])))  # produced_year
            self.car_table.setItem(row_position, 2, QTableWidgetItem(car[3]))  # color
            self.car_table.setItem(row_position, 3, QTableWidgetItem(car[4]))  # car_type
            self.car_table.setItem(row_position, 4, QTableWidgetItem(f"{car[10]} Năm"))  # warranty_year

            # Handle the price conversion
            try:
                formatted_price = format_price(float(car[9]))  # price (corrected index)
            except ValueError:
                formatted_price = "N/A"
                print(f"Warning: Could not convert price to float for car ID {car[0]}: {car[9]}")

            self.car_table.setItem(row_position, 5, QTableWidgetItem(formatted_price))

            # Format the fuel capacity
            formatted_capacity = f"{car[5]}L"  # fuel_capacity
            self.car_table.setItem(row_position, 6, QTableWidgetItem(formatted_capacity))

            # Display the status
            status_item = QTableWidgetItem(car[11])  # status (corrected index)
            if car[11] == "Đã bán":
                status_item.setForeground(Qt.GlobalColor.green)
            elif car[11] == "Chưa bán":
                status_item.setForeground(Qt.GlobalColor.blue)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.car_table.setItem(row_position, 7, status_item)

            # Add buttons for details, edit, delete with icons
            info_button = QPushButton()
            info_button.setIcon(QIcon("img/info.svg"))
            info_button.setFixedSize(30, 30)
            info_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            info_button.clicked.connect(lambda _, car_id=car[0]: self.show_car_info(car_id))
            self.car_table.setCellWidget(row_position, 8, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon("img/edit.svg"))
            edit_button.setFixedSize(30, 30)
            edit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            edit_button.clicked.connect(lambda _, car_id=car[0]: self.edit_car(car_id))
            self.car_table.setCellWidget(row_position, 9, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("img/delete.svg"))
            delete_button.setFixedSize(30, 30)
            delete_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            delete_button.clicked.connect(lambda _, car_id=car[0]: self.delete_car(car_id))
            self.car_table.setCellWidget(row_position, 10, delete_button)

        self.car_table.resizeColumnsToContents()

        # Adjust column widths to be slightly wider than content
        for col in range(7):  # Only adjust data columns
            current_width = self.car_table.columnWidth(col)
            self.car_table.setColumnWidth(col, current_width + 20)

        # Ensure button columns are only as wide as the buttons
        button_columns = [8, 9, 10]
        for col in button_columns:
            self.car_table.setColumnWidth(col, 40)

    def add_car(self):
        print("Adding a new car")
        dialog = CarAddDialog(self)
        if dialog.exec():
            self.load_cars()

    def delete_car(self, car_id):
        print(f"Deleting car with ID: {car_id}")
        delete_car(car_id)
        QMessageBox.information(self, "Deleted", f"Car ID '{car_id}' has been deleted.")
        self.load_cars()

    def show_car_info(self, car_id):
        print(f"Showing info for car ID: {car_id}")
        dialog = CarInfoDialog(car_id, self)
        dialog.exec()

    def edit_car(self, car_id):
        print(f"Editing car ID: {car_id}")
        dialog = CarEditDialog(car_id, self)
        if dialog.exec():
            self.load_cars()
