# car_list.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtCore import Qt
from Car.car import Car
from Car.car_forms import CarEditDialog, CarInfoDialog, CarAddDialog

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
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        layout.addWidget(header)

        self.summary_layout = QHBoxLayout()
        self.summary_label = QLabel("")
        self.summary_label.setFont(QFont('Roboto', 11, QFont.Weight.Bold))
        self.summary_layout.addWidget(self.summary_label)

        add_car_button = QPushButton("+ Thêm xe")
        add_car_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        add_car_button.setFixedSize(120, 40)
        add_car_button.clicked.connect(self.add_car)
        add_car_button.setProperty("add_car_button", True)
        self.summary_layout.addWidget(add_car_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(self.summary_layout)

        self.car_table = QTableWidget()
        self.car_table.setColumnCount(11)
        self.car_table.setHorizontalHeaderLabels(["Tên xe", "Năm SX", "Màu sắc", "Loại xe", "Bảo hành", "Giá", "Dung tích", "Trạng thái", "", "", ""])
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
        cars = Car.get_all_cars()
        sold_count = 0
        not_sold_count = 0
        pending_count = 0
        reserved_count = 0

        for car in cars:
            row_position = self.car_table.rowCount()
            self.car_table.insertRow(row_position)
            self.car_table.setItem(row_position, 0, QTableWidgetItem(car.name))  # name
            self.car_table.setItem(row_position, 1, QTableWidgetItem(str(car.produced_year)))  # produced_year
            self.car_table.setItem(row_position, 2, QTableWidgetItem(car.color))  # color
            self.car_table.setItem(row_position, 3, QTableWidgetItem(car.car_type))  # car_type
            self.car_table.setItem(row_position, 4, QTableWidgetItem(f"{car.warranty_year} Năm"))  # warranty_year

            # Handle the price conversion
            try:
                formatted_price = format_price(float(car.price))  # price
            except ValueError:
                formatted_price = "N/A"

            self.car_table.setItem(row_position, 5, QTableWidgetItem(formatted_price))

            # Format the fuel capacity
            formatted_capacity = f"{car.fuel_capacity}L"  # fuel_capacity
            self.car_table.setItem(row_position, 6, QTableWidgetItem(formatted_capacity))

            # Display the status
            status_item = QTableWidgetItem(car.status)  # status
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
            if car.status == "Đã bán":
                status_item.setBackground(QColor("#43BF5E"))
                sold_count += 1
            elif car.status == "Chưa bán":
                status_item.setBackground(QColor("#8E8EE9"))
                not_sold_count += 1
            elif car.status == "Đặt cọc":
                status_item.setBackground(QColor("#E9938E"))
                reserved_count += 1
            else:
                status_item.setBackground(QColor("#09AD90"))
                pending_count += 1
            self.car_table.setItem(row_position, 7, status_item)

            # Add buttons for details, edit, delete with icons
            info_button = QPushButton()
            info_button.setIcon(QIcon("../img/info.svg"))
            info_button.setStyleSheet("background-color: transparent;")
            info_button.clicked.connect(lambda _, car_id=car.id: self.show_car_info(car_id))
            self.car_table.setCellWidget(row_position, 8, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon("../img/edit.svg"))
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.clicked.connect(lambda _, car_id=car.id: self.edit_car(car_id))
            self.car_table.setCellWidget(row_position, 9, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("../img/delete.svg"))
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.clicked.connect(lambda _, car_id=car.id: self.delete_car(car_id))
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

        # Update the summary labels
        self.summary_label.setText(f"Đã bán: {sold_count}   Chưa bán: {not_sold_count}  Chờ mở bán: {pending_count}   Đặt cọc: {reserved_count}")

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
