class ProtocolParser:
    """
    Parses a command coming in from the multimeter, as per the high level
    communication protocol a command is formatted in the following patten

    CMD:VALUE\n
    """

    def __init__(self, received_command: str):
        try:
            self._command = received_command.split(":")[0]
            self._command = ''.join(ch for ch in self._command if ch.isalpha())
            self._value = received_command.split(":")[1]
        except:
            self._command = ""
            self._value = ""
        self._value = self._value.strip()

    def get_command(self) -> str:
        """
        Returns the CMD portion of the data from the multimeter

        :return: (str) CMD portion of the data
        """
        return self._command

    def get_value(self) -> str:
        """
        Returns the VALUE portion of the data from the multimeter

        :return: (str) VALUE portion of the data
        """
        return self._value
