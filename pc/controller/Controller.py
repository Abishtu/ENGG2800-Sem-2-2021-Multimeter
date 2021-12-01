from pc.view.Application import *
from pc.controller.SerialController import *
from pc.controller.ProtocolParser import *
from PyQt5.QtCore import *
import threading
import sys


class Controller:
    """
    Controller class links the model and view, it modifies data in the
    model and updates their representation in the view. This class
    will also deal with multimeter serial communication
    """

    def __init__(self):
        self._mode_map = {DC: 1, AC: 0, RESISTANCE: 2, CONTINUITY: 3}
        self._hold_map = {True: 1, False: 0}
        self._serial_controller = SerialController()
        self._mulitmeter = Multimeter(AC, "1")
        self._current_view = App(self, self._serial_controller)

        self.default_current_view()

        self._current_view.get_reset_button().clicked.connect(self.reset_data)
        self._worker_thread = None

    def default_current_view(self) -> None:
        """
        Applies the defaults starting data of the
        multimeter class into the current view
        """
        self._current_view.default_current_view(self._mulitmeter)

    def reset_data(self) -> None:
        """
        Resets all data in multimeter when reset button is pressed,
        if multimeter is connected sends command to multimeter to reset all data.
        """
        self._mulitmeter = Multimeter(AC, "1")
        self.default_current_view()
        if self._serial_controller.get_serial() is not None:
            serial_dev = self._serial_controller.get_serial()
            serial_dev.write(b"RESET:\n")

    def set_mode(self, mode: str) -> None:
        """
        Updates the measurement mode of the system

        :param mode: (str) measurement mode always one of [AC Voltage | DC Voltage | Resistance]
        """
        if self._mulitmeter.get_mode() != mode:
            self._mulitmeter.set_mode(mode)
            if self._current_view is not None:
                self._current_view.get_multimeter_view().get_mode().setText(self._mulitmeter.get_mode())
                if self._mulitmeter.get_mode() == CONTINUITY:
                    recent_val = self._mulitmeter.get_recent_measurement()
                    recent_val.set_units("-")
                    self._current_view.get_multimeter_view().get_recent_volt().setText(str(recent_val))
                    self._current_view.get_multimeter_view().get_max_volt().setText("")
                    self._current_view.get_multimeter_view().get_min_volt().setText("")
                else:
                    self.update_measurement(self._mulitmeter.get_recent_measurement().get_value())
                    self.set_minimum(self._mulitmeter.get_minimum().get_value())
                    self.set_maximum(self._mulitmeter.get_maximum().get_value())

    def set_mode_serial(self, mode: str) -> None:
        """
        Updates the measurement mode of the system and sends
        data to microcontroller

        :param mode: (str) measurement mode always one of [AC Voltage | DC Voltage | Resistance]
        """
        self.set_mode(mode)
        if self._serial_controller.get_serial() is not None:
            serial_dev = self._serial_controller.get_serial()
            serial_dev.write(f"MODE:{self._mode_map[self._mulitmeter.get_mode()]}\n".encode())

    def update_measurement(self, value: float) -> None:
        """
        Updates the recently measured value of the system, this
        is only for the PC and no data is sent to the multimeter

        :param value: (float) new recently measured value
        """
        self._mulitmeter.get_recent_measurement().set_value(value)
        if self._mulitmeter.get_mode() == CONTINUITY:
            self.update_continuity_state()
        if self._current_view is not None:
            self._current_view.get_multimeter_view().get_recent_volt().setText(str(self._mulitmeter.
                                                                                   get_recent_measurement()))
        # self.update_continuity_state()

    def set_maximum(self, value: float) -> None:
        """
        Updates the maximum measured value of the system, this
        is only for the PC and no data is sent to the multimeter

        :param value: (float) new maximum measured value
        """
        if self._mulitmeter.get_mode() != CONTINUITY:
            self._mulitmeter.get_maximum().set_value(value)
            if self._current_view is not None:
                self._current_view.get_multimeter_view().get_max_volt().setText(str(self._mulitmeter.get_maximum()))

    def set_minimum(self, value: float) -> None:
        """
        Updates the minimum measured value of the system, this
        is only for the PC and no data is sent to the multimeter

        :param value: (float) new minimum measured value
        """
        if self._mulitmeter.get_mode() != CONTINUITY:
            self._mulitmeter.get_minimum().set_value(value)
            if self._current_view is not None:
                self._current_view.get_multimeter_view().get_min_volt().setText(str(self._mulitmeter.get_minimum()))

    def set_hold(self, state: bool) -> None:
        """
        Updates the hold state of the system, including serial.
        This method only updates the model and does handle
        sending a hold from PC -> Multimeter.

        :param state: (bool) hold state of the multimeter
        """
        self._mulitmeter.set_hold(state)
        if state:
            self._current_view.get_multimeter_view().get_hold().setText("H")
        else:
            self._current_view.get_multimeter_view().get_hold().setText("N/H")

    def set_hold_serial(self, state: bool) -> None:
        """
        Functional parity with `set_hold()` however this
        method handles the case when the PC wants to set
        the hold state of the multimeter.

        :param state: (bool) hold state of the multimeter
        """
        self.set_hold(state)
        if self._serial_controller.get_serial() is not None:
            serial_dev = self._serial_controller.get_serial()
            serial_dev.write(f"HOLD:{self._hold_map[self._mulitmeter.get_hold_state()]}\n".encode())

    def set_backlight_level(self, bl: int) -> None:
        """
        Updates the backlight/brightness level of the multimeter, this only impacts
        the model and view.
        :param bl: (int) backlight level of the multimeter's LCD display
        """
        if self._mulitmeter.get_backlight_level() != bl:
            self.set_backlight_level_model(bl)
            if self._current_view is not None:
                self._current_view.get_brightness_widget().get_backlight_slider().setValue(bl)
                self._current_view.get_brightness_widget().get_backlight_label().setText(f"{bl}")

    def set_backlight_level_model(self, bl: int) -> None:
        """
        Updates the backlight/brightness level of the multimeter in the model

        :param bl: (int) backlight level of the multimeter's LCD display
        """
        self._mulitmeter.set_backlight_level(bl)

    def set_backlight_level_serial(self, bl: int) -> None:
        """
        Updates the backlight/brightness level of the multimeter on the PC
        side and send that data to the multimeter

        :param bl: (int) backlight level of the multimeter's LCD display
        """
        self.set_backlight_level_model(bl);
        if self._serial_controller.get_serial() is not None:
            serial_dev = self._serial_controller.get_serial()
            serial_dev.write(f"BL:{self._mulitmeter.get_backlight_level()}\n".encode())

    def update_continuity_threshold(self, threshold: float) -> None:
        """
        Changes the value of the continuity threshold in the model

        :param threshold: (float) the new continuity threshold of the system
        """
        self._mulitmeter.get_continuity_threshold().set_value(threshold)
        if self._serial_controller.get_serial() is not None:
            serial_dev = self._serial_controller.get_serial()
            serial_dev.write(f"CT:{self._mulitmeter.get_continuity_threshold().get_value()}\n".encode())

    def update_continuity_state(self) -> None:
        """
        Updates the continuity state, this is will only be work if the measurement mode
        is Resistance. This is only updated in the PC Side
        """
        self._mulitmeter.update_continuity_state()

    def get_serial_controller(self) -> SerialController:
        """
        Returns the serial controller

        :return: (SerialController) serial controller used to send data to the multimeter
        """
        return self._serial_controller

    def get_current_view(self):
        """
        Returns the current view

        :return: (App) current view
        """
        return self._current_view

    def set_current_view(self, application) -> None:
        """
        Sets the current view class of the controller

        :param application: (App) object of the application class of the current app
        """
        self._current_view = application

    def handle_connected_in_view(self) -> None:
        """
        Updates the styling of the serial button to be green once it's
        connected to the micro controller.

        Will also display a pop up message box to inform the user that the
        connection has been made
        """
        self._serial_controller.set_connected(True)
        self._current_view.update_connection_status(True)

    def handle_disconnect(self) -> None:
        """
        Disconnects the multimeter from the PC
        Updates style of connect button to red.
        Pop up message box to inform the user the multimeter has been
        disconnected.
        """

        self._serial_controller.disconnect()
        self._current_view.update_connection_status(False)

    def confirm_its_connected(self) -> None:
        """
        This will allow the multimeter to know that the physical
        connection is still active with the multimeter after it's
        connected.
        """
        if self._serial_controller.get_serial() is not None:
            serial_dev = self._serial_controller.get_serial()
            serial_dev.write(b"Y:\n")

    def set_continuity_threshold(self, threshold: float) -> None:
        """
        Updates the continuity threshold based on the value from the
        multimeter
        :param threshold: (float) the threshold to update to
        """
        if self._mulitmeter.get_continuity_threshold().get_value() != threshold:
            self._mulitmeter.get_continuity_threshold().set_value(threshold)
            self._current_view.update_threshold_label(str(threshold))


