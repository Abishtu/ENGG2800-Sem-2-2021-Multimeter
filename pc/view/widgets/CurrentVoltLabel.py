from pc.view.widgets.AbstractMeasurementLabel import MeasurementLabel


class CurrentVolt(MeasurementLabel):
    """
    Label for the recent measurement, this is not exclusive
    to voltages, it will also work for resistance measurements
    """
    def __init__(self, parent, text):
        super().__init__(parent=parent, measurement=text)
        self.setObjectName("recentVolt")
        self.setStyleSheet("""
            QLabel {
                color: white;
                padding-left: 10px;
                padding-right: 10px;
                font-size: 40px;
                font-weight: bold;
                text-align: center;
            }
        """)
