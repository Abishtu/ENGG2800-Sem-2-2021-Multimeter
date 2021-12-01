from PyQt5.QtWidgets import *


class BacklightLevelText(QLabel):
    """
    Label to display the selected backlight level
    """
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setStyleSheet("""
            QLabel {
                color: #101010;
                padding-left: 10px;
                padding-right: 10px;
                padding-bottom: 10px;
                font-size: 15px;
                font-weight: bold;
                text-align: center;
            }
        """)

        self.setText("0")