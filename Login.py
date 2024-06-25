# Login.py
import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QStackedWidget, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from database import get_user, add_user

class LoginWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Đăng nhập Showroom Vinfast")
        self.setGeometry(100, 100, 500, 400)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.login_widget = self.create_login_widget()
        self.register_widget = self.create_register_widget()

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)

        self.setCentralWidget(self.main_widget)

    def create_login_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("<span style='color: #FFFFFF;font-size:30px;'>Showroom </span><span style='color: #FDBE02; font-size:30px;'>VinFast</span>")
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addStretch()

        username_label = QLabel("Tên đăng nhập")
        username_label.setFont(QFont('Arial', 14))
        username_label.setStyleSheet("color: #FDBE02;")
        layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("background-color: #FFFFFF; border-radius: 20px; padding-left: 10px; color: #000000; font-size: 16px;")
        layout.addWidget(self.username_input)

        password_label = QLabel("Mật khẩu")
        password_label.setFont(QFont('Arial', 14))
        password_label.setStyleSheet("color: #FDBE02;")
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("background-color: #FFFFFF; border-radius: 20px; padding-left: 10px; color: #000000; font-size: 16px;")
        layout.addWidget(self.password_input)

        layout.addStretch()

        button_layout = QHBoxLayout()

        register_button = QPushButton("Đăng ký")
        register_button.setFont(QFont('Arial', 14))
        register_button.setStyleSheet("background-color: #FDBE02; color: black; border-radius: 18px; padding: 10px;")
        register_button.clicked.connect(self.show_register)
        button_layout.addWidget(register_button)

        login_button = QPushButton("Đăng nhập")
        login_button.setFont(QFont('Arial', 14))
        login_button.setStyleSheet("background-color: #FDBE02; color: black; border-radius: 18px; padding: 10px;")
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)

        layout.addLayout(button_layout)

        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def create_register_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("<span style='color: #FFFFFF;font-size:30px;'>Showroom </span><span style='color: #FDBE02;font-size:30px;'>VinFast</span>")
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addStretch()

        username_label = QLabel("Tên đăng nhập")
        username_label.setFont(QFont('Arial', 14))
        username_label.setStyleSheet("color: #FDBE02;")
        layout.addWidget(username_label)

        self.reg_username_input = QLineEdit()
        self.reg_username_input.setFixedHeight(40)
        self.reg_username_input.setStyleSheet("background-color: #FFFFFF; border-radius: 20px; padding-left: 10px; color: #000000; font-size: 16px;")
        layout.addWidget(self.reg_username_input)

        password_label = QLabel("Mật khẩu")
        password_label.setFont(QFont('Arial', 14))
        password_label.setStyleSheet("color: #FDBE02;")
        layout.addWidget(password_label)

        self.reg_password_input = QLineEdit()
        self.reg_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_password_input.setFixedHeight(40)
        self.reg_password_input.setStyleSheet("background-color: #FFFFFF; border-radius: 20px; padding-left: 10px; color: #000000; font-size: 16px;")
        layout.addWidget(self.reg_password_input)

        confirm_password_label = QLabel("Xác nhận Mật khẩu")
        confirm_password_label.setFont(QFont('Arial', 14))
        confirm_password_label.setStyleSheet("color: #FDBE02;")
        layout.addWidget(confirm_password_label)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setFixedHeight(40)
        self.confirm_password_input.setStyleSheet("background-color: #FFFFFF; border-radius: 20px; padding-left: 10px; color: #000000; font-size: 16px;")
        layout.addWidget(self.confirm_password_input)

        layout.addStretch()

        button_layout = QHBoxLayout()

        back_button = QPushButton("Quay lại")
        back_button.setFont(QFont('Arial', 14))
        back_button.setStyleSheet("background-color: #FDBE02; color: black; border-radius: 18px; padding: 10px;")
        back_button.clicked.connect(self.show_login)
        button_layout.addWidget(back_button)

        register_button = QPushButton("Đăng ký")
        register_button.setFont(QFont('Arial', 14))
        register_button.setStyleSheet("background-color: #FDBE02; color: black; border-radius: 18px; padding: 10px;")
        register_button.clicked.connect(self.register)
        button_layout.addWidget(register_button)

        layout.addLayout(button_layout)

        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def show_register(self):
        self.stacked_widget.setCurrentWidget(self.register_widget)

    def login(self):
        print("Attempting to log in")
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Thất bại", "Vui lòng điền tên đăng nhập và mật khẩu.")
            return

        user = get_user(username)

        if user and user[2] == password:  # Assuming password is stored in the third column
            print("Login successful")
            self.hide()
            self.main_window.show_main_window(user[3], user[0], user[4])
        else:
            print("Login failed")
            QMessageBox.warning(self, "Thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def register(self):
        print("Attempting to register")
        username = self.reg_username_input.text().strip()
        password = self.reg_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Thất bại", "Vui lòng điền đầy đủ thông tin đăng ký.")
            return

        if password != confirm_password:
            print("Passwords do not match")
            QMessageBox.warning(self, "Thất bại", "Mật khẩu và xác nhận mật khẩu không khớp.")
            return


        name = "Thành viên Showroom"
        phone = ""
        email = ""
        address = ""
        gender = 1  # 1 for male, 0 for female
        role_id = 4  # mặc điịnh nhân viên hành chính

        try:
            add_user(username, password, name, phone, email, address, gender, role_id)
            print("Registration successful")
            QMessageBox.information(self, "Thành công", "Đăng ký thành công!")
            self.show_login()
        except sqlite3.IntegrityError:
            print("Username already exists")
            QMessageBox.warning(self, "Thất bại", "Tên đăng nhập đã tồn tại.")


if __name__ == '__main__':
    from main import MainWindow
    print("Starting login application")
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #000000;
        }
    """)
    main_window = MainWindow()
    login_window = LoginWindow(main_window)  # Create the LoginWindow
    login_window.show()
    sys.exit(app.exec())
