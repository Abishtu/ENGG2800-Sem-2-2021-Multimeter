from PyQt5.QtWidgets import *

from view.Application import App
from controller.Controller import Controller
from model.Multimeter import *

import sys

control = Controller(Multimeter(AC, "1"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(control)
    sys.exit(app.exec_())
