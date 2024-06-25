# PartnerGUI.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Partner import Partner
from PartnerView import PartnerEditDialog

class PartnerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Quản lý đối tác")
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên đối tác", "Địa chỉ", "Số điện thoại", "Email"
        ])
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        self.view_button = QPushButton("Xem thông tin")
        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")
        button_layout.addWidget(self.view_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Load data
        self.load_data()

        # Connect buttons
        self.view_button.clicked.connect(self.view_partner)
        self.edit_button.clicked.connect(self.edit_partner)
        self.delete_button.clicked.connect(self.delete_partner)

    def load_data(self):
        partners = Partner.get_all_partners()
        self.table.setRowCount(len(partners))
        for row_idx, partner in enumerate(partners):
            for col_idx, value in enumerate(partner):
                item = QTableWidgetItem(str(value))
                if col_idx == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def view_partner(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            partner_id = int(self.table.item(selected_row, 0).text())
            dialog = PartnerEditDialog(partner_id, view_only=True)
            dialog.exec()

    def edit_partner(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            partner_id = int(self.table.item(selected_row, 0).text())
            dialog = PartnerEditDialog(partner_id)
            dialog.exec()
            self.load_data()

    def delete_partner(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            partner_id = int(self.table.item(selected_row, 0).text())
            Partner.delete_partner(partner_id)
            self.load_data()
