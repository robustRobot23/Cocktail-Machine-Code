import time
from machine import Pin, PWM
from user_lib.pin_definitions import *

MOTOR_PWM_FREQ = 20000

# pump_1 = Pin(PUMP_1_PIN_NUM, Pin.OUT)
# pump_2 = Pin(PUMP_2_PIN_NUM, Pin.OUT)
# pump_3 = Pin(PUMP_3_PIN_NUM, Pin.OUT)
# pump_4 = Pin(PUMP_4_PIN_NUM, Pin.OUT)

pump_1 = PWM(Pin(PUMP_1_PIN_NUM), freq=MOTOR_PWM_FREQ, duty=0)
pump_2 = PWM(Pin(PUMP_2_PIN_NUM), freq=MOTOR_PWM_FREQ, duty=0)
pump_3 = PWM(Pin(PUMP_3_PIN_NUM), freq=MOTOR_PWM_FREQ, duty=0)
pump_4 = PWM(Pin(PUMP_4_PIN_NUM), freq=MOTOR_PWM_FREQ, duty=0)

pumps = [None, pump_1, pump_2, pump_3, pump_4] 

ML_PER_MIN = 500
MIN_PER_ML = 1/ML_PER_MIN
SEC_PER_ML = MIN_PER_ML * 60
MS_PER_ML = SEC_PER_ML * 1000

def dispense(pump_num, ml):

    if not pumps[pump_num]:
        return
    pump_on_time = SEC_PER_ML * ml
    print(f"Turning pump {pump_num} on for {pump_on_time} seconds")
    pumps[pump_num].duty(1023)
    time.sleep(pump_on_time)
    pumps[pump_num].duty(0)
    print(f"Pump {pump_num} finished dispensing")


# def dispense_mixer(mixer, ml):
    
    
    
    
