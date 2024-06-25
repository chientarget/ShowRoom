# DealerGUI.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Dealer import Dealer
from DealerView import DealerEditDialog

class DealerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Quản lý đại lý")
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên đại lý", "Địa chỉ", "Số điện thoại", "Email"
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
        self.view_button.clicked.connect(self.view_dealer)
        self.edit_button.clicked.connect(self.edit_dealer)
        self.delete_button.clicked.connect(self.delete_dealer)

    def load_data(self):
        dealers = Dealer.get_all_dealers()
        self.table.setRowCount(len(dealers))
        for row_idx, dealer in enumerate(dealers):
            for col_idx, value in enumerate(dealer):
                item = QTableWidgetItem(str(value))
                if col_idx == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def view_dealer(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            dealer_id = int(self.table.item(selected_row, 0).text())
            dialog = DealerEditDialog(dealer_id, view_only=True)
            dialog.exec()

    def edit_dealer(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            dealer_id = int(self.table.item(selected_row, 0).text())
            dialog = DealerEditDialog(dealer_id)
            dialog.exec()
            self.load_data()

    def delete_dealer(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            dealer_id = int(self.table.item(selected_row, 0).text())
            Dealer.delete_dealer(dealer_id)
            self.load_data()
