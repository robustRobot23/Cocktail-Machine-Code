import json
import _thread as thread
from user_lib.cocktails import Cocktail
from hardware_drivers import linear_actuator 
from hardware_drivers import pumps
from hardware_drivers import ssd1309_driver
from hardware_drivers import my_neopixel
from user_lib import neopixel_colours as npixel
from user_lib import oled_display
import time


def pour_liquor_shots(cocktail: Cocktail):
    with open('config/current_liquor.txt', 'r') as f:
        current_liquor = f.read().strip()

    if cocktail.liquor != current_liquor:
        print(f"Cannot make cocktail as {cocktail.liquor} not on machine, returning")
        return False
    if cocktail.shots_liquor == 0:
        print("Cannot pour liquor as cocktail has 0 shots, returning")
        return False
    if cocktail.shots_liquor >= 5:
        print("No, returning")
        return False
    
    thread.start_new_thread(linear_actuator.pour_shots, (cocktail.shots_liquor,))


def make_cocktail(cocktail: Cocktail):
    '''
    Run as a thread
    In charge of pouring the shots and dispensing the mixers
    '''
    oled_display.write_text(["", "Making Drink :)"])
    thread.start_new_thread(my_neopixel.chasing_colour, (npixel.CYAN,0.7))
    linear_actuator.pour_shots(cocktail.shots_liquor)


    pump_num = cocktail.value
    if pump_num > 2:
        pump_num = 0

    pumps.dispense(pump_num, 200)

    ssd1309_driver.clear_display()

    my_neopixel.end_animation()
    print("Ended chasing colours animation")
    
# def run_water_cycle():
#     pumps.dispense(1, )

def finished_drink():
    my_neopixel.set_single_colour(npixel.GREEN)
    ssd1309_driver.write_text(["Enjoy your drink"])
    print("Finished!")
    time.sleep(3)
    ssd1309_driver.clear_display()