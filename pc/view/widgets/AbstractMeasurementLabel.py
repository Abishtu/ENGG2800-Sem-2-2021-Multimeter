from PyQt5.QtWidgets import *


class MeasurementLabel(QLabel):
    """
    Abstract class to represent GUI label
    for the min, max and current measurement
    values
    """

    def __init__(self, parent, measurement="0.0 M"):
        super().__init__(parent=parent)
        self._measurement = measurement
        self.setText(self._measurement)
