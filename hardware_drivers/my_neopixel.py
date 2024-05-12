import machine, neopixel
from user_lib.pin_definitions import *
import _thread as thread
import time

NUM_NEOPIXELS = 24
npixel = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN_NUM), NUM_NEOPIXELS)

animation_thread_locker = thread.allocate_lock()


def set_single_colour(colour, brightness=0.5):
    assert brightness >= 0 and brightness <= 1

    bright_colour = tuple(int(colour_val * brightness) for colour_val in colour)

    for i in range(NUM_NEOPIXELS):
        npixel[i] = bright_colour

    npixel.write()

animate = False
def end_animation():
    animation_thread_locker.acquire()
    global animate
    animate = False
    animation_thread_locker.release()

def chasing_colour(colour, brightness=0.5, speed=50):
    '''
    Speed from 0 to 100
    '''
    bright_colour = tuple(int(colour_val * brightness) for colour_val in colour)  
    animation_thread_locker.acquire()
    global animate
    if animate == True:
        print("Another animation running, chasing colour wont run")
        return False
    animate = True
    animation_thread_locker.release()
    chasing_index = 0
    prev_index = 0

    other_chasing_index = int(NUM_NEOPIXELS/2)
    other_prev_index = other_chasing_index - 1

    sleep_time = (100 - speed)/1000
    play_animation = True
    for pixel in range(NUM_NEOPIXELS):
        npixel[pixel] = (0,0,0)
    print("Beginning Chasing Animation: Pixels cleared")
    
    while play_animation:
        npixel[prev_index] = (0,0,0)
        npixel[chasing_index] = bright_colour
        npixel[other_prev_index] = (0,0,0)
        npixel[other_chasing_index] = bright_colour
        npixel.write()
        prev_index = chasing_index
        other_prev_index = other_chasing_index
        chasing_index += 1
        other_chasing_index += 1
        if chasing_index >= NUM_NEOPIXELS:
            chasing_index = 0
        if other_chasing_index >= NUM_NEOPIXELS:
            other_chasing_index = 0

        time.sleep(sleep_time/2)

        animation_thread_locker.acquire()
        play_animation = animate
        animation_thread_locker.release()

    print("Chasing colours ended")
    thread.exit()

def fade_colour(colour, min_brightness=0, max_brightness=1, speed=100):
    print("Starting fade colour")

    animation_thread_locker.acquire()
    global animate
    if animate:
        print("Animation already running, cannot fade_colour")
        return False
    animate = True
    animation_thread_locker.release()
    
    max_animation_time = 5
    number_steps = 100 
    total_animation_time = max_animation_time * (speed/100)
    delay_time = total_animation_time / (number_steps*2)

    play_animation = True
    while play_animation:
        for brightness in range(min_brightness, max_brightness,1):
            bright_colour = tuple(int(colour_val * brightness) for colour_val in colour)            
            set_single_colour(bright_colour)
            time.sleep(delay_time)
            animation_thread_locker.acquire()
            play_animation = animate
            animation_thread_locker.release()
            if not play_animation:
                return
        
        for brightness in range(max_brightness, min_brightness,1):
            bright_colour = tuple(int(colour_val * brightness) for colour_val in colour)
            set_single_colour(bright_colour)
            time.sleep(delay_time)
            animation_thread_locker.acquire()
            play_animation = animate
            animation_thread_locker.release()
            if not play_animation:
                return
        
