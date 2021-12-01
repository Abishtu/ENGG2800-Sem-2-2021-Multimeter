from PyQt5.QtWidgets import *
import PyQt5.QtCore as QtCore
from pc.view.widgets.BacklightLabel import BacklightLevelText
from pc.controller.Controller import Controller


class BacklightIndicator(QFrame):
    """
    A custom widget to allow the user to adjust
    the backlight level of the LCD display.
    """
    def __init__(self, controller: Controller):
        super().__init__(flags=QtCore.Qt.WindowFlags())

        self._grid = QHBoxLayout() # Horizontal box, widgets arranged left -> right.
        self.setLayout(self._grid)

        self._slider = QSlider(QtCore.Qt.Horizontal)
        self._slider.setMinimum(0)
        self._slider.setMaximum(4)
        self._slider.setTickInterval(1)
        self._slider.setTickPosition(QSlider.TicksBelow)

        self._backlight_label = BacklightLevelText(self)
        self._backlight_update_button = QPushButton("Update Backlight")
        self._backlight_update_button.clicked.connect(self.update_serial)

        self._controller = controller

        self.setStyleSheet("""
            QFrame {
                padding-left: 10px;
                padding-right: 10px;
            }
        """)
        self._slider.valueChanged.connect(self.update_label)

        self._grid.addWidget(self._slider)
        self._grid.addWidget(self._backlight_label)
        self._grid.addWidget(self._backlight_update_button)

    def get_backlight_label(self) -> BacklightLevelText:
        """
        Returns the backlight label widget
        :return: (BacklightLevelText) backlight label
        """
        return self._backlight_label

    def get_backlight_slider(self) -> QSlider:
        """
        Returns the backlight slider select widget
        :return: (QSlider) backlight slider
        """
        return self._slider

    def update_label(self) -> None:
        """
        Event that is called when moving the slider, this
        method updates the text in the backlight label
        """
        self._backlight_label.setText(f"{self._slider.value()}")

    def update_serial(self) -> None:
        """
        This method is called when update backlight button is pressed,
        it sends the new backlight value to the multimeter
        (if serial device is connected).
        """
        self._controller.set_backlight_level_serial(int(self._backlight_label.text()))