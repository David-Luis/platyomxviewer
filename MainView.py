from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from VideoWidget import VideoWidget
from VideosListWidget import VideosListWidget

import os
from pathlib import Path

class MainView(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setGeometry(0, 20, 900, 700)
        self.setWindowTitle("Platy Omx Viewer")

        self.root_path = (str(Path.home()) + "/Downloads").replace("\\", "/")
        self.video_files = []

        self.search_video_files()
        self.create_videos_list()

        self.show()

    def is_video_file(self, filename):
        video_extensions = ['avi', 'mkv', 'wmv', 'mp4', 'mpg', '3gp', 'mov']
        for extension in video_extensions:
            if filename.endswith(extension):
                return True

        return False

    def search_video_files(self):
        self.video_files = []

        for root, subdirs, files in os.walk(self.root_path):
            for filename in files:
                if self.is_video_file(filename):
                    file_path = os.path.join(root, filename)
                    self.video_files.append({"file_path": file_path.replace("\\", "/"), "filename": filename})

    def create_videos_container(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.videos_widget = VideosListWidget()
        self.main_layout.addWidget(self.videos_widget)

    def create_videos_list(self):
        self.create_videos_container()

        for video_file in self.video_files:
            video_widget = VideoWidget(video_file)
            self.videos_widget.add_video(video_widget)



