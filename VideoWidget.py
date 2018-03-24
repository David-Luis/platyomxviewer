from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *

from PicButton import PicButton

import subprocess
import os
import signal
import sys
import platform
import pexpect

class VideoWidget(QGroupBox):
    def __init__(self, video_file, videos_widget):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.videos_widget = videos_widget
        self.video_file = video_file
        self.is_playing = False

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
        return children[-1].pid

    def play_video(self, file_path):
        self.videos_widget.playing_widget = self
        self.is_playing = True
        
        system = platform.system().lower()
        if "windows" in system:
            pexpect.spawn("vlc " + '"' + file_path)
        else:
            pexpect.spawn("omxplayer " + file_path)
            #self.videos_widget.pro = subprocess.Popen("omxplayer " + file_path, stdout=subprocess.PIPE, shell=True)

        pixmap = QPixmap('stop.png')
        self.bt_image.set_pixmap(pixmap)

    def set_stop_view(self):
        pixmap = QPixmap('loading.png')
        self.bt_image.set_pixmap(pixmap)
        self.is_playing = False
        
    def on_clicked(self):
        try:
            
            if self.videos_widget.pro:
                print("stop")
                children_pid = self.children_pid(self.videos_widget.pro)
                os.kill(children_pid, signal.SIGTERM)
                self.videos_widget.pro = None

                is_playing = self.is_playing

                self.videos_widget.playing_widget.set_stop_view()
                self.videos_widget.playing_widget = None

                print("_is_playing " + str(is_playing))

                if not is_playing:
                    self.play_video(self.video_file["file_path"])
                else:
                    self.is_playing = False
            else:
                print(self.video_file)
                self.play_video(self.video_file["file_path"])

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
