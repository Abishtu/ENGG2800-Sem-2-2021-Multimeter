from pc.controller.Controller import Controller
from pc.model.Multimeter import AC, DC, RESISTANCE, CONTINUITY
from PyQt5.QtWidgets import *
import PyQt5.QtCore as QtCore
import typing


class ModeButtonsCol(QFrame):
    """
    Frame that contains three buttons, each pertaining to the three
    available modes; AC, DC, Resistance (Ω) & Continuity (Ω(cont.))
    """
    def __init__(self, parent: typing.Optional[QWidget], controller: Controller) -> None:
        super().__init__(parent=parent, flags=QtCore.Qt.WindowFlags())

        self._controller = controller
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: #353b48;
                border: 2px;
            }
            
            QPushButton:hover {
                color: white;
            }
        """)

        self._button_col = QVBoxLayout()
        self.setLayout(self._button_col)
        self._ac_button = QPushButton("AC")
        self._ac_button.clicked.connect(self.ac_mode)

        self._dc_button = QPushButton("DC")
        self._dc_button.clicked.connect(self.dc_mode)

        self._res_button = QPushButton("Ω")
        self._res_button.clicked.connect(self.res_mode)

        self._cont_button = QPushButton("Ω(cont.)")
        self._cont_button.clicked.connect(self.cont_mode)

        self._button_col.addWidget(self._ac_button)
        self._button_col.addWidget(self._dc_button)
        self._button_col.addWidget(self._res_button)
        self._button_col.addWidget(self._cont_button)
        self._button_col.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._button_col.setGeometry(QtCore.QRect(0, 0, 50, 200))

    def ac_mode(self) -> None:
        """
        Signal to change mode of multimeter to AC voltage, this is activated
        when the AC button is pressed
        """
        self._controller.set_mode_serial(AC)

    def dc_mode(self) -> None:
        """
        Signal to change mode of multimeter to DC voltage, this is activated
        when the DC button is pressed
        """
        self._controller.set_mode_serial(DC)

    def res_mode(self) -> None:
        """
        Signal to change mode of multimeter to Resistance, this is activated
        when the 'Ω' button is pressed
        """
        self._controller.set_mode_serial(RESISTANCE)

    def cont_mode(self) -> None:
        """
        Signal to change mode of multimeter to Continuity, this is activated
        when the 'Ω(cont.)' button is pressed
        """
        self._controller.set_mode_serial(CONTINUITY)