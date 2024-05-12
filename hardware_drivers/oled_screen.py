
from select import select
import time
from utime import sleep_us, ticks_cpu, ticks_us, ticks_diff  # type: ignore
from machine import Pin, SPI

import _thread as thread
from user_lib.ssd1309 import Display

from user_lib.pin_definitions import *
from hardware_drivers import select_button
from hardware_drivers.rotary_encoder import encoder

DISPLAY_WIDTH = 128  # Width of LCD display

spi = SPI(1, baudrate=10000000, sck=Pin(SCK_PIN_NUM), mosi=Pin(MOSI_PIN_NUM))
display = Display(spi, dc=Pin(OLED_DC_PIN_NUM), cs=Pin(OLED_CS_PIN_NUM), rst=Pin(OLED_RESET_PIN_NUM))

"""SSD1309 demo (bouncing boxes)."""
from random import random, seed



class Box(object):
    """Bouncing box."""

    def __init__(self, screen_width, screen_height, size, display):
        """Initialize box.
        Args:
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            size (int): Square side length.
            display (SSD1351): OLED display object.
        """
        self.size = size
        self.w = screen_width
        self.h = screen_height
        self.display = display
        SPEED_DIVIDER = 3
        # Generate non-zero random speeds between -5.0 and 5.0
        seed(ticks_cpu())
        r = random() * 10.0
        self.x_speed = (5.0 - r if r < 5.0 else r - 10.0)/SPEED_DIVIDER
        r = random() * 10.0
        self.y_speed = (5.0 - r if r < 5.0 else r - 10.0)/SPEED_DIVIDER

        self.x = self.w / 2.0
        self.y = self.h / 2.0
        self.prev_x = self.x
        self.prev_y = self.y

    def update_pos(self):
        """Update box position and speed."""
        x = self.x
        y = self.y
        size = self.size
        w = self.w
        h = self.h
        x_speed = abs(self.x_speed)
        y_speed = abs(self.y_speed)
        self.prev_x = x
        self.prev_y = y

        if x + size >= w - x_speed:
            self.x_speed = -x_speed
        elif x - size <= x_speed + 1:
            self.x_speed = x_speed

        if y + size >= h - y_speed:
            self.y_speed = -y_speed
        elif y - size <= y_speed + 1:
            self.y_speed = y_speed

        self.x = x + self.x_speed
        self.y = y + self.y_speed

    def draw(self):
        """Draw box."""
        x = int(self.x)
        y = int(self.y)
        size = self.size
        prev_x = int(self.prev_x)
        prev_y = int(self.prev_y)
        self.display.fill_rectangle(prev_x - size,
                                    prev_y - size,
                                    size, size, invert=True)
        self.display.fill_rectangle(x - size,
                                    y - size,
                                    size, size)
        self.display.present()

def write_text(texts: list):
    display.clear()
    x = 4
    y = 4
    y_increment = 16
    for text in texts:
        display.draw_text8x8(x,y,text)
        y += y_increment
    display.present()

def clear_display():
    display.clear()

def focus(line_num):
    line_height = 16 #pixels
    display.draw_rectangle(0,line_num*line_height, DISPLAY_WIDTH-1, line_height)
    display.present()
    
def test():
    """Bouncing box."""
    try:
        display.clear()

        sizes = [12, 11, 10, 9, 8, 7]
        boxes = [Box(128, 64, sizes[i], display) for i in range(6)]
        print("About to go")
        while True:
            timer = ticks_us()
            for b in boxes:
                b.update_pos()
                b.draw()
            # Attempt to set framerate to 30 FPS
            timer_dif = 33333 - ticks_diff(ticks_us(), timer)
            if timer_dif > 0:
                sleep_us(timer_dif)

    except KeyboardInterrupt:
        display.cleanup()

def idle_screen():
    sizes = [12, 11, 10, 9, 8, 7]
    boxes = [Box(128, 64, sizes[i], display) for i in range(6)]
    prev_enc_value = encoder.value()
    while not select_button.menu_select_pushed() and prev_enc_value == encoder.value():
        timer = ticks_us()
        for b in boxes:
            b.update_pos()
            b.draw()
        # Attempt to set framerate to 30 FPS
        timer_dif = 33333 - ticks_diff(ticks_us(), timer)
        if timer_dif > 0:
            sleep_us(timer_dif)

    while select_button.menu_select_pushed():
        time.sleep(0.1)

    time.sleep(0.1)
    display.clear()
        
