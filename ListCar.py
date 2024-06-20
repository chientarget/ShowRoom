import sys
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy


# Database setup
def init_db():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            year INTEGER,
            color TEXT,
            size TEXT,
            engine TEXT,
            max_power TEXT,
            fuel_capacity TEXT,
            transmission TEXT,
            fuel_consumption TEXT,
            drivetrain TEXT,
            seats INTEGER,
            airbags INTEGER,
            warranty TEXT,
            price TEXT,
            dealer TEXT,
            status TEXT
        )
    ''')

    # Insert sample data
    sample_data = [
        ("VINFAST LUX A2.0", "Sedan", 2021, "Trắng", "4,973 x 1,900 x 1,464 mm", "2.0L", "228 HP", "70L", "Tự động 8 cấp", "8.5L/100km", "RWD", 5, 6, "5 năm", "2.114.000.000 VND", "Vinfast Dealer 1", "Đã bán"),
        ("VINFAST VF 9", "SUV", 2022, "Trắng", "5,120 x 2,000 x 1,721 mm", "Electric", "402 HP", "90 kWh", "Single-speed", "N/A", "AWD", 7, 6, "10 năm", "2.114.000.000 VND", "Vinfast Dealer 2", "Chưa bán"),
        ("VINFAST President", "SUV", 2022, "Trắng", "4,750 x 1,900 x 1,660 mm", "Electric", "402 HP", "90 kWh", "Single-speed", "N/A", "AWD", 5, 6, "10 năm", "2.114.000.000 VND", "Vinfast Dealer 3", "Đặt cọc")
    ]

    cursor.executemany('''
        INSERT INTO cars (name, type, year, color, size, engine, max_power, fuel_capacity, transmission, fuel_consumption, drivetrain, seats, airbags, warranty, price, dealer, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_data)

    conn.commit()
    conn.close()


def get_cars():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, type, year, color, warranty, price, status FROM cars')
    cars = cursor.fetchall()
    conn.close()
    return cars


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
        self.car_table.setHorizontalHeaderLabels(["Tên xe", "Loại xe", "Năm sản xuất", "Màu sắc", "Bảo hành", "Giá", "Trạng thái", "Thông tin", "Sửa", "Xóa"])
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
        cars = get_cars()
        for car in cars:
            row_position = self.car_table.rowCount()
            self.car_table.insertRow(row_position)
            self.car_table.setItem(row_position, 0, QTableWidgetItem(car[0]))
            self.car_table.setItem(row_position, 1, QTableWidgetItem(car[1]))
            self.car_table.setItem(row_position, 2, QTableWidgetItem(str(car[2])))
            self.car_table.setItem(row_position, 3, QTableWidgetItem(car[3]))
            self.car_table.setItem(row_position, 4, QTableWidgetItem(car[4]))
            self.car_table.setItem(row_position, 5, QTableWidgetItem(car[5]))
            status_item = QTableWidgetItem(car[6])
            if car[6] == "Đã bán":
                status_item.setForeground(Qt.GlobalColor.green)
            elif car[6] == "Chưa bán":
                status_item.setForeground(Qt.GlobalColor.blue)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.car_table.setItem(row_position, 6, status_item)

            # Add buttons for details, edit, delete with icons
            info_button = QPushButton()
            info_button.setIcon(QIcon("info.svg"))
            info_button.setFixedSize(30, 30)
            info_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            info_button.clicked.connect(lambda _, name=car[0]: self.show_car_info(name))
            self.car_table.setCellWidget(row_position, 7, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon("edit.svg"))
            edit_button.setFixedSize(30, 30)
            edit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            edit_button.clicked.connect(lambda _, name=car[0]: self.edit_car(name))
            self.car_table.setCellWidget(row_position, 8, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("delete.svg"))
            delete_button.setFixedSize(30, 30)
            delete_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            delete_button.clicked.connect(lambda _, name=car[0]: self.delete_car(name))
            self.car_table.setCellWidget(row_position, 9, delete_button)

        self.car_table.resizeColumnsToContents()

        # Adjust column widths to be slightly wider than content
        for col in range(self.car_table.columnCount() - 3):
            current_width = self.car_table.columnWidth(col)
            self.car_table.setColumnWidth(col, current_width + 20)

        # Ensure button columns are only as wide as the buttons
        button_columns = [7, 8, 9]
        for col in button_columns:
            self.car_table.setColumnWidth(col, 40)

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


if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QPushButton { 
            padding: 10px;
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
