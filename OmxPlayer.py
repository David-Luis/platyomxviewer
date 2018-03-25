import pexpect
import platform
import sys

class OmxPlayer():
    instance = None
    
    def __init__(self):
        self.process = None
        OmxPlayer.instance = self
        
    def play(self, file_path):
        try:
            system = platform.system().lower()
            if "windows" in system:
                self.process = pexpect.spawn("vlc " + '"' + file_path)
            else:
                print("SPAWN " + file_path)
                self.process = pexpect.spawn("omxplayer " + file_path)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
    
    def pause_resume(self):
        if self.process:
            print("Sending p")
            self.process.send('p')
    
