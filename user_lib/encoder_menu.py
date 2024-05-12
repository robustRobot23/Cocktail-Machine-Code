from hardware_drivers.rotary_encoder import encoder
from hardware_drivers.select_button import menu_select_pushed as button
from hardware_drivers.oled_screen import write_text, clear_display, focus

import time

class MenuItem:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Menu:
    def __init__(self, items: list):
        self.items = items
        self.selected_index = 0
    
    def navigate(self, direction):
        if direction == "up":
            self.selected_index = int((self.selected_index - 1) % len(self.items))
        elif direction == "down":
            self.selected_index = int((self.selected_index + 1) % len(self.items))
        
    
    def get_selected_item(self):
        return self.items[self.selected_index]

def display_menu(menu: Menu):

    clear_display()
    # i = encoder.value()
    # print(f"Index: {menu.selected_index}, Option: {menu.get_selected_item().name}")
    if len(menu.items) <= 4:
        display_items = menu.items
        focus_index = menu.selected_index
    elif len(menu.items) - (menu.selected_index + 1) < 4:
        display_items = menu.items[-4 : len(menu.items)]
        focus_index = 3 - (len(menu.items) - (menu.selected_index + 1))
        # print(f"index: {menu.selected_index}, elif: {[item.name for item in display_items]}")
    else:
        display_items = menu.items[menu.selected_index: menu.selected_index + 4]
        # print(f"index: {menu.selected_index}, else: {[item.name for item in display_items]}")
        focus_index = 0

    text = [item.name for item in display_items]
    write_text(text)
    focus(focus_index)

# def one():
#     print("1")

# def two():
#     print("2")

items = [MenuItem("Gin & Tonic", 1), MenuItem("Gin & Lemonade", 2), MenuItem("Gin Shot", 3), MenuItem("Double Shot", 4)]
menu = Menu(items)


