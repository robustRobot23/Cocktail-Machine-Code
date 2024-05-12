from machine import Pin
import time
from user_lib.pin_definitions import TOP_LIMIT_SWITCH_PIN_NUM, BOTTOM_LIMIT_SWITCH_PIN_NUM
top_limit_pin = Pin(TOP_LIMIT_SWITCH_PIN_NUM, Pin.IN)
bottom_limit_pin = Pin(BOTTOM_LIMIT_SWITCH_PIN_NUM, Pin.IN)

def wait_for_top_limit_pressed():
       
    while top_limit_pin.value() == 1:
        time.sleep(0.1)
    print("Top limit was pressed")
    return True

def top_limit_pressed():
    return top_limit_pin.value()

def bottom_limit_pressed():
    return bottom_limit_pin.value()