import os
import sqlite3

from PyQt6.QtWidgets import*
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from Order.Order import Order

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info_icon_path = os.path.join(base_dir, "img", "img_crud", "info.svg")
edit_icon_path = os.path.join(base_dir, "img", "img_crud", "edit.svg")
delete_icon_path = os.path.join(base_dir, "img", "img_crud", "delete.svg")


def format_price(price):
    if price >= 1_000_000_000:
        formatted_price = f"{price / 1_000_000_000:.2f} Tỷ"
    elif price >= 1_000_000:
        formatted_price = f"{price / 1_000_000:.0f} Triệu"
    else:
        formatted_price = f"{price:,} vnđ"
    return formatted_price
class OrderListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("Danh sách đơn hàng")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        layout.addWidget(header)

        self.button_layout = QHBoxLayout()
        self.add_order_button = QPushButton("+   Thêm đơn hàng")
        self.add_order_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_order_button.setFixedSize(150, 40)
        self.add_order_button.clicked.connect(self.add_order)
        self.add_order_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        self.button_layout.addWidget(self.add_order_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(self.button_layout)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(12)
        self.order_table.setHorizontalHeaderLabels([
            "Mã ĐH", "Khách hàng", "Xe", "Giá", "Đại lý",
            "Nhân viên", "Chức vụ", "SĐT KH", "Email KH", "VIN", "Ngày tạo", "Thao tác"
        ])
        self.order_table.verticalHeader().setVisible(False)
        self.order_table.horizontalHeader().setStretchLastSection(True)
        self.order_table.setAlternatingRowColors(True)
        self.order_table.setStyleSheet("""
            QHeaderView::section { background-color: #09AD90; color: white; font-size: 16px;  font-weight: bold; font-family: Roboto;}
            QTableWidget::item { font-size: 30px; font-family: Roboto; }
        """)
        layout.addWidget(self.order_table)

        self.setLayout(layout)
        self.load_orders()

    def load_orders(self):
        self.order_table.setRowCount(0)
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT o.id, c.name, car.name, o.total_price, d.name, 
                   hr.name, r.name, c.phone, c.email, car.vin, o.creation_time
            FROM "Order" o
            JOIN Customer c ON o.customer_id = c.id
            JOIN Car car ON o.car_id = car.id
            JOIN Human_resources hr ON o.human_resource_id = hr.id
            JOIN Dealer d ON o.dealer_id = d.id
            JOIN Role r ON hr.role_id = r.id
        ''')

        orders = cursor.fetchall()
        conn.close()

        for row_number, order in enumerate(orders):
            self.order_table.insertRow(row_number)
            for column_number, data in enumerate(order):
                if column_number == 0:
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.order_table.setItem(row_number, column_number, item)
                else:
                    self.order_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(2)

            info_button = QPushButton()
            info_button.setIcon(QIcon(info_icon_path))
            info_button.setStyleSheet("background-color: transparent;")

            info_button.setToolTip("View Details")
            info_button.clicked.connect(lambda _, order_id=order[0]: self.show_order_info(order_id))
            action_layout.addWidget(info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setToolTip("Edit Order")
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.clicked.connect(lambda _, order_id=order[0]: self.edit_order(order_id))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.setToolTip("Delete Order")
            delete_button.clicked.connect(lambda _, order_id=order[0]: self.delete_order(order_id))
            action_layout.addWidget(delete_button)

            self.order_table.setColumnWidth(0, 80)
            self.order_table.setColumnWidth(3, 80)
            self.order_table.setColumnWidth(9, 69)
            self.order_table.setCellWidget(row_number, 11, action_widget)

    def add_order(self):
        dialog = OrderAddDialog(self)
        if dialog.exec():
            self.load_orders()

    def delete_order(self, order_id):
        Order.delete(order_id)
        QMessageBox.information(self, "Deleted", f"Order ID '{order_id}' has been deleted.")
        self.load_orders()

    def show_order_info(self, order_id):
        dialog = OrderInfoDialog(order_id, self)
        dialog.exec()

    def edit_order(self, order_id):
        dialog = OrderEditDialog(order_id, self)
        if dialog.exec():
            self.load_orders()



class OrderEditDialog(QDialog):
    def __init__(self, order_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chỉnh sửa đơn hàng")
        self.order_id = order_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()

        # Fetch current order data
        cursor.execute('''
            SELECT o.human_resource_id
            FROM "Order" o
            WHERE o.id = ?
        ''', (self.order_id,))
        order = cursor.fetchone()

        # Fetch options for dropdowns
        cursor.execute("SELECT id, name FROM Human_resources")
        staff = cursor.fetchall()

        conn.close()

        form_layout = QGridLayout()

        self.staff_combo = QComboBox()
        self.staff_combo.addItems([f"{s[0]} - {s[1]}" for s in staff])
        self.staff_combo.setCurrentIndex([s[0] for s in staff].index(order[0]))
        form_layout.addWidget(QLabel("Nhân viên bán hàng:"), 0, 0)
        form_layout.addWidget(self.staff_combo, 0, 1)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)


        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        human_resource_id = int(self.staff_combo.currentText().split(' - ')[0])

        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE "Order"
            SET human_resource_id = ?
            WHERE id = ?
        ''', (human_resource_id, self.order_id))
        conn.commit()
        conn.close()

        super().accept()


