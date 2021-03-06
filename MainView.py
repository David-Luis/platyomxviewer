from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from VideoWidget import VideoWidget
from VideosListWidget import VideosListWidget

from PicButton import PicButton
from OmxPlayer import OmxPlayer

import os
import configparser
import ast

from pathlib import Path

class VideoInfo(dict):
    def __eq__(self, other):
        self.filename == other.filename
        
    def __lt__(self, other):
        if self["new"] and not other["new"]:
            return True
        elif other["new"] and not self["new"]:
            return False
        
        return self['filename'].lower() < other['filename'].lower()

class MainView(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setGeometry(0, 30, 900, 700)
        self.setWindowTitle("Platy Omx Viewer")

        self.root_path = (str(Path.home()) + "/Downloads").replace("\\", "/")
        self.video_files = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()

        self.search_video_files()
        self.create_videos_list()
        self.create_control_buttons()

        self.show()

    def is_video_file(self, filename):
        video_extensions = ['avi', 'mkv', 'wmv', 'mp4', 'mpg', '3gp', 'mov']
        for extension in video_extensions:
            if filename.endswith(extension):
                return True

        return False
    
    def __get_config(self):
        output_folder = (str(Path.home()) + "/.platyomxplayer/").replace("\\", "/")
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        output_path = output_folder + "user.ini"
        
        if not os.path.exists(output_path):
                with open(output_path, 'w'): pass
                
        config = configparser.ConfigParser()
        config.read(output_path)
        
        return config
    
    def __save_config(self, config):
        output_folder = (str(Path.home()) + "/.platyomxplayer/").replace("\\", "/")
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        output_path = output_folder + "user.ini"
        
        if not os.path.exists(output_path):
            with open(output_path, 'w'): pass
        
        with open(output_path, 'w') as configfile:
            config.write(configfile)
    
    def is_video_new(self, filename):
        config = self.__get_config()
        
        if 'PLAYED' in config:
            return filename not in config['PLAYED']['filenames']
        
        return True
    
    def save_video_played(self, filename):
        config = self.__get_config()
        
        if 'PLAYED' in config:
            filenames = ast.literal_eval(config['PLAYED']['filenames'])
            filenames.append(filename)
            config['PLAYED'] = {'filenames':filenames}
        else:
            config['PLAYED'] = {'filenames':[filename]}
        
        self.__save_config(config)

    def search_video_files(self):
        self.video_files = []

        for root, subdirs, files in os.walk(self.root_path):
            for filename in files:
                if self.is_video_file(filename):
                    file_path = os.path.join(root, filename)
                    video_info = VideoInfo()
                    video_info["file_path"] = file_path.replace("\\", "/")
                    video_info["filename"] = filename
                    video_info["new"] = self.is_video_new(filename)
                    self.video_files.append(video_info)

        self.video_files.sort()

    def create_videos_container(self):
        self.central_widget.setLayout(self.main_layout)
        self.videos_widget = VideosListWidget()
        self.main_layout.addWidget(self.videos_widget)

    def create_videos_list(self):
        self.create_videos_container()

        for video_file in self.video_files:
            video_widget = VideoWidget(self, video_file)
            self.videos_widget.add_video(video_widget)
            
    def create_control_buttons(self):
        size_buttons = 80
        
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.addLayout(self.buttons_layout)
        
        pixmap = QPixmap('data/play.png')
        self.bt_play_pause = PicButton(pixmap)
        self.bt_play_pause.setMaximumSize(size_buttons,size_buttons)
        self.bt_play_pause.clicked.connect(OmxPlayer.instance.pause_resume)
        
        pixmap = QPixmap('data/stop.png')
        self.bt_stop = PicButton(pixmap)
        self.bt_stop.setMaximumSize(size_buttons,size_buttons)
        self.bt_stop.clicked.connect(OmxPlayer.instance.stop)
        
        pixmap = QPixmap('data/seek_back.png')
        self.bt_back = PicButton(pixmap)
        self.bt_back.setMaximumSize(size_buttons,size_buttons)
        self.bt_back.clicked.connect(OmxPlayer.instance.back)
        
        pixmap = QPixmap('data/seek_forward.png')
        self.bt_forward = PicButton(pixmap)
        self.bt_forward.setMaximumSize(size_buttons,size_buttons)
        self.bt_forward.clicked.connect(OmxPlayer.instance.forward)
        
        pixmap = QPixmap('data/seek_back_s.png')
        self.bt_back_s = PicButton(pixmap)
        self.bt_back_s.setMaximumSize(size_buttons,size_buttons)
        self.bt_back_s.clicked.connect(OmxPlayer.instance.back_s)
        
        pixmap = QPixmap('data/seek_forward_s.png')
        self.bt_forward_s = PicButton(pixmap)
        self.bt_forward_s.setMaximumSize(size_buttons,size_buttons)
        self.bt_forward_s.clicked.connect(OmxPlayer.instance.forward_s)
        
        pixmap = QPixmap('data/sub_back.png')
        self.bt_sub_back = PicButton(pixmap)
        self.bt_sub_back.setMaximumSize(size_buttons,size_buttons)
        self.bt_sub_back.clicked.connect(OmxPlayer.instance.sub_back)
        
        pixmap = QPixmap('data/sub_forward.png')
        self.bt_sub_forward = PicButton(pixmap)
        self.bt_sub_forward.setMaximumSize(size_buttons,size_buttons)
        self.bt_sub_forward.clicked.connect(OmxPlayer.instance.sub_forward)
        
        self.buttons_layout.addWidget(self.bt_sub_back)
        self.buttons_layout.addWidget(self.bt_back_s)
        self.buttons_layout.addWidget(self.bt_back)
        self.buttons_layout.addWidget(self.bt_play_pause)
        self.buttons_layout.addWidget(self.bt_stop)
        self.buttons_layout.addWidget(self.bt_forward)
        self.buttons_layout.addWidget(self.bt_forward_s)
        self.buttons_layout.addWidget(self.bt_sub_forward)
        
    def on_play(self):
        pixmap = QPixmap('data/pause.png')
        self.bt_play_pause.set_pixmap(pixmap)
    
    def on_paused(self):
        pixmap = QPixmap('data/play.png')
        self.bt_play_pause.set_pixmap(pixmap)
    
    def on_stop(self):
        pixmap = QPixmap('data/play.png')
        self.bt_play_pause.set_pixmap(pixmap)




