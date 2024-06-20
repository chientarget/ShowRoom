import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from car_list import CarListWidget
from database import init_db

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Showroom Vinfast")
        self.setGeometry(100, 100, 1500, 900)

        # Main container widget
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Left sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("<span style='color: #2DB4AE;'>Showroom</span><span style='color: #FBCE49;'> VinFast</span>")
        title.setFont(QFont('MulishRoman', 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2DB4AE;")  # Light green color
        sidebar_layout.addWidget(title)

        user_label = QLabel("Phạm nhật vượng\nID: 3456")
        user_label.setFont(QFont('MulishRoman', 12))
        user_label.setStyleSheet("color: #FFFFFF; background-color: #444444; padding: 10px;")
        sidebar_layout.addWidget(user_label)

        sidebar_buttons = [
            "Tổng quan", "Danh sách xe", "Danh sách đơn hàng",
            "Hãng xe đối tác", "Danh sách khách hàng", "Danh sách nhân viên",
            "Danh sách đại lý"
        ]
        sidebar_layout.addStretch()

        for button_text in sidebar_buttons:
            button = QPushButton(button_text)
            button.setFont(QFont('MulishRoman', 12, QFont.Weight.Bold))
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        logout_button = QPushButton("Đăng xuất")
        logout_button.setFont(QFont('MulishRoman', 12, QFont.Weight.Bold))
        sidebar_layout.addWidget(logout_button)

        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar.setLayout(sidebar_layout)

        # Main content area
        content = CarListWidget()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)
        main_layout.setStretch(1, 1)  # Ensure the content area takes up the remaining space

        self.setCentralWidget(main_widget)

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QPushButton { 
            padding: 10px;
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
