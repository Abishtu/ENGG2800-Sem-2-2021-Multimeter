from PyQt5.QtWidgets import *
from pc.view.widgets.SideVoltLabel import *
from pc.view.widgets.CurrentVoltLabel import *
from pc.view.widgets.ModeLabel import ModeLabel
from pc.view.widgets.HoldLabel import HoldButton
from pc.controller.Controller import Controller
import PyQt5.QtCore as QtCore
import typing


class MultimeterInfo(QFrame):
    """
    This is a tile widget that shows the following
    information about the multimeter:

    - Current measurement mode [AC Voltage | DC Voltage | Resistance]
    - Continuity State [SHORT | OPEN]
    - Hold State [N/H | H]
    - Minimum measured value
    - Maximum measured value
    - Recent measured value
    """
    def __init__(self, parent: typing.Optional[QWidget], controller: Controller) -> None:
        super().__init__(parent=parent, flags=QtCore.Qt.WindowFlags())

        self.setup_style()

        self._grid = QGridLayout()
        self.setLayout(self._grid)
        self._mode = ModeLabel(self, "M1")
        self._hold = HoldButton(self, controller=controller)

        self._min_volt = SideVolt(self, "0 V")
        self._max_volt = SideVolt(self, "0 V")
        self._recent_volt = CurrentVolt(self, "0 V")

        self.setup_grid()

    def setup_style(self) -> None:
        """
        Initialises custom CSS stylesheet definitions for this widget,
        it also sets the style of the frame
        """
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)

        self.setStyleSheet("""
            QFrame {
                background-color: #353b48;
                border: 2px;
                border-radius: 5px;
            }
        """)

    def setup_grid(self) -> None:
        """
        Initialises the position of each child widget in the
        parent widgets' (MultimeterInfo) grid
        """
        self._grid.addWidget(self._min_volt, 2, 1)
        self._grid.addWidget(self._recent_volt, 2, 2)
        self._grid.addWidget(self._max_volt, 2, 3)
        self._grid.addWidget(self._mode, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        self._grid.addWidget(self._hold, 1, 3, QtCore.Qt.AlignmentFlag.AlignRight)
        self._grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self._grid.setGeometry(QtCore.QRect(0, 0, 600, 200))

    def get_mode(self) -> ModeLabel:
        """
        Returns the mode label widget

        :return: (ModeLabel) the mode label widget
        """
        return self._mode

    def get_hold(self) -> HoldButton:
        """
        Returns the hold state toggle button

        :return: (HoldButton) the hold state toggle button
        """
        return self._hold

    def get_min_volt(self) -> SideVolt:
        """
        Returns the minimum measurement label widget

        :return: (SideVolt) the minimum label widget
        """
        return self._min_volt

    def get_max_volt(self) -> SideVolt:
        """
        Returns the maximum measurement label widget

        :return: (SideVolt) the maximum label widget
        """
        return self._max_volt

    def get_recent_volt(self) -> CurrentVolt:
        """
        Returns the recent measurement label widget

        :return: (CurrentVolt) the current measurement label widget
        """
        return self._recent_volt

    def update_continuity_state(self, state: str) -> None:
        """
        Enables updating the label of the continuity state,
        under the current implementation, the state param
        will always be either one of the strings; "SHORT" or
        "OPEN".

        :param state: (str) continuity state, either "SHORT" or "OPEN"
        """
        self._continuity_state.setText(state)
