import pexpect
import platform

def play(self, file_path):
    system = platform.system().lower()
    if "windows" in system:
        pexpect.spawn("vlc " + '"' + file_path)
    else:
        pexpect.spawn("omxplayer " + file_path)