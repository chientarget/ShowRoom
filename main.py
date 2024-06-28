# main.py
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QFont, QIcon
from Car.CarGUI import CarGUI
from OverviewWidget import OverviewWidget
from Dealer.DealerGUI import DealerGUI
from Customer.CustomerGUI import CustomerGUI
from database import get_role_by_id
from Human_resources.HumanResourcesGUI import HumanResourcesListWidget
from Order.OrderGUI import OrderListWidget
from Partner.PartnerGUI import PartnerListWidget
from Login import LoginWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Showroom Management')
        self.resize(1600, 800)

        # Sidebar
        self.sidebar = self.create_sidebar()

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        # Main Container
        self.container = QHBoxLayout()
        self.container.addWidget(self.sidebar)
        self.container.addWidget(self.main_widget)

        main_container_widget = QWidget()
        main_container_widget.setLayout(self.container)

        self.setCentralWidget(main_container_widget)
        self.current_button = None
        # Initial view

        self.show_over_view()
        self.centerOnScreen()

    def centerOnScreen(self):
        resolution = self.screen().availableGeometry()
        self.move(int((resolution.width() / 2) - (self.frameSize().width() / 2)),
                  int((resolution.height() / 2) - (self.frameSize().height() / 2)))

    def create_sidebar(self):
        self.setStyleSheet("""
        QPushButton { 
            padding: 10px; background-color: #444444; color: #FFFFFF; border: none; text-align: left;
            border-radius: 10px;
        }
         """)
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        self.sidebar_layout = QVBoxLayout(sidebar)

        self.title = QLabel("<span style='color: #2DB4AE;'>Showroom</span><span style='color: #FBCE49;'> VinFost</span>")
        self.title.setFont(QFont('MulishRoman', 30, QFont.Weight.Bold))
        self.title.setStyleSheet("font-size: 30px;")
        self.sidebar_layout.addWidget(self.title)

        self.user_label = QLabel()
        self.user_label.setFont(QFont('Arial', 16))
        self.user_label.setStyleSheet("color: #FFFFFF; background-color: transparent; padding: 10px; font-size: 18px; font-weight: bold;")
        self.sidebar_layout.addWidget(self.user_label)

        sidebar_buttons = [
            ("Tổng quan", self.show_over_view, "img/img_sidebar_buttons/overview.svg"),
            ("Danh sách xe", self.show_car_list, "img/img_sidebar_buttons/car_list.svg"),
            ("Danh sách đơn hàng", self.show_order_list, "img/img_sidebar_buttons/order_list.svg"),
            ("Hãng xe đối tác", self.show_partner_list, "img/img_sidebar_buttons/partner_list.svg"),
            ("Danh sách khách hàng", self.show_customer_list, "img/img_sidebar_buttons/show_customer_list.svg"),
            ("Danh sách nhân sự", self.human_resources, "img/img_sidebar_buttons/human_resource_list.svg"),
            ("Danh sách đại lý", self.show_dealer_list, "img/img_sidebar_buttons/dealer_list.svg")  # Đổi tên hàm và icon
        ]
        self.sidebar_layout.addStretch()

        for button_text, handler, icon_path in sidebar_buttons:
            button = QPushButton(button_text)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(30, 30))
            button.setFont(QFont('MulishRoman', 12, QFont.Weight.Bold))
            button.setStyleSheet("background-color: transparent;font-size:18px;")
            button.clicked.connect(lambda checked, btn=button, hdlr=handler: self.on_sidebar_button_clicked(btn, hdlr))
            self.sidebar_layout.addWidget(button)

        self.sidebar_layout.addStretch()

        self.logout_button = QPushButton("Đăng xuất")
        self.logout_button.setFont(QFont('MulishRoman', 12, QFont.Weight.Bold))
        self.logout_button.setStyleSheet("background-color: transparent; font-size:18px;")
        self.logout_button.setIconSize(QSize(30, 30))

        self.logout_button.setIcon(QIcon("img/img_sidebar_buttons/logout.svg"))
        self.logout_button.clicked.connect(self.logout)
        self.sidebar_layout.addWidget(self.logout_button)

        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar.setLayout(self.sidebar_layout)

        return sidebar

    def on_sidebar_button_clicked(self, button, handler):
        if self.current_button:
            self.current_button.setStyleSheet("background-color: transparent;font-size:18px; spacing: 10px;")

        self.current_button = button
        button.setStyleSheet("background-color: transparent;font-size:18px; spacing: 10px; border-left: 3px solid #FBCE49; border-radius: none;")
        handler()

    user_ids = 0

    def show_main_window(self, name, user_id, role_id):
        role = get_role_by_id(role_id)
        self.user_ids = user_id
        self.user_label.setText(f"{name}\nChức danh: {role}\nID: {user_id}")
        self.user_role = role_id
        self.show()

    def clear_main_layout(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def show_over_view(self):
        self.clear_main_layout()
        self.main_layout.addWidget(OverviewWidget())

    def show_car_list(self):
        self.clear_main_layout()
        self.main_layout.addWidget(CarGUI(self.user_ids))

    def show_order_list(self):
        if self.user_role not in [1, 2, 4]:
            QMessageBox.critical(self, "Error", "Bạn không có quyền xem thông tin khách hàng.")
            return
        else:
            self.clear_main_layout()
            self.main_layout.addWidget(OrderListWidget())

    def show_partner_list(self):
        self.clear_main_layout()
        self.main_layout.addWidget(PartnerListWidget())

    def show_customer_list(self):
        if self.user_role not in [1,2, 4]:
            QMessageBox.critical(self, "Error", "Bạn không có quyền xem thông tin khách hàng.")
            return
        else:
            self.clear_main_layout()
            self.main_layout.addWidget(CustomerGUI())

    def human_resources(self):
        if self.user_role not in [1, 4]:
            QMessageBox.critical(self, "Error", "Bạn không có quyền xem thông tin khách hàng.")
            return
        else:
            self.clear_main_layout()
            self.main_layout.addWidget(HumanResourcesListWidget())

    def show_dealer_list(self):
        if self.user_role not in [1]:
            QMessageBox.critical(self, "Error", "Bạn không có quyền xem thông tin đại lý.")
            return
        else:
            self.clear_main_layout()
            self.main_layout.addWidget(DealerGUI())

    def logout(self):
        print("Logout clicked")
        self.hide()
        self.login_window = LoginWindow(self)
        self.login_window.show()


if __name__ == '__main__':
    print("Starting application")
    app = QApplication(sys.argv)
    with open("style.qss", "r") as f:
        stylesheet = f.read()
        app.setStyleSheet(stylesheet)
    main_window = MainWindow()

    login_window = LoginWindow(main_window)
    login_window.show()

    # main_window.show_main_window("Admin", 1, 1)
    sys.exit(app.exec())
