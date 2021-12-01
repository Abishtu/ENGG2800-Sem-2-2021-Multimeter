from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor
from pc.controller.SerialController import SerialController


class SerialPortSelector(QFrame):
    """
    A custom widget to allow the user to select the COM port and
    baud rate of the multimeter's assigned serial communication
    port
    """

    def __init__(self, serial_controller: SerialController):
        super(SerialPortSelector, self).__init__()
        self._h_box = QHBoxLayout(self)
        self.setLayout(self._h_box)
        self._serial_controller = serial_controller

        self._baud_rate_entry = QComboBox()
        self._baud_rate_entry.addItems(["19200", "9200", "4800"])
        self._comport_combo_box = QComboBox()
        self._init_serial_button = QPushButton("Connect")
        self._init_serial_button.clicked.connect(self.connect_serial)
        self._disconnect_serial = QPushButton("Disconnect")
        self._disconnect_serial.clicked.connect(self.dissconnect_serial)
        self._update_combo_list_button = QPushButton("Update")
        self._update_combo_list_button.clicked.connect(self.update_entries)
        self._connection_status = QLabel("Disconnected")
        self._h_box.addWidget(self._update_combo_list_button)
        self._h_box.addWidget(self._comport_combo_box)
        self._h_box.addWidget(self._baud_rate_entry)
        self._h_box.addWidget(self._init_serial_button)
        self._h_box.addWidget(self._disconnect_serial)
        self._h_box.addWidget(self._connection_status)

    def update_entries(self) -> None:
        """
        Updates the combobox containing connected comports,
        clears the list of comports and reloads them whenever
        the 'Update' button is pressed, this is done to avoid
        duplicate entries
        """
        self._comport_combo_box.blockSignals(True)
        self._comport_combo_box.clear()
        self._comport_combo_box.blockSignals(False)
        controller_list = self._serial_controller.get_comports()
        ports = []

        for comport in controller_list:
            ports.append(f"{comport.get_port()}")

        self._comport_combo_box.addItems(ports)

    def update_connection_status(self, state: bool) -> None:
        """
        Changes the connection status label depending
        on the connection state

        :param: (bool) connection state of system
        """
        connection_map = {True: "Connected", False: "Disconnected"}
        self._connection_status.setText(connection_map[state])

    def check_update_connection_state(self) -> None:
        """
        Very similar to above function, however changes based
        on state in serial_controller
        """
        connection_map = {True: "Connected", False: "Disconnected"}
        self._connection_status.setText(connection_map[
                                            self._serial_controller.is_connected()])

    def connect_serial(self) -> None:
        """
        Attempts a connection with the serial device on the selected comport,
        self._serial_controller.confirm_connection() is uses to check if
        device it's connected to is the multimeter or not.
        """
        if not self._serial_controller.is_connected():
            selected_port = self._comport_combo_box.currentText()
            baud_rate = self._baud_rate_entry.currentText()
            if len(selected_port) > 1:
                self._serial_controller.set_serial(selected_port, int(baud_rate))
                self._serial_controller.confirm_connection()

    def dissconnect_serial(self) -> None:
        """
        Disconnects the connected serial device
        """
        if self._serial_controller.is_connected():
            self._serial_controller.confirm_disconnection()