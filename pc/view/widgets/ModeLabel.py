from PyQt5.QtWidgets import *


class ModeLabel(QLabel):
    """
    Defines a label for displaying the mode
    on the MultimeterTile, most of the changes
    from the base QLabel class are aesthetic
    in nature.
    """
    def __init__(self, parent, mode):
        super().__init__(parent=parent)
        self._mode = mode
        self.setText(mode)
        self.setStyleSheet("""
            QLabel {
                color: green;
                padding-left: 10px;
                padding-right: 10px;
                font-size: 15px;
                font-weight: bold;
                text-align: center;
            }
        """)
