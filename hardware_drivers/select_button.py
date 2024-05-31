from machine import Pin
from user_lib.pin_definitions import MENU_SELECT_PIN_NUM
import time
menu_select_pin = Pin(MENU_SELECT_PIN_NUM, Pin.IN, Pin.PULL_UP)

def menu_select_pushed():
    return menu_select_pin.value() == 0

def debounce_button():
    if menu_select_pin.value() is not 0:
        return False
    time.sleep(0.1) #debounce
    return menu_select_pin.value() == 0