class ReadThread(QThread):
    """
    Abstraction to handle the serial rx stream, makes use of QThread
    to better integrate with PyQt's application signals when closing
    the window.
    """

    def __init__(self, controller: Controller, application: QApplication) -> None:
        # Constants to translate data from communication protocol
        # to respective definition in software client
        super().__init__(application)
        self._mode_map = {0: AC, 1: DC, 2: RESISTANCE, 3: CONTINUITY}
        self._hold_map = {1: True, 0: False}

        self._controller = controller

        # Maps command with it's respective function
        self._command_map = {
            "MODE": lambda value: self._controller.set_mode(self._mode_map[int(value)]),
            "HOLD": lambda value: self._controller.set_hold(self._hold_map[int(value)]),
            "BL": lambda value: self._controller.set_backlight_level(int(value)),
            "CURR": lambda value: self._controller.update_measurement(float(value)),
            "MIN": lambda value: self._controller.set_minimum(float(value)),
            "MAX": lambda value: self._controller.set_maximum(float(value)),
            "OK": lambda value: self._controller.handle_connected_in_view(),
            "BYE": lambda value: self._controller.handle_disconnect(),
            "?": lambda value: self._controller.confirm_its_connected(),
            "CT": lambda value: self._controller.set_continuity_threshold(float(value))
        }

        self._lock = threading.Lock()
        self._serial_controller = self._controller.get_serial_controller()

        self._running = False
        
    def run(self) -> None:
        """
        Overriding QThread.run() to activate
        the read_commands function
        """
        self._running = True
        print(""":::::::::::::::::::::::::::::::""")
        print(""":: Team 16 Multimeter Client ::""")
        print("""::        Debug Log          ::""")
        print(""":::::::::::::::::::::::::::::::""")
        while self._running:
            with self._lock:
                self.read_commands()

    def read_commands(self) -> None:
        """
        This function handles our rx input, it will
        determine the appropriate response to received
        commands, this response can be as simple and sending
        data back to the multimeter or can affect elements
        in the GUI.
        """

        if self._serial_controller.get_serial() is not None:
            try:
                serial_dev = self._serial_controller.get_serial()
                command = serial_dev.readline().decode("utf-8")
                parser = ProtocolParser(command)
                cmd = parser.get_command()
                value = parser.get_value()
                print(f"""Command: {cmd} :: Value: {value}""")
                if not self._serial_controller.is_connected() and "OK" in cmd:
                    self._command_map[cmd](value)
                else:
                    print(cmd, value)
                    if "BYE" in cmd:
                        self._command_map[cmd](value)
                    else:
                        try:
                            self._command_map[cmd](value)
                        except KeyError:
                            print("Invalid Command!")
            except SerialException as e:
                self._controller.handle_disconnect()
                self._controller.reset_data()

    def before_ending(self) -> None:
        """
        This will allow for our GUI to gracefully exit by handling
        the following cases:
            1. Connection has been established between the multimeter
            and PC, in this case the PC will send the disconnect command
            (DISS:\n) to the multimeter, if the multimeter responds
            back with a "BYE:\n" then this mean that he connection
            status has been updated on the multimeter and the program will
            wait for 1 second before stopping the thread

            2. Connection has been established between the multimeter
            and PC, however, there is a connection timeout, in this case
            the serial device will be closed and the program will wait
            for 1 second before stopping the thread

            3. There was never a connection established, in this case
            the program wait for 1 second before the stopping the thread
        """
        serial_controller = self._controller.get_serial_controller()
        if serial_controller.get_serial() is not None:
            try:
                serial_dev = serial_controller.get_serial()
                serial_controller.confirm_disconnection()
                command = serial_dev.readline().decode("utf-8")
                parser = ProtocolParser(command)
                cmd = parser.get_command()
                value = parser.get_value()
                if serial_controller.is_connected() and "BYE" in cmd:
                    self._command_map[cmd](value)
                    self.msleep(50)
            except SerialTimeoutException:
                self._controller.handle_disconnect()
                self.msleep(50)
            except:
                self.msleep(50)
        else:
            self.msleep(50)

    def stop(self) -> None:
        """
        Overriding QThread.stop() to activate
        the before_ending function
        """
        self._running = False
        with self._lock:
            self.before_ending()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mult = Controller()
    thread = ReadThread(mult, app)
    app.aboutToQuit.connect(thread.stop)
    thread.start()
    sys.exit(app.exec_())
