import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from Human_resources.human_resources import HumanResource
from Human_resources.human_resources_forms import HumanResourceEditDialog, HumanResourceInfoDialog, HumanResourceAddDialog

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info_icon_path = os.path.join(base_dir, "img", "img_crud", "info.svg")
edit_icon_path = os.path.join(base_dir, "img", "img_crud", "edit.svg")
delete_icon_path = os.path.join(base_dir, "img", "img_crud", "delete.svg")

class HumanResourcesListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        header = QLabel("Danh sách nhân viên")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        self.main_layout.addWidget(header)

        self.button_layout = QHBoxLayout()
        self.add_human_resource_button = QPushButton("+   Thêm nhân viên")
        self.add_human_resource_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_human_resource_button.setFixedSize(150, 40)
        self.add_human_resource_button.clicked.connect(self.add_human_resource)
        self.add_human_resource_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        self.button_layout.addWidget(self.add_human_resource_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addLayout(self.button_layout)

        self.human_resource_table = QTableWidget()
        self.human_resource_table.setColumnCount(9)
        self.human_resource_table.setHorizontalHeaderLabels(["ID", "Username", "Name", "Phone", "Email", "Address", "Gender", "Role", "Actions"])
        self.human_resource_table.verticalHeader().setVisible(False)
        self.human_resource_table.horizontalHeader().setStretchLastSection(True)
        self.human_resource_table.setAlternatingRowColors(True)
        self.human_resource_table.setStyleSheet("""
            QHeaderView::section { background-color: #09AD90; color: white; font-size: 16px;  font-weight: bold; font-family: Roboto;}
            QTableWidget::item { font-size: 14px; font-family: Roboto; }
            QWidget { border: none; }
            QHBoxLayout { border: none; }
            QTableWidget::item:selected { background-color: #2DB4AE; }
        """)
        self.main_layout.addWidget(self.human_resource_table)

        self.setLayout(self.main_layout)
        self.load_human_resources()

    def load_human_resources(self):
        self.human_resource_table.setRowCount(0)
        human_resources = HumanResource.get_all_human_resource()

        for hr in human_resources:
            row_position = self.human_resource_table.rowCount()
            self.human_resource_table.insertRow(row_position)
            self.human_resource_table.setItem(row_position, 0, QTableWidgetItem(str(hr[0])))
            self.human_resource_table.setItem(row_position, 1, QTableWidgetItem(hr[1]))
            self.human_resource_table.setItem(row_position, 2, QTableWidgetItem(hr[3]))
            self.human_resource_table.setItem(row_position, 3, QTableWidgetItem(hr[4]))
            self.human_resource_table.setItem(row_position, 4, QTableWidgetItem(hr[5]))
            self.human_resource_table.setItem(row_position, 5, QTableWidgetItem(hr[6]))
            self.human_resource_table.setItem(row_position, 6, QTableWidgetItem("Male" if hr[7] else "Female"))
            self.human_resource_table.setItem(row_position, 7, QTableWidgetItem(HumanResource.get_role_name(hr[8])))

            # Add action buttons
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(0)

            button_size = 40

            info_button = QPushButton()
            info_button.setIcon(QIcon(info_icon_path))
            info_button.setFixedSize(button_size, button_size)
            info_button.setStyleSheet("border: none; background-color: transparent; padding: 5px;")
            info_button.clicked.connect(lambda _, hr_id=hr[0]: self.show_human_resource_info(hr_id))

            edit_button = QPushButton()
            edit_button.setIcon(QIcon(edit_icon_path))
            edit_button.setFixedSize(button_size, button_size)
            edit_button.setStyleSheet("border: none; background-color: transparent; padding: 5px;")
            edit_button.clicked.connect(lambda _, hr_id=hr[0]: self.edit_human_resource(hr_id))

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(delete_icon_path))
            delete_button.setFixedSize(button_size, button_size)
            delete_button.setStyleSheet("border: none; background-color: transparent; padding: 5px;")
            delete_button.clicked.connect(lambda _, hr_id=hr[0]: self.delete_human_resource(hr_id))

            action_layout.addWidget(info_button)
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.human_resource_table.setCellWidget(row_position, 8, action_widget)

        self.human_resource_table.setColumnWidth(8, 120)  # Adjust width for action buttons

    def add_human_resource(self):
        dialog = HumanResourceAddDialog(self)
        if dialog.exec():
            self.load_human_resources()

    def delete_human_resource(self, human_resource_id):
        HumanResource.delete(human_resource_id)
        QMessageBox.information(self, "Deleted", f"Human resource ID '{human_resource_id}' has been deleted.")
        self.load_human_resources()

    def show_human_resource_info(self, human_resource_id):
        dialog = HumanResourceInfoDialog(human_resource_id, self)
        dialog.exec()

    def edit_human_resource(self, human_resource_id):
        dialog = HumanResourceEditDialog(human_resource_id, self)
        if dialog.exec():
            self.load_human_resources()
