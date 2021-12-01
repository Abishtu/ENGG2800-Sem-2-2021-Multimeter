from pc.model.Measurement import Measurement


class Voltage(Measurement):
    """
    Voltage sub class inherits all the attributes from the
    Measurement parent class, the only difference is that the unit
    is set to `V`
    """

    def __init__(self) -> None:
        super().__init__("V")
