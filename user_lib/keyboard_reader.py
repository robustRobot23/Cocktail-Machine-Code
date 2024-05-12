import sys
import utime
from hardware_drivers import linear_actuator as la
# Define key codes for arrow keys
KEY_UP = '\x1b[A'
KEY_DOWN = '\x1b[B'

# Function to read a key press
def get_key():
    return sys.stdin.read(1)

def up_pressed():
    key = get_key()
    if key:
        print(f"Key: {key}")
    if key == 'A':
        print("Up")
        return True
    return False

def down_pressed():
    key = get_key()
    if key == 'B':
        print("Down")
        return True
    return False

def raise_la_with_keys():
    while True:
        while up_pressed():
            la.raise_linear_actuator_pin.on()
        la.raise_linear_actuator_pin.off()

        while down_pressed():
            la.lower_linear_actuator_pin.on()
        la.lower_linear_actuator_pin.off()