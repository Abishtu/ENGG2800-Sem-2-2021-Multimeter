from PyQt5.QtWidgets import *
from pc.controller.Controller import Controller


class HoldButton(QPushButton):
    """
    Button to toggle hold mode for multimeter
    """

    def __init__(self, parent, controller: Controller, isHold=False):
        super().__init__(parent=parent)
        self._controller = controller
        self._isHold = isHold
        self.setText("N/H")
        self.setStyleSheet("""
            QPushButton {
                color: green;
                padding-left: 10px;
                padding-right: 10px;
                font-size: 15px;
                font-weight: bold;
                text-align: center;
                padding-top: 5px;
                padding-bottom: 5px;
            }
        """)
        self.clicked.connect(lambda: self.change_label(self._controller))

    def change_label(self, controller: Controller) -> None:
        """
        When the button is pressed, the label of the button
        will change and the hold state will be updated on the
        controller and sent to the multimeter.
        :param controller: (Controller) current controller of the GUI
        """
        if self._isHold:
            self._isHold = False
        else:
            self._isHold = True

        controller.set_hold_serial(self._isHold)
        if self._isHold:
            self.setText("H")
        else:
            self.setText("N/H")
