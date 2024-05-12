#module to pour a shot. Imported by main
import machine
import time
from user_lib.pin_definitions import *
from hardware_drivers import limits
raise_linear_actuator_pin = machine.Pin(RAISE_LINEAR_ACTUATOR_PIN_NUM, machine.Pin.OUT)
lower_linear_actuator_pin = machine.Pin(LOWER_LINEAR_ACTUATOR_PIN_NUM, machine.Pin.OUT)

def lower_linear_actuator():
    lower_linear_actuator_pin.on()

PAUSE_TIME_S = 3

def pour_shots(number_of_shots=1):
    print(f"Pouring {number_of_shots} shots")
    shots_poured = 0
    while shots_poured < number_of_shots:
        raise_linear_actuator_pin.on()
        while not limits.top_limit_pressed():
            time.sleep(0.05)
        raise_linear_actuator_pin.off()
        time.sleep(PAUSE_TIME_S)
        print("Lowering")
        lower_linear_actuator_pin.on()
        while not limits.bottom_limit_pressed():
            time.sleep(0.05)
        lower_linear_actuator_pin.off()
        shots_poured += 1
        print(f"Poured {shots_poured} shots")
        if shots_poured < number_of_shots:
            time.sleep(PAUSE_TIME_S)

def set_raise_pwm(duty):
    raise_linear_actuator_pin = machine.PWM(machine.Pin(RAISE_LINEAR_ACTUATOR_PIN_NUM), freq=1000, duty=duty)
    raise_linear_actuator_pin.duty = duty

def set_lower_pwm(duty):
    # lower_linear_actuator_pin = machine.PWM(machine.Pin(LOWER_LINEAR_ACTUATOR_PIN_NUM), freq=1000, duty=duty)
    while True:
        lower_linear_actuator_pin.on()
        time.sleep(0.1)
        lower_linear_actuator_pin.off()
        time.sleep(0.1)
    # lower_linear_actuator_pin.duty = duty