from pc.view.widgets.AbstractMeasurementLabel import MeasurementLabel


class SideVolt(MeasurementLabel):
    """
    Defines the format of the min and max measurement
    on the MultimeterTile widget
    """
    def __init__(self, parent, text="0v"):
        super().__init__(parent=parent, measurement=text)
        self.setObjectName("sideVolts")
        self.setStyleSheet("""
            QLabel {
                color: white;
                padding-left: 10px;
                padding-right: 10px;
                font-size: 20px;
                font-weight: bold;
                text-align: center;
            }
        """)
