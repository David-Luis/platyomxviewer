import pexpect
import platform
import sys

class OmxPlayer():
    NONE = 0
    PLAYING = 1
    PAUSED = 2
    
    instance = None
    
    def __init__(self):
        self.process = None
        self.state = OmxPlayer.NONE
        OmxPlayer.instance = self
        
    def set_observer(self, observer):
        self.observer = observer
        
    def play(self, file_path):
        try:
            system = platform.system().lower()
            if "windows" in system:
                self.process = pexpect.spawn("vlc " + '"' + file_path)
            else:
                print("SPAWN " + file_path)
                self.process = pexpect.spawn("omxplayer " + file_path)
                self.observer.on_play()
                self.state = OmxPlayer.PLAYING
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
    
    def pause_resume(self):
        if self.process and not self.state == OmxPlayer.NONE:
            if self.state == OmxPlayer.PLAYING:
                self.state = OmxPlayer.PAUSED
                self.observer.on_paused()
            else:
                self.state = OmxPlayer.PLAYING
                self.observer.on_play()
                
            print("Sending p")
            self.process.send('p')
            
    def stop(self):
        if self.process:
            self.state = OmxPlayer.NONE
            print("Sending q")
            self.process.send('q')
            self.observer.on_stop()
            
    def back(self):
        if self.process and self.state == OmxPlayer.PLAYING:
            print("Sending left")
            self.process.send('\x1b\x5b\x44')
            
    def forward(self):
        if self.process and self.state == OmxPlayer.PLAYING:
            print("Sending right")
            self.process.send('\x1b\x5b\x43')
            
    def back_s(self):
        if self.process and self.state == OmxPlayer.PLAYING:
            print("Sending left")
            self.process.send('\x1b\x5b\x42')
            
    def forward_s(self):
        if self.process and self.state == OmxPlayer.PLAYING:
            print("Sending right")
            self.process.send('\x1b\x5b\x41')
    
