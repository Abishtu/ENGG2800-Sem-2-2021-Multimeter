import pc.model.Measurement as mes
import pc.model.Voltage as v
import pc.model.Resistance as r
import pc.model.Continuity as c
# Below constants are for the mode string
AC = "AC Voltage"
DC = "DC Voltage"
RESISTANCE = "Resistance"
CONTINUITY = "Continuity"
DEFAULT = "Not Set"


class Multimeter:
    """
    Data structure to represent a multimeter, stores
    the following data:

    - Multimeter id
    - Current mode
    - Current measurement
    - Minimum measured value
    - Maximum measured value
    - Hold state
    - Backlight level
    - Continuity threshold (software only)
    - Continuity state (SHORT | OPEN)
    """
    def __init__(self, mode: str, id: str) -> None:
        """
        Creates a new multimeter, depending on what the mode string is
        the multimeter's measurement values changes to the appropriate
        unit

        :param mode: one of the mode constant strings
        :param id: the id of the current multimeter
        """
        self._id = id
        self._current_mode = mode
        if self._current_mode == AC or self._current_mode == DC:
            self._recent_measurement = v.Voltage()
            self._minimum = v.Voltage()
            self._maximum = v.Voltage()
        elif self._current_mode == RESISTANCE:
            self._recent_measurement = r.Resistance()
            self._minimum = r.Resistance()
            self._maximum = r.Resistance()
        elif self._current_mode == CONTINUITY:
            self._recent_measurement = c.Continuity()
            self._minimum = mes.Measurement("")
            self._maximum = mes.Measurement("")
        self._hold_is_active = False
        self._backlight_level = 4

        self._continuity_threshold = r.Resistance()  # Only relevant when mode = CONTINUITY
        self._continuity_threshold.set_value(float(2.0))  # Only relevant when mode = CONTINUITY

        self._continuity_state = c.OPEN  # Only relevant when mode = RESISTANCE

    def get_id(self) -> str:
        """
        Returns the id of the multimeter

        :return: (str) id of the multimeter
        """
        return self._id

    def get_mode(self) -> str:
        """
        Returns the current mode of the multimeter

        :return: (str) current mode of the multimeter
        """
        return self._current_mode

    def get_recent_measurement(self) -> mes.Measurement:
        """
        Returns the recently measured measurement

        :return: (Measurement) recently measured measurement
        """
        return self._recent_measurement

    def get_minimum(self) -> mes.Measurement:
        """
        Returns the minimum measurement

        :return: (Measurement) minimum measurement
        """
        return self._minimum

    def get_maximum(self) -> mes.Measurement:
        """
        Returns the maximum measurement

        :return: (Measurement) maximum measurement
        """
        return self._maximum

    def get_hold_state(self) -> bool:
        """
        Returns whether or not the multimeter is on
        hold

        :return: (bool) hold state of the multimeter
        """
        return self._hold_is_active

    def get_backlight_level(self) -> int:
        """
        Returns the backlight level of the multimeter

        :return: (int) backlight level of the multimeter
        """
        return self._backlight_level

    def get_continuity_threshold(self) -> r.Resistance:
        """
        Returns the set continuity threshold of the multimeter
        this value is only used in software and is not
        used or sent to the micro controller.

        :return: (Resistance) continuity threshold of the system
        """
        return self._continuity_threshold

    def get_continuity_state(self) -> str:
        """
        Returns the continuity state of the multimeter, i.e.,
        whether or not it's `OPEN` or `SHORT`

        :return: (str) continuity state string
        """
        return self._continuity_state

    def set_mode(self, mode: str) -> None:
        """
        Set's the measurement mode of the multimeter, this will
        also reset the measured values of the multimeter.

        :param mode: mode string constants
        """
        self._current_mode = mode
        if self._current_mode == AC or self._current_mode == DC:
            self._recent_measurement = v.Voltage()
            self._minimum = v.Voltage()
            self._maximum = v.Voltage()
        elif self._current_mode == RESISTANCE:
            self._recent_measurement = r.Resistance()
            self._minimum = r.Resistance()
            self._maximum = r.Resistance()
        elif self._current_mode == CONTINUITY:
            self._recent_measurement = c.Continuity()
            self._minimum = mes.Measurement("")
            self._maximum = mes.Measurement("")

    def update_measurement(self, measurement: mes.Measurement) -> None:
        """
        Updates the recent measurement made by the multimeter

        :param measurement: most recent measurement made by the multimeter
        """
        self._recent_measurement = measurement

    def set_minimum(self, min: mes.Measurement) -> None:
        """
        Updates the recent minimum measurement made by the multimeter

        :param min: most recent minimum measurement made by the multimeter
        """
        self._minimum = min

    def set_maximum(self, max: mes.Measurement) -> None:
        """
        Updates the recent maximum measurement made by the multimeter

        :param max: most recent maximum measurement made by the multimeter
        """
        self._maximum = max

    def set_hold(self, isHold: bool) -> None:
        """
        Updates the hold state of the multimeter

        :param isHold: new hold state of the multimeter
        """
        self._hold_is_active = isHold

    def set_backlight_level(self, bLevel: int) -> None:
        """
        Updates the backlight level of the multimeter

        :param bLevel: new backlight level of the multimeter
        """
        self._backlight_level = bLevel

    def update_continuity_state(self) -> None:
        """
        Updates the continuity state based on the following conditions:
            * If the current mode is in continuity
                - else nothing changes
            * If the recent measurement is greater than the continuity threshold, then
              continuity state is set to `OPEN`
                - else the continuity state is set to `SHORT`
        """
        if self._current_mode == CONTINUITY:
            if self._recent_measurement.get_value() > self._continuity_threshold.get_value():
                self._recent_measurement.set_units(c.OPEN)
            elif self._recent_measurement.get_value() <= self._continuity_threshold.get_value():
                self._recent_measurement.set_units(c.SHORT)

    def __str__(self) -> str:
        return (f"ID: {self._id}\n" +
                f"Mode: {self._current_mode}\n" +
                f"Recent Measurement: {self._recent_measurement}\n" +
                f"Minimum: {self._minimum}\n" +
                f"Maximum: {self._maximum}\n" +
                f"Hold: {self._hold_is_active}\n" +
                f"Backlight Level: {self._backlight_level}\n" +
                f"Continuity Threshold: {self._continuity_threshold}")

    def __repr__(self) -> str:
        return str(self)
