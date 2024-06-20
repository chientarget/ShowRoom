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
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        header = QLabel("Danh sách xe")
        header.setFont(QFont('MulishRoman', 18, QFont.Weight.Bold))  # Increased font size
        layout.addWidget(header)

        self.car_table = QTableWidget()
        self.car_table.setColumnCount(10)  # 7 data columns + 3 for buttons
        self.car_table.setHorizontalHeaderLabels(["Tên xe", "Năm sản xuất", "Màu sắc", "Bảo hành", "Giá", "Dung tích nhiên liệu", "Trạng thái", "", "", ""])
        self.car_table.horizontalHeader().setStretchLastSection(True)
        self.car_table.setAlternatingRowColors(True)
        self.car_table.setStyleSheet("QHeaderView::section { background-color: #2DB4AE; color: white; }")

        # Set font size for the table and header
        font = QFont('MulishRoman', 12)
        self.car_table.setFont(font)
        self.car_table.horizontalHeader().setFont(QFont('MulishRoman', 14, QFont.Weight.Bold))

        layout.addWidget(self.car_table)

        add_car_button = QPushButton("+ Thêm xe")
        add_car_button.setFont(QFont('MulishRoman', 12))
        add_car_button.setFixedSize(120, 40)
        add_car_button.clicked.connect(self.add_car)
        layout.addWidget(add_car_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.load_cars()

    def load_cars(self):
        self.car_table.setRowCount(0)
        cars = get_cars()
        for car in cars:
            row_position = self.car_table.rowCount()
            self.car_table.insertRow(row_position)
            self.car_table.setItem(row_position, 0, QTableWidgetItem(car[1]))
            self.car_table.setItem(row_position, 1, QTableWidgetItem(str(car[2])))
            self.car_table.setItem(row_position, 2, QTableWidgetItem(car[3]))
            self.car_table.setItem(row_position, 3, QTableWidgetItem(str(car[4])))

            # Format the price
            formatted_price = format_price(float(car[5]))
            self.car_table.setItem(row_position, 4, QTableWidgetItem(formatted_price))

            # Format the fuel capacity
            formatted_capacity = f"{car[6]}L"
            self.car_table.setItem(row_position, 5, QTableWidgetItem(formatted_capacity))

            status_item = QTableWidgetItem(car[7])
            if car[7] == "Đã bán":
                status_item.setForeground(Qt.GlobalColor.green)
            elif car[7] == "Chưa bán":
                status_item.setForeground(Qt.GlobalColor.blue)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.car_table.setItem(row_position, 6, status_item)

            # Add buttons for details, edit, delete with icons
            info_button = QPushButton()
            info_button.setIcon(QIcon("img/info.svg"))
            info_button.setFixedSize(30, 30)
            info_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            info_button.clicked.connect(lambda _, car_id=car[0]: self.show_car_info(car_id))
            self.car_table.setCellWidget(row_position, 7, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon("img/edit.svg"))
            edit_button.setFixedSize(30, 30)
            edit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            edit_button.clicked.connect(lambda _, car_id=car[0]: self.edit_car(car_id))
            self.car_table.setCellWidget(row_position, 8, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("img/delete.svg"))
            delete_button.setFixedSize(30, 30)
            delete_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            delete_button.clicked.connect(lambda _, car_id=car[0]: self.delete_car(car_id))
            self.car_table.setCellWidget(row_position, 9, delete_button)

        self.car_table.resizeColumnsToContents()

        # Adjust column widths to be slightly wider than content
        for col in range(7):  # Only adjust data columns
            current_width = self.car_table.columnWidth(col)
            self.car_table.setColumnWidth(col, current_width + 20)

        # Ensure button columns are only as wide as the buttons
        button_columns = [7, 8, 9]
        for col in button_columns:
            self.car_table.setColumnWidth(col, 40)

    def add_car(self):
        dialog = CarAddDialog(self)
        if dialog.exec():
            self.load_cars()

    def delete_car(self, car_id):
        delete_car(car_id)
        QMessageBox.information(self, "Deleted", f"Car ID '{car_id}' has been deleted.")
        self.load_cars()

    def show_car_info(self, car_id):
        dialog = CarInfoDialog(car_id, self)
        dialog.exec()

    def edit_car(self, car_id):
        dialog = CarEditDialog(car_id, self)
        if dialog.exec():
            self.load_cars()
