# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont
from car_list import CarListWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Showroom Vinfest")
        self.setGeometry(200, 150, 1500, 800)

        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)

        self.sidebar = self.create_sidebar()
        self.main_layout.addWidget(self.sidebar)

        self.content = CarListWidget()
        self.main_layout.addWidget(self.content)
        self.main_layout.setStretch(1, 1)

        self.user_role = None
        self.setCentralWidget(self.main_widget)

    def create_sidebar(self):
        self.setStyleSheet("""
        QPushButton { 
            padding: 10px; background-color: #444444; color: #FFFFFF; border: none; text-align: left;
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
        self.user_label.setText(f"{name}\nID: {user_id}")
        self.user_role = role_id  # Store the user role
        # Kiểm tra nếu CarListWidget có phương thức set_permissions
        if hasattr(self.content, 'set_permissions'):
            self.content.set_permissions(role_id)  # Pass the role to the content widget
        self.show()

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
