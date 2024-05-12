import json
import _thread as thread
from cocktails import Cocktail
from hardware_drivers import linear_actuator 
from hardware_drivers import pumps
from hardware_drivers import oled_screen
from hardware_drivers import my_neopixel
from user_lib import neopixel_colours as npixel
import time

mixers_filename = "config/pump_mixers.json"
with open(mixers_filename, 'r') as f:
    pump_mixers = json.load(f)
# print(pump_mixers["mixers"])
pump_mixers = pump_mixers["mixers"]
possible_mixers = ["Tonic",
                   "Orange Juice",
                   "Lemonade",
                   "Cranberry Juice"]

def set_mixer(pump_num, mixer):
    pump_mixers[pump_num] = mixer


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

# def dispense_mixers(cocktail: Cocktail):
#     pump_num = None
#     mixers_to_pour = cocktail
#     for pump_mixer in pump_mixers:
#         print(pump_mixer)
#         if pump_mixer["name"] == mixer:
#             pump_num = pump_mixer["pump"]

#     if pump_num is None:
#         print(f"Mixer '{mixer}' not in machine")
#         return


def make_drink(cocktail):
    '''
    Run as a thread
    In charge of pouring the shots and dispensing the mixers
    '''
    oled_screen.write_text(["", "Making Drink :)"])
    thread.start_new_thread(my_neopixel.chasing_colour, (npixel.CYAN,0.7))
    print("about to raise actuator")
    linear_actuator.pour_shots(1)

    if cocktail.value == 4:
        linear_actuator.pour_shots(2)
    else:
        linear_actuator.pour_shots(1)

    pump_num = cocktail.value
    if pump_num > 2:
        pump_num = 0

    pumps.dispense(pump_num, 200)

    oled_screen.clear_display()

    my_neopixel.end_animation()
    print("Ended chasing colours animation")
    

def finished_drink():
    my_neopixel.set_single_colour(npixel.GREEN)
    oled_screen.write_text(["Enjoy your drink"])
    print("Finished!")
    time.sleep(3)
    oled_screen.clear_display()