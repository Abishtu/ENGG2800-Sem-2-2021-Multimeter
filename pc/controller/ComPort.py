
class ComPort:
    """
    Data structure/Abstraction of meta data of the
    connected serial communication device
    """
    def __init__(self, port: str, hwid: str, description: str) -> None:
        """
        Initialises a ComPort data structure with it's port,
        hardware id and manufacturer provided description

        :param port: (str) port number of connected serial device
        :param hwid: (str) hardware id of connected serial device
        :param description: (str) manufacturer provided description of
                                  connected serial device
        """
        self._port = port
        self._hwid = hwid
        self._description = description

    def get_port(self) -> str:
        """
        Returns the assigned port number of the serial device

        :return: (str) port number serial device is assigned
        """
        return self._port

    def get_hwid(self) -> str:
        """
        Returns the assigned hardware id of the serial device

        :return: (str) hardware id serial device is assigned
        """
        return self._hwid

    def get_description(self) -> str:
        """
        Returns the manufacturer provided description of the connected
        serial device

        :return: (str) manufacturer provided description of serial device
        """
        return self._description

    def set_port(self, port: str) -> None:
        """
        Modifies the assigned port number of the serial device

        :param port: (str) the new port number assigned to the serial device
        """
        self._port = port

    def set_hwid(self, hwid: str) -> None:
        """
        Modifies the assigned hardware id of the serial device

        :param hwid: (str) the new hardware id assigned to the serial device
        """
        self._hwid = hwid

    def set_description(self, description: str) -> None:
        """
        Modifies the manufacturer provided description of the serial device

        :param description: (str) the new description of the serial device
        """
        self._description = description

    def __str__(self) -> str:
        """
        Built in python method to define the string representation of the
        serial device data strucutre

        :return: (str) string representation of the serial device
        """
        return f"{self._port}: {self._description} [{self._hwid}]"

    def __repr__(self) -> str:
        return str(self)
