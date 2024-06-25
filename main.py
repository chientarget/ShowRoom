# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont
from Car.car_list import CarListWidget
from agency_list import AgencyList
from customer_list import CustomerList
from database import get_role_by_id
from employee_list import EmployeeList
from order_list import OrderList
from partner_list import PartnerList


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Car Showroom Management')

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()

        self.car_list_button = QPushButton('Danh sách xe')
        # self.car_list_button.clicked.connect(self.show_car_list)
        self.sidebar_layout.addWidget(self.car_list_button)

        self.order_list_button = QPushButton('Danh sách đơn hàng')
        self.order_list_button.clicked.connect(self.show_order_list)
        self.sidebar_layout.addWidget(self.order_list_button)

        self.partner_list_button = QPushButton('Hãng xe đối tác')
        self.partner_list_button.clicked.connect(self.show_partner_list)
        self.sidebar_layout.addWidget(self.partner_list_button)

        self.customer_list_button = QPushButton('Danh sách khách hàng')
        self.customer_list_button.clicked.connect(self.show_customer_list)
        self.sidebar_layout.addWidget(self.customer_list_button)

        self.employee_list_button = QPushButton('Danh sách nhân viên')
        self.employee_list_button.clicked.connect(self.show_employee_list)
        self.sidebar_layout.addWidget(self.employee_list_button)

        self.agency_list_button = QPushButton('Danh sách đại lý')
        self.agency_list_button.clicked.connect(self.show_agency_list)
        self.sidebar_layout.addWidget(self.agency_list_button)

        self.sidebar.setLayout(self.sidebar_layout)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        # Initial view
        self.show_car_list()

    def create_sidebar(self):
        self.setStyleSheet("""
        QPushButton { 
            padding: 10px; background-color: #444444; color: #FFFFFF; border: none; text-align: left;
            border-radius: 10px; /* Thêm dòng này */
        }
         """)
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(sidebar)

        self.title = QLabel("<span style='color: #2DB4AE;'>Showroom</span><span style='color: #FBCE49;'> VinFest</span>")
        self.title.setFont(QFont('MulishRoman', 30, QFont.Weight.Bold))
        self.title.setStyleSheet("font-size: 30px;  ")
        self.sidebar_layout.addWidget(self.title)
        self.user_label = QLabel("Có vẻ chưa đăng nhập :)))")
        self.user_label.setFont(QFont('MulishRoman', 15))
        self.user_label.setStyleSheet("color: #FFFFFF; background-color: transparent; padding: 10px;  font-size:18px; font-weight: bold;")
        self.sidebar_layout.addWidget(self.user_label)

        sidebar_buttons = [
            "Tổng quan", "Danh sách xe", "Danh sách đơn hàng",
            "Hãng xe đối tác", "Danh sách khách hàng", "Danh sách nhân viên",
            "Danh sách đại lý"
        ]
        self.sidebar_layout.addStretch()

        for button_text in sidebar_buttons:
            button = QPushButton(button_text)
            button.setFont(QFont('MulishRoman', 12, QFont.Weight.Bold))
            button.setStyleSheet("background-color: transparent;font-size:18px; ")
            self.sidebar_layout.addWidget(button)

        self.sidebar_layout.addStretch()

        self.logout_button = QPushButton("Đăng xuất")
        self.logout_button.setFont(QFont('MulishRoman', 12, QFont.Weight.Bold))
        self.logout_button.setStyleSheet("background-color: transparent; font-size:18px;")
        self.logout_button.clicked.connect(self.logout)
        self.sidebar_layout.addWidget(self.logout_button)

        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar.setLayout(self.sidebar_layout)

        return sidebar

    def show_main_window(self, name, user_id, role_id):
        role = get_role_by_id(role_id)
        self.user_label.setText(f"{name}\nChức danh: {role}\nID: {user_id}")
        self.user_role = role_id
        # Kiểm tra nếu CarListWidget có phương thức set_permissions
        if hasattr(self.content, 'set_permissions'):
            self.content.set_permissions(role_id)  # Pass the role to the content widget
        self.show()

    def clear_main_layout(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()



    def show_order_list(self):
        self.clear_main_layout()
        self.main_layout.addWidget(OrderList())

    def show_partner_list(self):
        self.clear_main_layout()
        self.main_layout.addWidget(PartnerList())

    def show_customer_list(self):
        self.clear_main_layout()
        self.main_layout.addWidget(CustomerList())

    def show_employee_list(self):
        self.clear_main_layout()
        self.main_layout.addWidget(EmployeeList())

    def show_agency_list(self):
        self.clear_main_layout()
        self.main_layout.addWidget(AgencyList())
        
    def logout(self):
        print("Logout clicked")
        self.hide()
        self.login_window = LoginWindow(self)  # Re-create the LoginWindow
        self.login_window.show()

if __name__ == '__main__':
    print("Starting application")
    from Login import LoginWindow
    app = QApplication(sys.argv)
    with open("style.qss", "r") as f:
        stylesheet = f.read()
        app.setStyleSheet(stylesheet)
    main_window = MainWindow()

    login_window = LoginWindow(main_window)  # Create the LoginWindow
    login_window.show()

    # main_window.show_main_window("Admin", 1, 1)
    sys.exit(app.exec())
