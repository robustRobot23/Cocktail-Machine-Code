import time
from user_lib.oled_display import Box, clear_display

from utime import sleep_us, ticks_cpu, ticks_us, ticks_diff  # type: ignore

from hardware_drivers.select_button import debounce_button, menu_select_pushed as button
from hardware_drivers.rotary_encoder import encoder
from user_lib.encoder_menu import MenuItem, Menu
from user_lib import cocktails
from make_drink import make_cocktail

main_menu = Menu("Main Menu")
cocktail_menu = Menu("Cocktail Menu")
service_menu = Menu("Service Menu")
set_mixer = Menu("Mixer Menu")
set_liquor = Menu("Liquor Menu")

main_menu.add_item(MenuItem("Cocktail Menu", submenu=cocktail_menu))
main_menu.add_item(MenuItem("Service Menu", submenu=service_menu))

service_menu.add_item(MenuItem("Change Liquor", submenu=set_liquor))
service_menu.add_item(MenuItem("Change Mixer 1", submenu=set_mixer))
service_menu.add_item(MenuItem("Change Mixer 2", submenu=set_mixer))
service_menu.add_item(MenuItem("Return"))

with open("config/liquor.txt", 'r') as f:
    liquor = f.read().strip()

with open("config/pump1.txt", 'r') as f:
    mixer_one = f.read().strip()

with open("config/pump2.txt", 'r') as f:
    mixer_two = f.read().strip()

def update_available_cocktails(new_mixer_one=None, new_mixer_two=None, new_liquor=None):
    global mixer_one, mixer_two, liquor
    if new_mixer_one:
        mixer_one = new_mixer_one
        with open("config/pump1.txt", 'w') as f:
            f.write(mixer_one)
    if new_mixer_two:
        mixer_two = new_mixer_two
        with open("config/pump2.txt", 'w') as f:
            f.write(mixer_two)
    if new_liquor:
        liquor = new_liquor
        with open("config/liquor.txt", 'w') as f:
            f.write(liquor)

    mixers = [mixer_one, mixer_two]
    cocktail_menu.clear_items()
    possible_cocktails = cocktails.get_possible_cocktails(liquor, mixers)
    for cocktail in possible_cocktails:
        cocktail_menu.add_item(MenuItem(cocktail.name, make_cocktail, cocktail))
    cocktail_menu.add_item(MenuItem("Return"))

def load_liquor_menu():
    set_liquor.clear_items()
    with open("config/all_mixers.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            set_mixer.add_item(MenuItem(line.strip()))
load_liquor_menu()

def load_mixers_menu():
    set_mixer.clear_items()
    with open("config/all_mixers.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            set_mixer.add_item(MenuItem(line.strip())) #doesn't need an action or submenu as case handled by menu navigator
load_mixers_menu()
class MenuNavigator:
    def __init__(self, root_menu: Menu):
        self.root_menu = root_menu
        self.current_menu = root_menu
        self.menu_stack = []

    def process_selection(self):
        '''
        The select button has been pressed, process it.
        '''
        if self.current_menu.title == "Mixer Menu":
            if self.menu_stack[-2] == "Change Mixer 1":
                new_mixer_one = self.current_menu.items[self.current_menu.selected_index]
                update_available_cocktails(new_mixer_one=new_mixer_one)
            elif self.menu_stack[-2] == "Change Mixer 2":
                new_mixer_two = self.current_menu.items[self.current_menu.selected_index]
                update_available_cocktails(new_mixer_two=new_mixer_two)

            self.current_menu = self.root_menu
            # self.current_menu = self.menu_stack.pop()
            return
        if self.current_menu.title == "Liquor Menu":
            if self.menu_stack[-2] == "Change Liquor":
                new_liquor = self.current_menu.items[self.current_menu.selected_index]
                update_available_cocktails(new_liquor=new_liquor)
            # self.current_menu = self.menu_stack.pop()
            self.current_menu = self.root_menu
            return 

        choice_idx = self.current_menu.selected_index
        if 0 <= choice_idx < len(self.current_menu.items):
            selected_item = self.current_menu.items[choice_idx]
            print(f"Selected: {selected_item.name}")
            if selected_item.name == "Return":
                if self.menu_stack:
                    self.current_menu = self.menu_stack.pop()
                else:
                    print("You are at the top-level menu.")
            elif selected_item.submenu:
                self.menu_stack.append(self.current_menu)
                self.current_menu = selected_item.submenu
            elif selected_item.action:
                if type(selected_item.content) == cocktails.Cocktail:
                    selected_item.action(selected_item.content) #cocktail maker will take write to screen, and block menu
                else:
                    selected_item.action()
            else:
                print("Invalid menu item.")
        else:
            print(f"Invalid choice of {choice_idx} outside bounds of menu")

    def navigate(self):
        prev_encoder_value = 0
        update_menu = True
        while True:
            encoder_value = encoder.value()
            if encoder_value > prev_encoder_value:
                self.current_menu.navigate("down")
                update_menu = True
            elif encoder_value < prev_encoder_value:
                self.current_menu.navigate("up")
                update_menu = True
            prev_encoder_value = encoder_value

            if debounce_button():
                update_menu = True

            if update_menu:
                self.current_menu.display()
                update_menu = False

navigator = MenuNavigator(main_menu)

def idle_screen():
    sizes = [12, 11, 10, 9, 8, 7]
    boxes = [Box(128, 64, sizes[i]) for i in range(6)]
    prev_enc_value = encoder.value()
    while not button() and prev_enc_value == encoder.value():
        timer = ticks_us()
        for b in boxes:
            b.update_pos()
            b.draw()
        # Attempt to set framerate to 30 FPS
        timer_dif = 33333 - ticks_diff(ticks_us(), timer)
        if timer_dif > 0:
            sleep_us(timer_dif)

    while button:
        time.sleep(0.1)

    time.sleep(0.1)
    clear_display()


# def run_cocktail_select_menu():
#     print("running menu")
#     prev_encoder_value = encoder.value()
#     update_menu = True
#     selected_item = False
#     while not selected_item:
        
#         if update_menu:
#             display_menu(menu)
#             update_menu = False
        
        # if button():
        #     time.sleep(0.1)
        #     if button():
        #         selected_item = menu.get_selected_item()
        #         print("Selected:", selected_item.name, selected_item.value)
        #         time.sleep(0.05)
        #         update_menu = True
        
        # encoder_value = encoder.value()
        # if encoder_value > prev_encoder_value:
        #     menu.navigate("down")
        #     update_menu = True
        # elif encoder_value < prev_encoder_value:
        #     menu.navigate("up")
        #     update_menu = True
        
#         prev_encoder_value = encoder_value

#     clear_display()
#     return selected_item




if __name__ == "__main__":
    update_available_cocktails()
    navigator.navigate()