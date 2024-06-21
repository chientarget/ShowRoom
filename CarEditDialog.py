import sys
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy, QDialog, QFormLayout, QLineEdit, QDialogButtonBox

def get_cars():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, produced_year, color, car_type, warranty_year, price, status FROM Car')
    cars = cursor.fetchall()
    conn.close()
    return cars

def get_car_details(car_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, produced_year, color, car_type, warranty_year, price, status FROM Car WHERE id = ?', (car_id,))
    car = cursor.fetchone()
    conn.close()
    return car

def update_car(car_id, name, produced_year, color, car_type, warranty_year, price, status):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Car
        SET name = ?, produced_year = ?, color = ?, car_type = ?, warranty_year = ?, price = ?, status = ?
        WHERE id = ?
    ''', (name, produced_year, color, car_type, warranty_year, price, status, car_id))
    conn.commit()
    conn.close()

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
        self.produced_year_edit = QLineEdit(str(car_details[1]))
        self.color_edit = QLineEdit(car_details[2])
        self.car_type_edit = QLineEdit(car_details[3])
        self.warranty_year_edit = QLineEdit(car_details[4])
        self.price_edit = QLineEdit(car_details[5])
        self.status_edit = QLineEdit(car_details[6])

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
        update_car(
            self.car_id,
            self.name_edit.text(),
            int(self.produced_year_edit.text()),
            self.color_edit.text(),
            self.car_type_edit.text(),
            self.warranty_year_edit.text(),
            self.price_edit.text(),
            self.status_edit.text()
        )
        super().accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Showroom Vinfast")
        self.setGeometry(100, 100, 1500, 900)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("<span style='color: #2DB4AE;'>Showroom</span><span style='color: #FBCE49;'> VinFast</span>")
        title.setFont(QFont('MulishRoman', 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2DB4AE;")
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

        content = QWidget()
        content_layout = QVBoxLayout(content)

        header = QLabel("Danh sách xe")
        header.setFont(QFont('MulishRoman', 16, QFont.Weight.Bold))
        content_layout.addWidget(header)

        self.car_table = QTableWidget()
        self.car_table.setColumnCount(10)
        self.car_table.setHorizontalHeaderLabels(["Tên xe", "Năm sản xuất", "Màu sắc", "Loại xe", "Bảo hành", "Giá", "Trạng thái", "Thông tin", "Sửa", "Xóa"])
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
            self.car_table.setItem(row_position, 0, QTableWidgetItem(car[1]))
            self.car_table.setItem(row_position, 1, QTableWidgetItem(str(car[2])))
            self.car_table.setItem(row_position, 2, QTableWidgetItem(car[3]))
            self.car_table.setItem(row_position, 3, QTableWidgetItem(car[4]))
            self.car_table.setItem(row_position, 4, QTableWidgetItem(car[5]))
            self.car_table.setItem(row_position, 5, QTableWidgetItem(car[6]))
            status_item = QTableWidgetItem(car[7])
            if car[7] == "Đã bán":
                status_item.setForeground(Qt.GlobalColor.green)
            elif car[7] == "Chưa bán":
                status_item.setForeground(Qt.GlobalColor.blue)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.car_table.setItem(row_position, 6, status_item)

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

        for col in range(self.car_table.columnCount() - 3):
            current_width = self.car_table.columnWidth(col)
            self.car_table.setColumnWidth(col, current_width + 20)

        button_columns = [7, 8, 9]
        for col in button_columns:
            self.car_table.setColumnWidth(col, 40)

    def add_car(self):
        pass

    def delete_car(self, car_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Car WHERE id = ?', (car_id,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Deleted", f"Car ID '{car_id}' has been deleted.")
        self.load_cars()

    def show_car_info(self, car_id):
        car_details = get_car_details(car_id)
        QMessageBox.information(self, "Thông tin xe", f"Thông tin chi tiết của xe:\n\nTên xe: {car_details[0]}\nLoại xe: {car_details[1]}\nNăm sản xuất: {car_details[2]}\nMàu sắc: {car_details[3]}\nBảo hành: {car_details[4]}\nGiá: {car_details[5]}\nTrạng thái: {car_details[6]}")

    def edit_car(self, car_id):
        dialog = CarEditDialog(car_id, self)
        if dialog.exec():
            self.load_cars()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QPushButton { 
            padding: 10px;
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
