# partner_forms.py
from PyQt6.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QDialogButtonBox
from Partner.partner import Partner

class PartnerEditDialog(QDialog):
    def __init__(self, partner_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin đối tác")
        self.partner_id = partner_id
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        partner = Partner.get_partner_by_id(self.partner_id)

        self.logo_edit = QLineEdit(partner.logo)
        self.name_edit = QLineEdit(partner.name)
        self.country_edit = QLineEdit(partner.country)
        self.founded_year_edit = QLineEdit(str(partner.founded_year))
        self.description_edit = QLineEdit(partner.description)

        layout.addWidget(QLabel("Logo:"), 0, 0)
        layout.addWidget(self.logo_edit, 0, 1)
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
        layout.addWidget(self.button_box, 5, 0, 1, 2)

    def accept(self):
        partner = Partner(
            self.partner_id,
            self.logo_edit.text(),
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

        layout.addWidget(QLabel("Logo:"), 0, 0)
        layout.addWidget(QLabel(partner.logo), 0, 1)
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

        self.logo_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.country_edit = QLineEdit()
        self.founded_year_edit = QLineEdit()
        self.description_edit = QLineEdit()

        layout.addWidget(QLabel("Logo:"), 0, 0)
        layout.addWidget(self.logo_edit, 0, 1)
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
        layout.addWidget(self.button_box, 5, 0, 1, 2)

    def accept(self):
        partner = Partner(
            None,
            self.logo_edit.text(),
            self.name_edit.text(),
            self.country_edit.text(),
            int(self.founded_year_edit.text()),
            self.description_edit.text()
        )
        partner.save()
        super().accept()
