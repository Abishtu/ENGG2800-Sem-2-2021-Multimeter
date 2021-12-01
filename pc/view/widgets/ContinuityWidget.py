from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence

from pc.controller.Controller import Controller


class ContinuityWidget(QFrame):
    """
    Custom widget to set the continuity threshold
    of the system.

    Ctrl+i : +5 continuity threshold
    Ctrl+d : -5 continuity threshold
    """
    def __init__(self, controller: Controller):
        super(ContinuityWidget, self).__init__()

        self._v_box = QVBoxLayout()
        self.setLayout(self._v_box)

        self._increase_by_five_shortcut = QShortcut(QKeySequence("Ctrl+i"), self)
        self._increase_by_five_shortcut.activated.connect(self.increase_five)

        self._decrease_by_five_shortcut = QShortcut(QKeySequence("Ctrl+d"), self)
        self._decrease_by_five_shortcut.activated.connect(self.decrease_five)

        self._title_label = QLabel("Continuity Threshold")

        self._increase_threshold_button = QPushButton("+")
        self._increase_threshold_button.resize(10, 10)

        self._decrease_threshold_button = QPushButton("-")
        self._decrease_threshold_button.resize(10, 10)

        self._update_threshold_button = QPushButton("Update")
        self._update_threshold_button.resize(10, 10)

        self._threshold_value_label = QLabel("2.0")
        self._threshold_value_label.resize(10, 10)

        self._v_box.addWidget(self._title_label)
        self._v_box.addWidget(self._increase_threshold_button)
        self._v_box.addWidget(self._threshold_value_label)
        self._v_box.addWidget(self._decrease_threshold_button)
        self._v_box.addWidget(self._update_threshold_button)

        self._increase_threshold_button.clicked.connect(self.increase)
        self._decrease_threshold_button.clicked.connect(self.decrease)
        self._update_threshold_button.clicked.connect(self.update_threshold)

        self._controller = controller

        self.setStyleSheet("""
            QFrame {
                background-color: #353b48;
                border: 2px;
            }
            
            QLabel {
                color: white;
                font-weight: bold;
            }
            
        """)

    def increase(self) -> None:
        """
        Signal to increment the continuity threshold when the `+`
        button is pressed
        """
        self._increase_threshold_button.blockSignals(True)
        current_value = float(self._threshold_value_label.text())
        if 0.0 <= current_value < 20.0:
            current_value += float(0.1)
            current_value = abs(current_value)
            current_value = float(format(current_value, '.2f'))
            self._threshold_value_label.setText(str(current_value))
        self._increase_threshold_button.blockSignals(False)

    def decrease(self) -> None:
        """
        Signal to decrement the continuity threshold when the `-`
        button is pressed
        """
        self._increase_threshold_button.blockSignals(True)
        current_value = float(self._threshold_value_label.text())
        if 0.0 < current_value <= 20.0:
            current_value -= float(0.1)
            current_value = abs(current_value)
            current_value = float(format(current_value, '.2f'))
            self._threshold_value_label.setText(str(current_value))
        self._increase_threshold_button.blockSignals(False)

    def increase_five(self):
        """
        Signal to increase the by continuity threshold by +5
        if the shortcut key `Ctrl+i` is used
        """
        self._increase_threshold_button.blockSignals(True)
        current_value = float(self._threshold_value_label.text())
        if 0.0 <= current_value < 20.0:
            current_value += float(0.1*50.0)
            current_value = abs(current_value)
            current_value = float(format(current_value, '.2f'))
            if current_value > 20.0:
                current_value = float(format(20.0, '.2f'))
            self._threshold_value_label.setText(str(current_value))
        self._increase_threshold_button.blockSignals(False)

    def decrease_five(self):
        """
        Signal to decrease the by continuity threshold by -5
        if the shortcut key `Ctrl+d` is used
        """
        self._increase_threshold_button.blockSignals(True)
        current_value = float(self._threshold_value_label.text())
        if 0.0 < current_value <= 20.0:
            current_value -= float(0.1*50)
            current_value = abs(current_value)
            current_value = float(format(current_value, '.2f'))
            if current_value < 0.0:
                current_value = float(format(0.0, '.2f'))
            self._threshold_value_label.setText(str(current_value))
        self._increase_threshold_button.blockSignals(False)

    def update_threshold(self) -> None:
        """
        Activates the update functionality of the continuity widget,
        this will update the value in the multimeter model and if
        serial is connected then it'll update it on the multimeter
        """
        self._update_threshold_button.blockSignals(True)
        current_threshold = self._threshold_value_label.text()
        self._controller.update_continuity_threshold(float(current_threshold))
        self._update_threshold_button.blockSignals(False)

    def update_threshold_label(self, threshString: str) -> None:
        """
        Updates the threshold label based on the value from
        threshString parameter
        :param threshString: (str) new threshold value
        """
        self._threshold_value_label.setText(threshString)
