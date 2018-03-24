import pexpect
import platform
import sys

def play(file_path):

    try:
        system = platform.system().lower()
        if "windows" in system:
            pexpect.spawn("vlc " + '"' + file_path)
        else:
            pexpect.spawn("omxplayer " + file_path)
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])