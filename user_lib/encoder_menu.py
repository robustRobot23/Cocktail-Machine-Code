# from user_lib.oled_display import write_text, clear_display, focus
from user_lib.cocktails import Cocktail
import time

class MenuItem:
    def __init__(self, name, action=None, content=None, submenu=None):
        self.name = name
        self.content = content
        self.submenu = submenu
        self.action = action

class Menu:
    def __init__(self, title, items=None):
        self.title = title
        self.items = items if items is not None else []
        self.selected_index = 0
    
    def navigate(self, direction):
        if direction == "up":
            self.selected_index -= 1
            if self.selected_index < 0:
                self.selected_index = len(self.items)-1
        elif direction == "down":
            self.selected_index += 1
            if self.selected_index >= len(self.items):
                self.selected_index = 0
                
    def add_item(self, item):
        self.items.append(item)

    def get_selected_item(self):
        return self.items[self.selected_index]
    
    def clear_items(self):
        self.items = []

    def display(self):
        # clear_display()
        if len(self.items) <= 4:
            display_items = self.items
            focus_index = self.selected_index
        elif len(self.items) - (self.selected_index + 1) < 4:
            display_items = self.items[-4 :]
            focus_index = 3 - (len(self.items) - (self.selected_index + 1))
            # print(f"index: {self.selected_index}, elif: {[item.name for item in display_items]}")
        else:
            display_items = self.items[self.selected_index: self.selected_index + 4]
            # print(f"index: {self.selected_index}, else: {[item.name for item in display_items]}")
            focus_index = 0

        text = [item.name for item in display_items]
        # write_text(text)
        print(text)
        print()
        # focus(focus_index)


