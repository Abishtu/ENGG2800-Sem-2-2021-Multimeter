from PyQt5.QtWidgets import *
from pc.view.widgets.MultimeterTile import MultimeterInfo
from pc.view.widgets.ModeCol import ModeButtonsCol
from pc.controller.Controller import Controller
from pc.view.widgets.SerialPortSelector import SerialPortSelector
from pc.view.widgets.BacklightFrame import BacklightIndicator
from pc.view.widgets.ContinuityWidget import ContinuityWidget
from pc.model.Multimeter import *

import PyQt5.QtCore as QtCore


class App(QWidget):
    """
    This class is the applications super class, it has
    instances of all the widgets used and methods to
    interact with them.

    Handles windows properties such as window title name,
    left, right and top positions and size of the window
    """

    def __init__(self, controller: Controller, serial_controller):
        super().__init__()
        self._title = "Team 16 +Multimeter Client"
        self._left = 50
        self._top = 50
        self._width = 640
        self._height = 480

        self._controller = controller
        self._controller.set_current_view(self)

        self._layout = QGridLayout()
        self.setLayout(self._layout)

        self._multimeter = MultimeterInfo(self, controller)
        self._buttons = ModeButtonsCol(self, self._controller)
        self._serial_chooser = SerialPortSelector(serial_controller)

        self._brightness_slider = BacklightIndicator(self._controller)

        self._continuity_setter = ContinuityWidget(self._controller)

        self._reset_button = QPushButton("Reset")

        self.init_ui()

    def init_ui(self) -> None:
        """
        Set's up the window title and places components in their appropriate position
        in the application's grid layout
        """
        self.setWindowTitle(self._title)
        self._layout.addWidget(self._multimeter, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._buttons, 1, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self._layout.addWidget(self._continuity_setter, 2, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self._layout.addWidget(self._serial_chooser, 2, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        self._layout.addWidget(self._brightness_slider, 3, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._reset_button, 4, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

        self._layout.setGeometry(QtCore.QRect(self._top, self._left, self._width, self._height))

        self.show()

    def get_multimeter_view(self) -> MultimeterInfo:
        """
        Returns the multimeter tile widget

        :return: (MultimeterInfo) multimeter tile widget
        """
        return self._multimeter

    def get_brightness_widget(self) -> BacklightIndicator:
        """
        Returns the brightness widget

        :return: (BacklightIndicator) brightness widget
        """
        return self._brightness_slider

    def update_connection_status(self, state: bool) -> None:
        """
        Changes the connection status label depending
        on the connection state

        :param: (bool) connection state of system
        """
        self._serial_chooser.update_connection_status(state)

    def default_current_view(self, multimeter: Multimeter) -> None:
        """
        Applies the defaults starting data of the
        multimeter class into the current view

        :param: (Multimeter) the startign model with default
                values
        """

        self._brightness_slider.get_backlight_slider().setValue(multimeter.get_backlight_level())
        self._brightness_slider.get_backlight_label().setText(f"{multimeter.get_backlight_level()}")

        self._multimeter.get_mode().setText(multimeter.get_mode())
        if multimeter.get_hold_state():
            self._multimeter.get_hold().setText("H")
        else:
            self._multimeter.get_hold().setText("N/H")

        if multimeter.get_mode() == CONTINUITY:
            self._multimeter.get_min_volt().setText("")
            self._multimeter.get_max_volt().setText("")
        else:
            self._multimeter.get_min_volt().setText(str(multimeter.get_minimum()))
            self._multimeter.get_max_volt().setText(str(multimeter.get_minimum()))

        self._multimeter.get_recent_volt().setText(str(multimeter.get_recent_measurement()))

        self._serial_chooser.check_update_connection_state()

    def get_reset_button(self) -> QPushButton:
        """
        Returns the reset button object

        :return: (QPushButton) reset button
        """
        return self._reset_button

    def update_threshold_label(self, threshString: str) -> None:
        """
        Updates the threshold label based on the value from
        threshString parameter
        :param threshString: (str) new threshold value
        """
        self._continuity_setter.update_threshold_label(threshString)
