import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Showroom Vinfast")
        self.setGeometry(100, 100, 1200, 600)

        # Main layout
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QListWidget()
        sidebar.addItem("Tổng quan")
        sidebar.addItem("Danh sách xe")
        sidebar.addItem("Danh sách đơn hàng")
        sidebar.addItem("Hãng xe đối tác")
        sidebar.addItem("Danh sách khách hàng")
        sidebar.addItem("Danh sách nhân viên")
        sidebar.addItem("Danh sách đại lý")
        sidebar.addItem("Đăng xuất")
        sidebar.setFixedWidth(200)

        main_layout.addWidget(sidebar)

        # Form layout
        form_layout = QVBoxLayout()

        header_label = QLabel("Thêm xe")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        form_layout.addWidget(header_label)

        form_grid = QHBoxLayout()
        left_form = QVBoxLayout()
        right_form = QVBoxLayout()

        # Left side of the form
        fields_left = [
            "Tên xe", "Năm sản xuất", "Dài x Rộng x Cao", "Công suất tối đa",
            "Hộp số", "Dẫn động", "Túi khí", "Giá xe"
        ]

        for field in fields_left:
            label = QLabel(field)
            line_edit = QLineEdit()
            left_form.addWidget(label)
            left_form.addWidget(line_edit)

        # Right side of the form
        fields_right = [
            "Dòng xe", "Màu sắc", "Động cơ", "Dung tích nhiên liệu",
            "Mức tiêu thụ nhiên liệu", "Số ghế", "Bảo hành", "Đại lý"
        ]

        for field in fields_right:
            label = QLabel(field)
            line_edit = QLineEdit()
            right_form.addWidget(label)
            right_form.addWidget(line_edit)

        form_grid.addLayout(left_form)
        form_grid.addLayout(right_form)

        form_layout.addLayout(form_grid)

        add_car_button = QPushButton("+ Thêm xe")
        form_layout.addWidget(add_car_button, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(form_layout)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
