from PyQt5.QtWidgets import QApplication

from OmxPlayer import OmxPlayer

import sys

from MainView import MainView

if __name__ == '__main__':

    app = QApplication(sys.argv)
    omx_player = OmxPlayer()
    view = MainView(app)

    sys.exit(app.exec_())