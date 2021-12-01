from serial import *
from serial.tools.list_ports_windows import *
from pc.controller.ComPort import ComPort


class SerialController:
    """
    Handles serial data and functions, such as :
    - Connecting to a device
    - Available serial devices
    - Getting the list of connected devices
    - Getting the connected serial device
    - Sending a handshake confirmation message
    - Getting and setting the connection state
    """

    def __init__(self):
        self._serial = None
        self._comports = []
        self.update_comports()
        self._connected = False

    def set_serial(self, portname: str, baud=4800) -> None:
        """
        Connected to the serial device with comport, `portname`
        and baud rate `baud`

        :param portname: (str) Comport of serial device to connect to
        :param baud: (int) Baud rate of serial device
        """
        try:
            if self._serial is not None:
                if not self._connected:
                    self._serial = Serial(portname, baudrate=baud)
                else:
                    self._serial.close()
                    self._serial = None
                    self._serial = Serial(portname, baudrate=baud)
            else:
                self._serial = Serial(portname, baudrate=baud)
        except SerialException:
            print("ERROR: Invalid Serial Device")
            self.set_connected(False)
            self._serial = None

    def update_comports(self) -> None:
        """
        Updates list of available serial devices to connect to
        """
        self._comports = []
        temp_comports = sorted(comports())
        for port, description, hwid in temp_comports:
            self._comports.append(ComPort(port, hwid, description))

    def get_comports(self) -> [ComPort]:
        """
        Returns the list of available serial devices

        :return: ([ComPort]) list of available serial devices
        """
        self.update_comports()
        return self._comports

    def get_serial(self) -> Serial:
        """
        Returns an object of the connected serial device, this can be used to

        :return: (Serial) connected serial device
        """
        return self._serial

    def confirm_connection(self) -> None:
        """
        Sends a handshake confirmation message to check if the connected
        serial device is the multimeter or not. Response from the
        device will be handling by the reading thread.
        """
        if self._serial is not None:
            try:
                self._serial.write(b"CONNECT:\n")
            except SerialException:
                print("ERROR: Serial exception occurred during connection attempt")
                self.set_connected(False)
                self._serial = None

    def confirm_disconnection(self) -> None:
        """
        Sends a handshake confirmation message to initiate a disconnection
        with the connected multimeter. Response from the
        device will be handling by the reading thread.
        """
        if self._serial is not None:
            try:
                self._serial.write(b"DISS:\n")
            except SerialException:
                print("ERROR: Serial exception occurred during disconnection")
                self.set_connected(False)
                self._serial = None

    def disconnect(self) -> None:
        """
        Disconnects from the connected serial device
        """
        if self._serial is not None:
            try:
                self._serial.close()
                self._serial = None
                self.set_connected(False)
            except SerialException:
                self.set_connected(False)
                self._serial = None

    def is_connected(self) -> bool:
        """
        Returns the connection status of the device

        :return: (bool)
                 true if connection is connected and confirmed
                 false if
                     connected and not confirmed
                     not connected
        """
        return self._connected

    def set_connected(self, state: bool) -> None:
        """
        Sets the connection state of the serial device

        :param state: (bool)
                      true if connection is connected and confirmed
                      false if
                          connected and not confirmed
                          not connected
        """
        self._connected = state
