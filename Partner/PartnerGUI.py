# PartnerGUI.py
import os
import sqlite3

from PyQt6.QtWidgets import*
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from Partner.Partner import Partner

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info_icon_path = os.path.join(base_dir, "img", "img_crud", "info.svg")
edit_icon_path = os.path.join(base_dir, "img", "img_crud", "edit.svg")
delete_icon_path = os.path.join(base_dir, "img", "img_crud", "delete.svg")

class PartnerListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("Danh sách đối tác")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        layout.addWidget(header)

        self.button_layout = QHBoxLayout()

        # ComboBox for Country Filter
        self.country_filter = QComboBox()
        self.country_filter.addItem("Tất cả")
        self.country_filter.addItems(self.get_all_countries())
        self.country_filter.currentTextChanged.connect(self.load_partners)
        self.button_layout.addWidget(QLabel("Lọc theo quốc gia:"))
        self.button_layout.addWidget(self.country_filter)

        # ComboBox for Sorting
        self.sort_order = QComboBox()
        self.sort_order.addItem("Năm thành lập tăng dần")
        self.sort_order.addItem("Năm thành lập giảm dần")
        self.sort_order.currentTextChanged.connect(self.load_partners)
        self.button_layout.addWidget(QLabel("Sắp xếp theo:"))
        self.button_layout.addWidget(self.sort_order)

        self.add_partner_button = QPushButton("+   Thêm đối tác")
        self.add_partner_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_partner_button.setFixedSize(150, 40)
        self.add_partner_button.clicked.connect(self.add_partner)
        self.add_partner_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        self.button_layout.addWidget(self.add_partner_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(self.button_layout)

        self.partner_table = QTableWidget()
        self.partner_table.setColumnCount(8)
        self.partner_table.setHorizontalHeaderLabels(["Partner ID", "Name", "Country", "Founded Year", "Description", "", "", ""])
        self.partner_table.verticalHeader().setVisible(False)
        self.partner_table.horizontalHeader().setStretchLastSection(True)
        self.partner_table.setAlternatingRowColors(True)
        self.partner_table.setStyleSheet("""
            QHeaderView::section { background-color: #09AD90; color: white; font-size: 16px;  font-weight: bold; font-family: Roboto;}
            QTableWidget::item { font-size: 30px; font-family: Roboto; }
        """)
        layout.addWidget(self.partner_table)

        self.setLayout(layout)
        self.load_partners()

    def get_all_countries(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT country FROM Partner')
        countries = [row[0] for row in cursor.fetchall()]
        conn.close()
        return countries

    def load_partners(self):
        self.partner_table.setRowCount(0)
        country = self.country_filter.currentText()
        sort_order = self.sort_order.currentText()

        if country == "Tất cả":
            partners = Partner.get_all_partners_sorted_by_year(ascending=(sort_order == "Năm thành lập tăng dần"))
        else:
            partners = Partner.get_partners_by_country(country)
            partners = sorted(partners, key=lambda x: x.founded_year, reverse=(sort_order == "Năm thành lập giảm dần"))

        for partner in partners:
            row_position = self.partner_table.rowCount()
            self.partner_table.insertRow(row_position)
            self.partner_table.setItem(row_position, 0, QTableWidgetItem(str(partner.id)))
            self.partner_table.setItem(row_position, 1, QTableWidgetItem(partner.name))
            self.partner_table.setItem(row_position, 2, QTableWidgetItem(partner.country))
            self.partner_table.setItem(row_position, 3, QTableWidgetItem(str(partner.founded_year)))
            self.partner_table.setItem(row_position, 4, QTableWidgetItem(partner.description))

            # Center align ID column
            self.partner_table.item(row_position, 0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            info_button = QPushButton()
            info_button.setIcon(QIcon(info_icon_path))
            info_button.setStyleSheet("background-color: transparent;")
            info_button.setMinimumWidth(50)
            info_button.clicked.connect(lambda _, partner_id=partner.id: self.show_partner_info(partner_id))
            self.partner_table.setCellWidget(row_position, 5, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.setMinimumWidth(50)
            edit_button.clicked.connect(lambda _, partner_id=partner.id: self.edit_partner(partner_id))
            self.partner_table.setCellWidget(row_position, 6, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setMinimumWidth(50)
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.clicked.connect(lambda _, partner_id=partner.id: self.delete_partner(partner_id))
            self.partner_table.setCellWidget(row_position, 7, delete_button)

        self.partner_table.resizeColumnsToContents()

    def add_partner(self):
        dialog = PartnerAddDialog(self)
        if dialog.exec():
            self.load_partners()

    def delete_partner(self, partner_id):
        reply = QMessageBox.question(self, 'Xác nhận xóa',
                                     f"Bạn có chắc chắn muốn xóa đối tác có ID '{partner_id}' không?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            Partner.delete(partner_id)
            self.load_partners()

    def show_partner_info(self, partner_id):
        dialog = PartnerInfoDialog(partner_id, self)
        dialog.exec()

    def edit_partner(self, partner_id):
        dialog = PartnerEditDialog(partner_id, self)
        if dialog.exec():
            self.load_partners()


class PartnerEditDialog(QDialog):
    def __init__(self, partner_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin đối tác")
        self.partner_id = partner_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        partner = Partner.get_partner_by_id(self.partner_id)

        self.name_edit = QLineEdit(partner.name)
        self.country_edit = QLineEdit(partner.country)
        self.founded_year_edit = QLineEdit(str(partner.founded_year))
        self.description_edit = QLineEdit(partner.description)

        layout.addWidget(QLabel("Tên đối tác:"), 1, 0)
        layout.addWidget(self.name_edit, 1, 1)
        layout.addWidget(QLabel("Quốc gia:"), 2, 0)
        layout.addWidget(self.country_edit, 2, 1)
        layout.addWidget(QLabel("Năm thành lập:"), 3, 0)
        layout.addWidget(self.founded_year_edit, 3, 1)
        layout.addWidget(QLabel("Mô tả:"), 4, 0)
        layout.addWidget(self.description_edit, 4, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        save_button = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box, 5, 0, 1, 2)

    def accept(self):
        partner = Partner(
            self.partner_id,
            self.name_edit.text(),
            self.country_edit.text(),
            int(self.founded_year_edit.text()),
            self.description_edit.text()
        )
        partner.update()
        super().accept()

class PartnerInfoDialog(QDialog):
    def __init__(self, partner_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin đối tác")
        self.partner_id = partner_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        partner = Partner.get_partner_by_id(self.partner_id)

        layout.addWidget(QLabel("Tên đối tác:"), 1, 0)
        layout.addWidget(QLabel(partner.name), 1, 1)
        layout.addWidget(QLabel("Quốc gia:"), 2, 0)
        layout.addWidget(QLabel(partner.country), 2, 1)
        layout.addWidget(QLabel("Năm thành lập:"), 3, 0)
        layout.addWidget(QLabel(str(partner.founded_year)), 3, 1)
        layout.addWidget(QLabel("Mô tả:"), 4, 0)
        layout.addWidget(QLabel(partner.description), 4, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        layout.addWidget(self.button_box, 5, 0, 1, 2)

class PartnerAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm đối tác mới")
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        self.name_edit = QLineEdit()
        self.country_edit = QLineEdit()
        self.founded_year_edit = QLineEdit()
        self.description_edit = QLineEdit()

        layout.addWidget(QLabel("Tên đối tác:"), 1, 0)
        layout.addWidget(self.name_edit, 1, 1)
        layout.addWidget(QLabel("Quốc gia:"), 2, 0)
        layout.addWidget(self.country_edit, 2, 1)
        layout.addWidget(QLabel("Năm thành lập:"), 3, 0)
        layout.addWidget(self.founded_year_edit, 3, 1)
        layout.addWidget(QLabel("Mô tả:"), 4, 0)
        layout.addWidget(self.description_edit, 4, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        save_button = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box, 5, 0, 1, 2)

    def accept(self):
        partner = Partner(
            None,
            self.name_edit.text(),
            self.country_edit.text(),
            int(self.founded_year_edit.text()),
            self.description_edit.text()
        )
        partner.save()
        super().accept()
