from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QDialogButtonBox, QComboBox, QGridLayout
from Human_resources.human_resources import HumanResource

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
