import os
from PyQt6.QtWidgets import*
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from Human_resources.HumanResources import HumanResource

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
        header = QLabel("Danh sách Nhân sự")
        header.setFont(QFont('Roboto', 30, QFont.Weight.ExtraBold))
        header.setStyleSheet("color: #09AD90; font-family: Roboto; font-size: 30px; margin-bottom: 20px;")
        self.main_layout.addWidget(header)

        search_layout = QHBoxLayout()

        self.search_name_edit = QLineEdit()
        self.search_name_edit.setPlaceholderText("Tìm theo tên")
        self.search_name_edit.setFixedWidth(200)
        self.search_name_edit.textChanged.connect(self.load_human_resources)
        search_layout.addWidget(self.search_name_edit)

        self.search_address_edit = QLineEdit()
        self.search_address_edit.setPlaceholderText("Tìm theo địa chỉ")
        self.search_address_edit.setFixedWidth(200)
        self.search_address_edit.textChanged.connect(self.load_human_resources)
        search_layout.addWidget(self.search_address_edit)

        self.search_role_combo = QComboBox()
        self.search_role_combo.setFixedWidth(250)
        self.search_role_combo.addItem("Tất cả")
        for role in HumanResource.get_roles():
            self.search_role_combo.addItem(role[1], role[0])
        self.search_role_combo.currentIndexChanged.connect(self.load_human_resources)
        search_layout.addWidget(self.search_role_combo)

        self.button_layout = QHBoxLayout()
        self.add_human_resource_button = QPushButton("+   Thêm Nhân sự")
        self.add_human_resource_button.setFont(QFont('Roboto', 12, QFont.Weight.Bold))
        self.add_human_resource_button.setFixedSize(150, 42)
        self.add_human_resource_button.clicked.connect(self.add_human_resource)
        self.add_human_resource_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 16px;")
        search_layout.addWidget(self.add_human_resource_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(search_layout)

        self.human_resource_table = QTableWidget()
        self.human_resource_table.setColumnCount(11)
        self.human_resource_table.setHorizontalHeaderLabels(["ID", "Tên đăng nhập", "Tên", "Điện thoại", "Email", "Địa chỉ", "Giới tính", "Vai trò", "Số lượng xe đã bán", "Doanh thu", "Hành động"])
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

        search_name = self.search_name_edit.text().lower()
        search_address = self.search_address_edit.text().lower()
        search_role = self.search_role_combo.currentData()

        for hr in human_resources:
            if (search_name and search_name not in hr[3].lower()) or (search_address and search_address not in hr[6].lower()) or (search_role and hr[8] != search_role):
                continue

            row_position = self.human_resource_table.rowCount()
            self.human_resource_table.insertRow(row_position)
            self.human_resource_table.setItem(row_position, 0, QTableWidgetItem(str(hr[0])))
            self.human_resource_table.setItem(row_position, 1, QTableWidgetItem(hr[1]))
            self.human_resource_table.setItem(row_position, 2, QTableWidgetItem(hr[3]))
            self.human_resource_table.setItem(row_position, 3, QTableWidgetItem(hr[4]))
            self.human_resource_table.setItem(row_position, 4, QTableWidgetItem(hr[5]))
            self.human_resource_table.setItem(row_position, 5, QTableWidgetItem(hr[6]))
            self.human_resource_table.setItem(row_position, 6, QTableWidgetItem("Nam" if hr[7] else "Nữ"))
            self.human_resource_table.setItem(row_position, 7, QTableWidgetItem(HumanResource.get_role_name(hr[8])))
            self.human_resource_table.setItem(row_position, 8, QTableWidgetItem(str(HumanResource.get_sold_cars_count(hr[0]))))
            self.human_resource_table.setItem(row_position, 9, QTableWidgetItem(f"{HumanResource.get_total_revenue(hr[0]):,}"))

            for col in [0, 6, 8, 9]:
                self.human_resource_table.item(row_position, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

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
            self.human_resource_table.setCellWidget(row_position, 10, action_widget)

        self.human_resource_table.setColumnWidth(10, 150)

    def add_human_resource(self):
        dialog = HumanResourceAddDialog(self)
        if dialog.exec():
            self.load_human_resources()

    def delete_human_resource(self, human_resource_id):
        reply = QMessageBox.question(self, 'Xác nhận xóa',
                                     f"Bạn có chắc chắn muốn xóa nhân viên có ID '{human_resource_id}' không?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            HumanResource.delete(human_resource_id)
            self.load_human_resources()

    def show_human_resource_info(self, human_resource_id):
        dialog = HumanResourceInfoDialog(human_resource_id, self)
        dialog.exec()

    def edit_human_resource(self, human_resource_id):
        dialog = HumanResourceEditDialog(human_resource_id, self)
        if dialog.exec():
            self.load_human_resources()


class HumanResourceEditDialog(QDialog):
    def __init__(self, human_resource_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin nhân viên")
        self.human_resource_id = human_resource_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        human_resource = HumanResource.get_human_resource_by_id(self.human_resource_id)
        roles = HumanResource.get_roles()

        self.username_edit = QLineEdit(human_resource[1])
        self.password_edit = QLineEdit(human_resource[2])
        self.name_edit = QLineEdit(human_resource[3])
        self.phone_edit = QLineEdit(human_resource[4])
        self.email_edit = QLineEdit(human_resource[5])
        self.address_edit = QLineEdit(human_resource[6])
        self.gender_edit = QComboBox()
        self.gender_edit.addItems(["Male", "Female"])
        self.gender_edit.setCurrentText("Male" if human_resource[7] else "Female")
        self.role_edit = QComboBox()
        for role in roles:
            self.role_edit.addItem(role[1], role[0])
        self.role_edit.setCurrentIndex(self.role_edit.findData(human_resource[8]))

        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("Username:"), 0, 0)
        form_layout.addWidget(self.username_edit, 0, 1)
        form_layout.addWidget(QLabel("Password:"), 0, 2)
        form_layout.addWidget(self.password_edit, 0, 3)
        form_layout.addWidget(QLabel("Name:"), 1, 0)
        form_layout.addWidget(self.name_edit, 1, 1)
        form_layout.addWidget(QLabel("Phone:"), 1, 2)
        form_layout.addWidget(self.phone_edit, 1, 3)
        form_layout.addWidget(QLabel("Email:"), 2, 0)
        form_layout.addWidget(self.email_edit, 2, 1)
        form_layout.addWidget(QLabel("Address:"), 2, 2)
        form_layout.addWidget(self.address_edit, 2, 3)
        form_layout.addWidget(QLabel("Gender:"), 3, 0)
        form_layout.addWidget(self.gender_edit, 3, 1)
        form_layout.addWidget(QLabel("Role:"), 3, 2)
        form_layout.addWidget(self.role_edit, 3, 3)

        # Set minimum width for input fields
        min_width = 200
        self.username_edit.setMinimumWidth(min_width)
        self.password_edit.setMinimumWidth(min_width)
        self.name_edit.setMinimumWidth(min_width)
        self.phone_edit.setMinimumWidth(min_width)
        self.email_edit.setMinimumWidth(min_width)
        self.address_edit.setMinimumWidth(min_width)
        self.gender_edit.setMinimumWidth(min_width)
        self.role_edit.setMinimumWidth(min_width)

        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        save_button = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box)


    def accept(self):
        gender = True if self.gender_edit.currentText() == "Male" else False
        human_resource = HumanResource(
            self.human_resource_id,
            self.username_edit.text(),
            self.password_edit.text(),
            self.name_edit.text(),
            self.phone_edit.text(),
            self.email_edit.text(),
            self.address_edit.text(),
            gender,
            self.role_edit.currentData()
        )
        human_resource.update()
        super().accept()

class HumanResourceInfoDialog(QDialog):
    def __init__(self, human_resource_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin nhân viên")
        self.human_resource_id = human_resource_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        human_resource = HumanResource.get_human_resource_by_id(self.human_resource_id)

        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("Tên nhân viên:"), 0, 0)
        form_layout.addWidget(QLabel(human_resource[3]), 0, 1)
        form_layout.addWidget(QLabel("Chức vụ:"), 1, 0)
        form_layout.addWidget(QLabel(HumanResource.get_role_name(human_resource[8])), 1, 1)
        form_layout.addWidget(QLabel("Số điện thoại:"), 2, 0)
        form_layout.addWidget(QLabel(human_resource[4]), 2, 1)
        form_layout.addWidget(QLabel("Email:"), 3, 0)
        form_layout.addWidget(QLabel(human_resource[5]), 3, 1)
        form_layout.addWidget(QLabel("Địa chỉ:"), 4, 0)
        form_layout.addWidget(QLabel(human_resource[6]), 4, 1)
        form_layout.addWidget(QLabel("Giới tính:"), 5, 0)
        form_layout.addWidget(QLabel("Male" if human_resource[7] else "Female"), 5, 1)

        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        layout.addWidget(self.button_box)

class HumanResourceAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm nhân viên mới")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        roles = HumanResource.get_roles()

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.address_edit = QLineEdit()
        self.gender_edit = QComboBox()
        self.gender_edit.addItems(["Male", "Female"])
        self.role_edit = QComboBox()
        for role in roles:
            self.role_edit.addItem(role[1], role[0])

        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("Username:"), 0, 0)
        form_layout.addWidget(self.username_edit, 0, 1)
        form_layout.addWidget(QLabel("Password:"), 0, 2)
        form_layout.addWidget(self.password_edit, 0, 3)
        form_layout.addWidget(QLabel("Name:"), 1, 0)
        form_layout.addWidget(self.name_edit, 1, 1)
        form_layout.addWidget(QLabel("Phone:"), 1, 2)
        form_layout.addWidget(self.phone_edit, 1, 3)
        form_layout.addWidget(QLabel("Email:"), 2, 0)
        form_layout.addWidget(self.email_edit, 2, 1)
        form_layout.addWidget(QLabel("Address:"), 2, 2)
        form_layout.addWidget(self.address_edit, 2, 3)
        form_layout.addWidget(QLabel("Gender:"), 3, 0)
        form_layout.addWidget(self.gender_edit, 3, 1)
        form_layout.addWidget(QLabel("Role:"), 3, 2)
        form_layout.addWidget(self.role_edit, 3, 3)

        # Set minimum width for input fields
        min_width = 200
        self.username_edit.setMinimumWidth(min_width)
        self.password_edit.setMinimumWidth(min_width)
        self.name_edit.setMinimumWidth(min_width)
        self.phone_edit.setMinimumWidth(min_width)
        self.email_edit.setMinimumWidth(min_width)
        self.address_edit.setMinimumWidth(min_width)
        self.gender_edit.setMinimumWidth(min_width)
        self.role_edit.setMinimumWidth(min_width)

        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        save_button = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("padding: 10px; background-color: #2DB4AE; color: white; border: none; text-align: center; border-radius: 10px;")

        layout.addWidget(self.button_box)

    def accept(self):
        gender = True if self.gender_edit.currentText() == "Male" else False
        human_resource = HumanResource(
            None,
            self.username_edit.text(),
            self.password_edit.text(),
            self.name_edit.text(),
            self.phone_edit.text(),
            self.email_edit.text(),
            self.address_edit.text(),
            gender,
            self.role_edit.currentData()
        )
        human_resource.save()
        super().accept()
