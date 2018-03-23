from PyQt5.QtWidgets import *


class VideosListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.elements_per_row = 3
        self.current_row = 0
        self.current_col = 0

        self.file_layout = QGridLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.file_layout)
        self.main_layout.addWidget(self.main_widget)

        
        self.files_widget = QWidget()
        self.files_widget.setLayout(self.file_layout)
        self.scroll_list = QScrollArea()
        self.scroll_list.setWidgetResizable(True)
        self.scroll_list.setWidget(self.files_widget)
        self.main_layout.addWidget(self.scroll_list)

    def add_video(self, widget):
        self.file_layout.addWidget(widget, self.current_row, self.current_col)

        self.current_col += 1
        if self.current_col >= self.elements_per_row:
            self.current_col = 0
            self.current_row += 1