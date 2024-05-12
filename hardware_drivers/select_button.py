from machine import Pin
from user_lib.pin_definitions import MENU_SELECT_PIN_NUM

menu_select_pin = Pin(MENU_SELECT_PIN_NUM, Pin.IN, Pin.PULL_UP)

def menu_select_pushed():
    return menu_select_pin.value() == 0

