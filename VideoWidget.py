from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *

from pathlib import Path

from PicButton import PicButton
from OmxPlayer import OmxPlayer

import os

import ffmpy

class VideoWidget(QGroupBox):
    def __init__(self, video_file):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.video_file = video_file
        self.is_playing = False

        self.setToolTip(video_file["filename"])

        pixmap = QPixmap('data/loading.png')
        self.bt_image = PicButton(pixmap)
        self.main_layout.addWidget(self.bt_image)
        self.bt_image.clicked.connect(self.on_clicked)

        self.lb_name = QLabel(video_file["filename"])
        self.lb_name.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.lb_name)

        self.setMaximumSize(256, 256)
        output_folder = video_file["file_path"].split("/")[0:-1]

        self.create_preview_img()

    def create_preview_img(self):
        output_folder = (str(Path.home()) + "/.platyomxplayertmp/").replace("\\", "/")
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        output_path = output_folder + self.video_file["filename"] + ".jpg"
        if not os.path.isfile(output_path):
            ff = ffmpy.FFmpeg(inputs={self.video_file["file_path"]: None},
                              outputs={output_path: '-ss 00:00:04 -t 00:00:2 -s 220x124 -r 1 -f mjpeg'})
            ff.run()
            
        self.set_img_preview(output_path)

    def set_img_preview(self, path):
        pixmap = QPixmap(path)
        self.bt_image.set_pixmap(pixmap)

    def on_clicked(self):
        OmxPlayer.instance.play(self.video_file["file_path"])
