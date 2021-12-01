import sys
from time import sleep

from pc.model.Multimeter import *

multi_meters_count = 0


def print_help(user_input: str) -> None:
    print(f"Invalid command: {user_input}")
    print(f"Accepted Commands:")
    print("connect [mode]: To connect a new multimeter")
    print("\tModes:")
    print("\t\t* AC: AC Voltage Mode")
    print("\t\t* DC: DC Voltage Mode")
    print("\t\t* RES: Resistance Mode")
    print("list: Lists all connected multimeter")
    print("[id]: Prints out the multimeter with id [id]")
    print("[id] [mode|update|min|max|hold] [value]: change apects of multimeter with id [id]")
    print("exit: Exits the console")


def print_help_h() -> None:
    print(f"Accepted Commands:")
    print("connect [mode]: To connect a new multimeter")
    print("\tModes:")
    print("\t\t* AC: AC Voltage Mode")
    print("\t\t* DC: DC Voltage Mode")
    print("\t\t* RES: Resistance Mode")
    print("list: Lists all connected multimeter")
    print("[id]: Prints out the multimeter with id [id]")
    print("[id] [mode|update|min|max|hold] [value]: change apects of multimeter with id [id]")
    print("exit: Exits the console")


def test_one():
    control.set_mode(AC)
    control.set_hold(False)
    for i in range(1, 100):
        control.set_minimum(i)
        control.update_measurement(i * 2)
        control.set_maximum(i * 3)
    control.set_hold(True)


if __name__ == '__main__':
    while True:
        user_input = input("?>> ")
        argument_list = user_input.split(" ")

        if argument_list[0] == "test1":
            control.set_current_view(ex)
            control.set_mode(AC)
            control.set_hold(True)

        elif argument_list[0] == "exit":
            sys.exit(0)
