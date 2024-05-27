# main.py -- put your code here!
import time
from user_lib.pin_definitions import *
from hardware_drivers import ssd1309_driver
from user_lib.cocktails import Cocktail
from make_drink import make_cocktail, finished_drink
import menu


while True:

    # thread.start_new_thread(my_neopixel.fade_colour(npixel.PINK))
    ssd1309_driver.idle_screen()
    # my_neopixel.end_animation()
    cocktail = menu.run_cocktail_select_menu()
    make_cocktail(cocktail)

    finished_drink()


# import machine
# machine.reset()      