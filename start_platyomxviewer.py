from PyQt5.QtWidgets import QApplication
import sys

from MainView import MainView

if __name__ == '__main__':

    app = QApplication(sys.argv)
    view = MainView(app)

    sys.exit(app.exec_())