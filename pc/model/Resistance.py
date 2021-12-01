from pc.model.Measurement import Measurement


class Resistance(Measurement):
    """
    Resistance sub class inherits all the attributes from the
    Measurement parent class, the only difference is that the unit
    is set to `Ω`
    """

    def __init__(self) -> None:
        super().__init__("Ω")
