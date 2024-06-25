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
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        header = QLabel("Danh sách đại lý")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        self.layout.addWidget(header)

        self.button_layout = QHBoxLayout()
        self.add_dealer_button = QPushButton("+   Thêm đại lý")
        self.add_dealer_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_dealer_button.setFixedSize(150, 40)
        self.add_dealer_button.clicked.connect(self.add_dealer)
        self.add_dealer_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        self.button_layout.addWidget(self.add_dealer_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addLayout(self.button_layout)

        self.dealer_table = QTableWidget()
        self.dealer_table.setColumnCount(6)
        self.dealer_table.setHorizontalHeaderLabels(["ID", "Tên", "Địa chỉ", "Số điện thoại", "Email", "Thao tác"])
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

        for dealer in dealers:
            row_position = self.dealer_table.rowCount()
            self.dealer_table.insertRow(row_position)
            self.dealer_table.setItem(row_position, 0, QTableWidgetItem(str(dealer.id)))
            self.dealer_table.setItem(row_position, 1, QTableWidgetItem(dealer.name))
            self.dealer_table.setItem(row_position, 2, QTableWidgetItem(dealer.address))
            self.dealer_table.setItem(row_position, 3, QTableWidgetItem(dealer.phone))
            self.dealer_table.setItem(row_position, 4, QTableWidgetItem(dealer.email))

            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(0)

            button_size = 40

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
            self.dealer_table.setCellWidget(row_position, 5, action_widget)

        self.adjust_column_widths()

    def adjust_column_widths(self):
        header = self.dealer_table.horizontalHeader()
        for column in range(self.dealer_table.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
            width = header.sectionSize(column)
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Interactive)
            self.dealer_table.setColumnWidth(column, width + 20)

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
                                f"Số điện thoại: {dealer.phone}\nEmail: {dealer.email}")

class DealerForm(QDialog):
    def __init__(self, dealer=None):
        super().__init__()
        self.dealer = dealer
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dealer Form")
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit(self.dealer.name if self.dealer else "")
        self.address_input = QLineEdit(self.dealer.address if self.dealer else "")
        self.phone_input = QLineEdit(self.dealer.phone if self.dealer else "")
        self.email_input = QLineEdit(self.dealer.email if self.dealer else "")

        self.form_layout.addRow("Name", self.name_input)
        self.form_layout.addRow("Address", self.address_input)
        self.form_layout.addRow("Phone", self.phone_input)
        self.form_layout.addRow("Email", self.email_input)

        self.layout.addLayout(self.form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def get_dealer_data(self):
        return {
            "name": self.name_input.text(),
            "address": self.address_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text()
        }