
class Measurement:
    """
    Abstract class that isn't directly initialised,
    defines an abstraction for a measurement, it can
    also deal with assigning appropriate units for
    inputted values, e.g.:
    if measured value (n) >= 1000 units (u),
    then measurement generated will be `n kU`
    """
    def __init__(self, units: str) -> None:
        """
        Initialises a measurement of unit `units` and stores it
        into the private variable self._units, by default,
        self._values for this implementation is `0`

        :param units: the units for the measurement
        """
        self._units = units
        self._value = 0

    def get_value(self) -> float:
        """
        Returns the measured value of the measurement

        :return: value of the measurement
        """
        return self._value

    def get_units(self) -> str:
        """
        Returns the units the measurement uses

        :return: units the measurement uses
        """
        return self._units

    def set_value(self, value: float) -> None:
        """
        Assigns the value of the measurement, the scale of unit
        depends on the value inputted. The method has unit scales
        "k, M, m and µ"

        :param value: value to update measurement to
        """
        if 1000.0 <= abs(value) < 1000000.0:
            self._units = "k" + self._units[-1]
            self._value = value / 1000.0
        elif abs(value) > 1000000.0:
            self._units = "M" + self._units[-1]
            self._value = value / 1000000.0
        elif 10.0 ** -3.0 < abs(value) < 1:
            self._units = "m" + self._units[-1]
            self._value = value / float(10.0 ** (-3.00))
        elif 0 < abs(value) < float(10 ** (-3.00)):
            self._units = "µ" + self._units[-1]
            self._value = value / float(10.0 ** (-6.00))
        else:
            self._units = self._units[-1]
            self._value = value

        self._value = float(format(self._value, '.3f'))

    def set_units(self, units: str) -> None:
        """
        This will only be used by the continuity, it sets the
        units of the current measurement to `units`
        :param units: (str) the new units for the measurement
        """
        self._units = units

    def __str__(self) -> str:
        return f"{self._value} {self._units}"

    def __repr__(self) -> str:
        return str(self)