class OrderInfoDialog(QDialog):
    def __init__(self, order_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chi tiết đơn hàng")
        self.order_id = order_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.id, c.name, c.phone, c.email, 
                   car.name, car.produced_year, car.color, 
                   o.total_price, d.name, hr.name, r.name
            FROM "Order" o
            JOIN Customer c ON o.customer_id = c.id
            JOIN Car car ON o.car_id = car.id
            JOIN Human_resources hr ON o.human_resource_id = hr.id
            JOIN Dealer d ON o.dealer_id = d.id
            JOIN Role r ON hr.role_id = r.id
            WHERE o.id = ?
        ''', (self.order_id,))
        order = cursor.fetchone()
        conn.close()

        if order:
            info_layout = QGridLayout()
            info_layout.addWidget(QLabel("Mã đơn hàng:"), 0, 0)
            info_layout.addWidget(QLabel(str(order[0])), 0, 1)
            info_layout.addWidget(QLabel("Tên khách hàng:"), 0, 2)
            info_layout.addWidget(QLabel(order[1]), 0, 3)
            info_layout.addWidget(QLabel("Số điện thoại:"), 1, 0)
            info_layout.addWidget(QLabel(order[2]), 1, 1)
            info_layout.addWidget(QLabel("Email:"), 1, 2)
            info_layout.addWidget(QLabel(order[3]), 1, 3)
            info_layout.addWidget(QLabel("Xe:"), 2, 0)
            info_layout.addWidget(QLabel(f"{order[4]} {order[5]}"), 2, 1)
            info_layout.addWidget(QLabel("Màu sắc:"), 2, 2)
            info_layout.addWidget(QLabel(order[6]), 2, 3)
            info_layout.addWidget(QLabel("Giá bán:"), 3, 0)
            info_layout.addWidget(QLabel(f"{order[7]:,} VND"), 3, 1)
            info_layout.addWidget(QLabel("Đại lý:"), 3, 2)
            info_layout.addWidget(QLabel(order[8]), 3, 3)
            info_layout.addWidget(QLabel("Nhân viên bán hàng:"), 4, 0)
            info_layout.addWidget(QLabel(order[9]), 4, 1)
            info_layout.addWidget(QLabel("Chức vụ nhân viên:"), 4, 2)
            info_layout.addWidget(QLabel(order[10]), 4, 3)

            layout.addLayout(info_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)


class OrderAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm đơn hàng mới")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()

        # Fetch options for dropdowns
        cursor.execute("SELECT id, name FROM Customer")
        customers = cursor.fetchall()
        cursor.execute("SELECT id, name, produced_year FROM Car WHERE status = 'Chưa bán' OR status = 'Đặt cọc'")
        cars = cursor.fetchall()
        cursor.execute("SELECT id, name FROM Human_resources")
        staff = cursor.fetchall()
        cursor.execute("SELECT id, name FROM Dealer")
        dealers = cursor.fetchall()

        conn.close()

        form_layout = QGridLayout()

        self.customer_combo = QComboBox()
        self.customer_combo.addItems([f"{c[0]} - {c[1]}" for c in customers])
        form_layout.addWidget(QLabel("Khách hàng:"), 0, 0)
        form_layout.addWidget(self.customer_combo, 0, 1)

        self.dealer_combo = QComboBox()
        self.dealer_combo.addItems([f"{d[0]} - {d[1]}" for d in dealers])
        self.dealer_combo.currentIndexChanged.connect(self.update_car_list)
        form_layout.addWidget(QLabel("Đại lý:"), 1, 0)
        form_layout.addWidget(self.dealer_combo, 1, 1)

        self.car_combo = QComboBox()
        self.car_combo.currentIndexChanged.connect(self.update_price)
        form_layout.addWidget(QLabel("Xe:"), 2, 0)
        form_layout.addWidget(self.car_combo, 2, 1)

        self.price_edit = QLineEdit()
        self.price_edit.setReadOnly(True)
        form_layout.addWidget(QLabel("Giá bán:"), 3, 0)
        form_layout.addWidget(self.price_edit, 3, 1)

        self.staff_combo = QComboBox()
        self.staff_combo.addItems([f"{s[0]} - {s[1]}" for s in staff])
        form_layout.addWidget(QLabel("Nhân viên bán hàng:"), 4, 0)
        form_layout.addWidget(self.staff_combo, 4, 1)

        self.purchase_type = QButtonGroup(self)
        self.purchase_radio = QRadioButton("Đặt mua")
        self.purchase_radio.setChecked(True)
        self.reserve_radio = QRadioButton("Đặt cọc")
        self.purchase_type.addButton(self.purchase_radio)
        self.purchase_type.addButton(self.reserve_radio)
        form_layout.addWidget(self.purchase_radio, 5, 0)
        form_layout.addWidget(self.reserve_radio, 5, 1)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def update_staff_list(self):
        dealer_id = int(self.dealer_combo.currentText().split(' - ')[0])
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hr.id, hr.name
            FROM Human_resources hr
        """)
        staff = cursor.fetchall()
        conn.close()

        self.staff_combo.clear()
        self.staff_combo.addItems([f"{s[0]} - {s[1]}" for s in staff])

    def update_car_list(self):
        dealer_id = int(self.dealer_combo.currentText().split(' - ')[0])
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name || ' ' || produced_year 
            FROM Car 
            WHERE dealer_id = ? AND (status = 'Chưa bán' OR status = 'Đặt cọc')
        """, (dealer_id,))
        cars = cursor.fetchall()
        conn.close()

        self.car_combo.clear()
        self.car_combo.addItems([f"{c[0]} - {c[1]}" for c in cars])
        self.update_price()
        self.update_staff_list()

    def update_price(self):
        if self.car_combo.currentText():
            car_id = int(self.car_combo.currentText().split(' - ')[0])
            conn = sqlite3.connect('showroom.db')
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM Car WHERE id = ?", (car_id,))
            price = cursor.fetchone()[0]
            conn.close()
            self.price_edit.setText(f"{price:,} VND")
        else:
            self.price_edit.clear()

    def accept(self):
        customer_id = int(self.customer_combo.currentText().split(' - ')[0])
        car_id = int(self.car_combo.currentText().split(' - ')[0])
        total_price = float(self.price_edit.text().replace(',', '').replace('VND', '').strip())
        human_resource_id = int(self.staff_combo.currentText().split(' - ')[0])
        dealer_id = int(self.dealer_combo.currentText().split(' - ')[0])
        purchase_type = self.purchase_radio.isChecked()

        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()

        # Check car status
        cursor.execute("SELECT status FROM Car WHERE id = ?", (car_id,))
        car_status = cursor.fetchone()[0]

        # Insert new order
        cursor.execute('''
            INSERT INTO "Order" (customer_id, car_id, total_price, human_resource_id, dealer_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, car_id, total_price, human_resource_id, dealer_id))

        # Update car status
        new_status = "Đặt cọc" if not purchase_type else "Đã bán"
        cursor.execute("UPDATE Car SET status = ? WHERE id = ?", (new_status, car_id))

        conn.commit()
        conn.close()

        super().accept()
