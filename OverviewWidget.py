# OverviewWidget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from database import (get_monthly_revenue, get_cars_sold, get_cars_in_stock,
                      get_top_dealers, get_top_human_resource_weekly, get_top_human_resource_monthly)

class OverviewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Thêm hàng đầu tiên
        top_row = QHBoxLayout()
        top_row.addWidget(self.create_info_box("Doanh thu tháng", f"{get_monthly_revenue():,} Vnd"))
        top_row.addWidget(self.create_info_box("Số xe đã bán", str(get_cars_sold())))
        top_row.addWidget(self.create_info_box("Số xe tồn kho", str(get_cars_in_stock())))
        main_layout.addLayout(top_row)

        # Thêm đường kẻ ngang
        main_layout.addWidget(self.create_horizontal_line())

        # Top doanh thu đại lý
        main_layout.addWidget(self.create_section_title("Top doanh thu đại lý"))
        main_layout.addLayout(self.create_top_section(get_top_dealers(), "Doanh số:"))

        # Nhân viên xuất sắc tuần
        main_layout.addWidget(self.create_section_title("Nhân viên xuất sắc tuần"))
        main_layout.addLayout(self.create_top_section(get_top_human_resource_weekly(), "Doanh số:"))

        # Nhân viên xuất sắc tháng
        main_layout.addWidget(self.create_section_title("Nhân viên xuất sắc tháng"))
        main_layout.addLayout(self.create_top_section(get_top_human_resource_monthly(), "Doanh số:"))

    def create_info_box(self, title, value):
        box = QFrame()
        box.setFrameShape(QFrame.Shape.StyledPanel)
        box_layout = QVBoxLayout()
        title_label = QLabel(title)
        value_label = QLabel(value)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; color: #FBCE49; font-size: 20px;")
        value_label.setStyleSheet("font-weight: bold; color: white; font-size: 24px;")
        box_layout.addWidget(title_label)
        box_layout.addWidget(value_label)
        box.setLayout(box_layout)
        box.setStyleSheet("background-color: #333333; border-radius: 10px; padding: 5px;")
        return box

    def create_top_section(self, items, prefix):
        section = QHBoxLayout()
        for i, (name, revenue) in enumerate(items, 1):
            widget = QFrame()
            widget.setFrameShape(QFrame.Shape.StyledPanel)
            layout = QVBoxLayout()
            title_label = QLabel(f"{name} - Top {i}")
            subtitle_label = QLabel(f"{prefix} {revenue:,}vnd")
            title_label.setStyleSheet("font-weight: bold; color: white; font-size: 18px;")
            subtitle_label.setStyleSheet("font-weight: bold; color: #FBCE49; font-size: 16px;")
            layout.addWidget(title_label)
            layout.addWidget(subtitle_label)
            widget.setLayout(layout)
            widget.setStyleSheet("background-color: #333333; border-radius: 10px; padding: 5px;")
            section.addWidget(widget)
        return section

    def create_horizontal_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #555555; height: 2px;")
        return line

    def create_section_title(self, title):
        label = QLabel(title)
        label.setStyleSheet("font-weight: bold; color: white; font-size: 22px; margin-top: 20px; margin-bottom: 10px;")
        return label
