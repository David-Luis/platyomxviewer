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
    
    def children_pid(self, pid):
        import psutil
        current_process = psutil.Process()
        children = current_process.children(recursive=True)
        print(children)
        return children[2].pid
        
    def on_clicked(self):
        try:
            
            if self.pro:
                print("stop")
                children_pid = self.children_pid(self.pro.pid)
                os.kill(children_pid, signal.SIGTERM)
                self.pro = None
            else:
                print(self.video_file)
                self.pro = subprocess.Popen("omxplayer " + self.video_file["file_path"], stdout=subprocess.PIPE, shell=True)

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
