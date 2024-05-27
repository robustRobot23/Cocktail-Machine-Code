# import time
# from user_lib.encoder_menu import menu, display_menu, button, encoder
# from hardware_drivers.ssd1309_driver import display
# from user_lib.oled_display import Box, clear_display
# import time
# from utime import sleep_us, ticks_cpu, ticks_us, ticks_diff  # type: ignore
# from hardware_drivers import select_button
# from hardware_drivers.rotary_encoder import encoder
from user_lib.encoder_menu import MenuItem, Menu
from user_lib import cocktails
from make_drink import make_cocktail
main_menu = Menu("Main Menu")
cocktail_menu = Menu("Cocktail Menu")
service_menu = Menu("Service Menu")

main_menu.add_item(MenuItem("Cocktail Menu", submenu=cocktail_menu))
main_menu.add_item(MenuItem("Service Menu", submenu=service_menu))


with open("config/liquor.txt", 'r') as f:
    liquor = f.read().strip()

with open("config/pump1.txt", 'r') as f:
    mixer_one = f.read().strip()

with open("config/pump2.txt", 'r') as f:
    mixer_two = f.read().strip()

def update_available_cocktails():
    with open("config/pump1.txt", 'w') as f:
        f.write(mixer_one)
    with open("config/pump2.txt", 'w') as f:
        f.write(mixer_two)
    with open("config/liquor.txt", 'w') as f:
        f.write(liquor)
    mixers = [mixer_one, mixer_two]
    cocktail_menu.clear_items()
    possible_cocktails = cocktails.get_possible_cocktails(liquor, mixers)
    for cocktail in possible_cocktails:
        cocktail_menu.add_item(MenuItem(cocktail.name, make_cocktail, cocktail))
    cocktail_menu.add_item(MenuItem("Return"))

def run_water_cycle() {
    
}


class MenuNavigator:
    def __init__(self, root_menu: Menu):
        self.current_menu = root_menu
        self.menu_stack = []

    def process_selection(self):
        choice_idx = self.current_menu.selected_index
        if 0 <= choice_idx < len(self.current_menu.items):
            selected_item = self.current_menu.items[choice_idx]
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
        update_menu = True
        while True:
            # encoder_value = encoder.value()
            # if encoder_value > prev_encoder_value:
            #     menu.navigate("down")
            #     update_menu = True
            # elif encoder_value < prev_encoder_value:
            #     menu.navigate("up")
            #     update_menu = True
            choice = input(f"\nCurrently Selected: {self.current_menu.items[self.current_menu.selected_index].name}, Move up 'l', down 'r', or select 's': ").strip()
            
            if choice.lower() == 's':
                self.process_selection()
            
            if choice.lower() == 'l':
                self.current_menu.navigate("up")
                update_menu = True
            elif choice.lower() == 'r':
                self.current_menu.navigate("down")
                update_menu = True

            if update_menu:
                self.current_menu.display()

navigator = MenuNavigator(main_menu)

# def idle_screen():
#     sizes = [12, 11, 10, 9, 8, 7]
#     boxes = [Box(128, 64, sizes[i], display) for i in range(6)]
#     prev_enc_value = encoder.value()
#     while not select_button.menu_select_pushed() and prev_enc_value == encoder.value():
#         timer = ticks_us()
#         for b in boxes:
#             b.update_pos()
#             b.draw()
#         # Attempt to set framerate to 30 FPS
#         timer_dif = 33333 - ticks_diff(ticks_us(), timer)
#         if timer_dif > 0:
#             sleep_us(timer_dif)

#     while select_button.menu_select_pushed():
#         time.sleep(0.1)

#     time.sleep(0.1)
#     display.clear()


# def run_cocktail_select_menu():
#     print("running menu")
#     prev_encoder_value = encoder.value()
#     update_menu = True
#     selected_item = False
#     while not selected_item:
        
#         if update_menu:
#             display_menu(menu)
#             update_menu = False
        
#         if button():
#             time.sleep(0.1)
#             if button():
#                 selected_item = menu.get_selected_item()
#                 print("Selected:", selected_item.name, selected_item.value)
#                 time.sleep(0.05)
#                 update_menu = True
        
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