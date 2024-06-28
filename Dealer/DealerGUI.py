import os
from PyQt6.QtWidgets import*
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from Dealer.Dealer import Dealer


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info_icon_path = os.path.join(base_dir, "img", "img_crud", "info.svg")
edit_icon_path = os.path.join(base_dir, "img", "img_crud", "edit.svg")
delete_icon_path = os.path.join(base_dir, "img", "img_crud", "delete.svg")


class DealerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.sort_order = Qt.SortOrder.DescendingOrder
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        header = QLabel("Danh sách đại lý")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        self.layout.addWidget(header)

        search_layout = QHBoxLayout()

        self.search_name_edit = QLineEdit()
        self.search_name_edit.setPlaceholderText("Tìm theo tên")
        self.search_name_edit.setFixedWidth(180)
        self.search_name_edit.textChanged.connect(self.load_dealers)
        search_layout.addWidget(self.search_name_edit)

        self.search_address_edit = QLineEdit()
        self.search_address_edit.setPlaceholderText("Tìm theo địa chỉ")
        self.search_address_edit.setFixedWidth(180)
        self.search_address_edit.textChanged.connect(self.load_dealers)
        search_layout.addWidget(self.search_address_edit)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.sort_button = QPushButton("Sắp xếp")
        self.sort_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.sort_button.setFixedHeight(50)
        self.sort_button.clicked.connect(self.sort_dealers)
        self.sort_button.setStyleSheet("padding: 10px 20px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 18px;")
        button_layout.addWidget(self.sort_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.add_dealer_button = QPushButton("+ Thêm đại lý")
        self.add_dealer_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_dealer_button.setFixedHeight(50)
        self.add_dealer_button.clicked.connect(self.add_dealer)
        self.add_dealer_button.setStyleSheet("padding: 10px 20px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 18px;")
        button_layout.addWidget(self.add_dealer_button, alignment=Qt.AlignmentFlag.AlignRight)

        search_layout.addLayout(button_layout)
        self.layout.addLayout(search_layout)

        self.dealer_table = QTableWidget()
        self.dealer_table.setColumnCount(10)  # Update to include new columns
        self.dealer_table.setHorizontalHeaderLabels(["ID", "Tên", "Địa chỉ", "Số điện thoại", "Email", "Doanh thu", "Số lượng xe", "Giờ đóng/mở cửa", "Nhân sự", "Thao tác"])
        self.dealer_table.verticalHeader().setVisible(False)
        self.dealer_table.setAlternatingRowColors(True)
        self.dealer_table.setStyleSheet("""
            QHeaderView::section { background-color: #09AD90; color: white; font-size: 16px; font-weight: bold; font-family: Roboto;}
            QTableWidget::item { font-size: 14px; font-family: Roboto; }
            QWidget { border: none; }
            QHBoxLayout { border: none; }
            QTableWidget::item:selected { background-color: #2DB4AE; }
        """)
        self.layout.addWidget(self.dealer_table)

        self.load_dealers()

    def load_dealers(self):
        self.dealer_table.setRowCount(0)
        dealers = Dealer.get_dealers()

        search_name = self.search_name_edit.text().lower()
        search_address = self.search_address_edit.text().lower()

        for dealer in dealers:
            if (search_name and search_name not in dealer.name.lower()) or \
               (search_address and search_address not in dealer.address.lower()):
                continue

            row_position = self.dealer_table.rowCount()
            self.dealer_table.insertRow(row_position)
            id_item = QTableWidgetItem(str(dealer.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dealer_table.setItem(row_position, 0, id_item)

            self.dealer_table.setItem(row_position, 1, QTableWidgetItem(dealer.name))
            self.dealer_table.setItem(row_position, 2, QTableWidgetItem(dealer.address))
            self.dealer_table.setItem(row_position, 3, QTableWidgetItem(dealer.phone))
            self.dealer_table.setItem(row_position, 4, QTableWidgetItem(dealer.email))

            revenue_item = QTableWidgetItem(Dealer.format_price(Dealer.get_dealer_revenue(dealer.id)))
            revenue_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.dealer_table.setItem(row_position, 5, revenue_item)

            car_count_item = QTableWidgetItem(str(Dealer.get_dealer_car_count(dealer.id)))
            car_count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dealer_table.setItem(row_position, 6, car_count_item)

            opening_hours = f"{dealer.open_time} - {dealer.close_time}"
            self.dealer_table.setItem(row_position, 7, QTableWidgetItem(opening_hours))

            employee_count_item = QTableWidgetItem(str(Dealer.get_dealer_employee_count(dealer.id)))
            employee_count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dealer_table.setItem(row_position, 8, employee_count_item)

            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(0)

            button_size = 35

            view_button = QPushButton()
            view_button.setIcon(QIcon(info_icon_path))
            view_button.setFixedSize(button_size, button_size)
            view_button.setStyleSheet("border: none; background-color: transparent; padding: 5px;")
            view_button.clicked.connect(lambda _, d=dealer: self.view_dealer_details(d))

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setFixedSize(button_size, button_size)
            edit_button.setStyleSheet("border: none; background-color: transparent; padding: 5px;")
            edit_button.clicked.connect(lambda _, d=dealer: self.edit_dealer(d))

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setFixedSize(button_size, button_size)
            delete_button.setStyleSheet("border: none; background-color: transparent; padding: 5px;")
            delete_button.clicked.connect(lambda _, d=dealer: self.delete_dealer(d))

            action_layout.addWidget(view_button)
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.dealer_table.setCellWidget(row_position, 9, action_widget)

        self.adjust_column_widths()

    def adjust_column_widths(self):
        header = self.dealer_table.horizontalHeader()
        for column in range(self.dealer_table.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
            width = header.sectionSize(column)
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Interactive)
            self.dealer_table.setColumnWidth(column, width + 20)

    def sort_dealers(self):
        self.sort_order = Qt.SortOrder.AscendingOrder if self.sort_order == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder
        self.dealer_table.sortItems(5, self.sort_order)

    def add_dealer(self):
        form = DealerForm()
        if form.exec():
            data = form.get_dealer_data()
            dealer = Dealer(**data)
            dealer.add_dealer()
            self.load_dealers()

    def edit_dealer(self, dealer):
        form = DealerForm(dealer)
        if form.exec():
            data = form.get_dealer_data()
            dealer.name = data["name"]
            dealer.address = data["address"]
            dealer.phone = data["phone"]
            dealer.email = data["email"]
            dealer.open_time = data["open_time"]
            dealer.close_time = data["close_time"]
            dealer.update_dealer()
            self.load_dealers()

    def delete_dealer(self, dealer):
        reply = QMessageBox.question(self, 'Xác nhận xóa', f'Bạn có chắc chắn muốn xóa đại lý "{dealer.name}"?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            Dealer.delete_dealer(dealer.id)
            self.load_dealers()

    def view_dealer_details(self, dealer):
        QMessageBox.information(self, "Thông tin đại lý",
                                f"ID: {dealer.id}\nTên: {dealer.name}\nĐịa chỉ: {dealer.address}\n"
                                f"Số điện thoại: {dealer.phone}\nEmail: {dealer.email}\nGiờ đóng/mở cửa: {dealer.open_time} - {dealer.close_time}")

class DealerForm(QDialog):
    def __init__(self, dealer=None):
        super().__init__()
        self.dealer = dealer
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Form Đại lý")
        self.layout = QGridLayout(self)

        self.name_input = QLineEdit(self.dealer.name if self.dealer else "")
        self.address_input = QLineEdit(self.dealer.address if self.dealer else "")
        self.phone_input = QLineEdit(self.dealer.phone if self.dealer else "")
        self.email_input = QLineEdit(self.dealer.email if self.dealer else "")
        self.open_time_input = QLineEdit(self.dealer.open_time if self.dealer else "")
        self.close_time_input = QLineEdit(self.dealer.close_time if self.dealer else "")

        self.layout.addWidget(QLabel("Tên"), 0, 0)
        self.layout.addWidget(self.name_input, 0, 1)
        self.layout.addWidget(QLabel("Địa chỉ"), 0, 2)
        self.layout.addWidget(self.address_input, 0, 3)
        self.layout.addWidget(QLabel("Số điện thoại"), 1, 0)
        self.layout.addWidget(self.phone_input, 1, 1)
        self.layout.addWidget(QLabel("Email"), 1, 2)
        self.layout.addWidget(self.email_input, 1, 3)
        self.layout.addWidget(QLabel("Giờ mở cửa"), 2, 0)
        self.layout.addWidget(self.open_time_input, 2, 1)
        self.layout.addWidget(QLabel("Giờ đóng cửa"), 2, 2)
        self.layout.addWidget(self.close_time_input, 2, 3)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        ok_button = self.button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        self.layout.addWidget(self.button_box, 3, 0, 1, 4)
        self.setLayout(self.layout)

    def get_dealer_data(self):
        return {
            "name": self.name_input.text(),
            "address": self.address_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text(),
            "open_time": self.open_time_input.text(),
            "close_time": self.close_time_input.text()
        }


