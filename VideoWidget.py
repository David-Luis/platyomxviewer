from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *

from PicButton import PicButton

import subprocess
import os
import signal
import sys

class VideoWidget(QGroupBox):
    def __init__(self, video_file):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.video_file = video_file
        self.pro = None

        self.setToolTip(video_file["filename"])

        pixmap = QPixmap('loading.png')
        self.bt_image = PicButton(pixmap)
        self.main_layout.addWidget(self.bt_image)
        self.bt_image.clicked.connect(self.on_clicked)

        self.lb_name = QLabel(video_file["filename"])
        self.lb_name.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.lb_name)

        self.setMaximumSize(256, 256)

    def on_clicked(self):
        try:
            print(self.video_file)
            if self.pro:
                os.killpg(os.getpgid(self.pro.pid), signal.SIGTERM)
            else:
                self.pro = subprocess.Popen("omxplayer " + self.video_file["file_path"], shell=True)

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
