# partner_list.py
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from Partner.partner import Partner
from Partner.partner_forms import PartnerEditDialog, PartnerInfoDialog, PartnerAddDialog

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
        self.add_partner_button = QPushButton("+   Thêm đối tác")
        self.add_partner_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_partner_button.setFixedSize(150, 40)
        self.add_partner_button.clicked.connect(self.add_partner)
        self.add_partner_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        self.button_layout.addWidget(self.add_partner_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(self.button_layout)

        self.partner_table = QTableWidget()
        self.partner_table.setColumnCount(9)  # Add 3 columns for the buttons
        self.partner_table.setHorizontalHeaderLabels(["Partner ID", "Logo", "Name", "Country", "Founded Year", "Description", "", "", ""])
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

    def load_partners(self):
        self.partner_table.setRowCount(0)
        partners = Partner.get_all_partners()

        for partner in partners:
            row_position = self.partner_table.rowCount()
            self.partner_table.insertRow(row_position)
            self.partner_table.setItem(row_position, 0, QTableWidgetItem(str(partner.id)))
            self.partner_table.setItem(row_position, 1, QTableWidgetItem(partner.logo))
            self.partner_table.setItem(row_position, 2, QTableWidgetItem(partner.name))
            self.partner_table.setItem(row_position, 3, QTableWidgetItem(partner.country))
            self.partner_table.setItem(row_position, 4, QTableWidgetItem(str(partner.founded_year)))
            self.partner_table.setItem(row_position, 5, QTableWidgetItem(partner.description))

            # Add buttons for details, edit, delete with icons
            info_button = QPushButton()
            info_button.setIcon(QIcon(info_icon_path))
            info_button.setStyleSheet("background-color: transparent;")
            info_button.clicked.connect(lambda _, partner_id=partner.id: self.show_partner_info(partner_id))
            self.partner_table.setCellWidget(row_position, 6, info_button)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setStyleSheet("background-color: transparent;")
            edit_button.clicked.connect(lambda _, partner_id=partner.id: self.edit_partner(partner_id))
            self.partner_table.setCellWidget(row_position, 7, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setStyleSheet("background-color: transparent;")
            delete_button.clicked.connect(lambda _, partner_id=partner.id: self.delete_partner(partner_id))
            self.partner_table.setCellWidget(row_position, 8, delete_button)

        self.partner_table.resizeColumnsToContents()

    def add_partner(self):
        dialog = PartnerAddDialog(self)
        if dialog.exec():
            self.load_partners()

    def delete_partner(self, partner_id):
        Partner.delete(partner_id)
        QMessageBox.information(self, "Deleted", f"Partner ID '{partner_id}' has been deleted.")
        self.load_partners()

    def show_partner_info(self, partner_id):
        dialog = PartnerInfoDialog(partner_id, self)
        dialog.exec()

    def edit_partner(self, partner_id):
        dialog = PartnerEditDialog(partner_id, self)
        if dialog.exec():
            self.load_partners()
