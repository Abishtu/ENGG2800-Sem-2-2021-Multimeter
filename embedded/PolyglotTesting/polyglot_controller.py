"""
SPI, I2C, USB/UART and GPIO can all be used in parallel
"""

import time
# from polyglot_turtle import PolyglotTurtleXiao, PinDirection, PinPullMode
from serial import *

# def gpio():
#     pt = PolyglotTurtleXiao()

#     red_led_pin = 2
#     green_led_pin = 3

#     pt.gpio_set_direction(red_led_pin, PinDirection.OUTPUT)
#     pt.gpio_set_direction(green_led_pin, PinDirection.OUTPUT)

#     while 1:
#         pt.gpio_set_level(red_led_pin, True)
#         pt.gpio_set_level(green_led_pin, False)
#         time.sleep(0.5)

#         pt.gpio_set_level(green_led_pin, True)
#         pt.gpio_set_level(red_led_pin, False)
#         time.sleep(0.5)


# def gpio_pull_up_pull_down_resistors():
#     pt = PolyglotTurtleXiao()

#     button_pin = 1
#     red_led_pin = 2
#     green_led_pin = 3

#     pt.gpio_set_direction(button_pin, PinDirection.INPUT)
#     pt.gpio_set_pull(button_pin,
#                      PinPullMode.PULL_UP)  # set the default state of button to pull up, i.e. button not pressed

#     pt.gpio_set_direction(red_led_pin, PinDirection.OUTPUT)
#     pt.gpio_set_direction(green_led_pin, PinDirection.OUTPUT)

#     while 1:
#         pt.gpio_set_level(red_led_pin, True)
#         pt.gpio_set_level(green_led_pin, False)
#         time.sleep(0.5)

#         pt.gpio_set_level(green_led_pin, True)
#         pt.gpio_set_level(red_led_pin, False)
#         time.sleep(0.5)

#         while pt.gpio_get_level(button_pin):
#             time.sleep(0.01)


# """
# CS - Chip select, selects a device to talk to
# SCK - Serial Clock, clock to transfer data, always generated by the master
# MOSI - Master Out, Slave In, (Data)
# MISO - Master In, Slave Out, (Data)
# """
# def spi():
#     pt = PolyglotTurtleXiao()
#     # pt.gpio_set_direction(3, PinDirection.OUTPUT)
#     # pt.gpio_set_level(3, True)

#     while 1:
#         # pt.gpio_set_level(3, False)
#         pt.spi_exchange(b"Foo Man", 100000, mode=3, cs_pin=3)
#         # pt.gpio_set_level(3, True)

#         time.sleep(1)


def serial_transfer():
    pg = Serial("COM8")
    # pg.baudrate = 9600
    while 1:
        data = pg.read(1)
        if data != b'\xc1':
            print(data)

if __name__ == "__main__":
    serial_transfer()
