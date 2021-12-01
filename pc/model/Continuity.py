from pc.model.Measurement import Measurement

SHORT = "SHORT"
OPEN = "OPEN"


class Continuity(Measurement):
    def __init__(self):
        super().__init__("-")

    def set_value(self, value: float) -> None:
        """
        Assigns the value of the measurement, the scale of unit
        depends on the value inputted.
        :param value: value to update measurement to
        """
        self._value = value

    def __str__(self) -> str:
        return f"{self.get_units()}"

    def __repr__(self) -> str:
        return str(self)
