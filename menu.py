import time
from user_lib.encoder_menu import menu, display_menu, button, encoder
from hardware_drivers.oled_screen import clear_display
def run_cocktail_select_menu():
    print("running menu")
    prev_encoder_value = encoder.value()
    update_menu = True
    selected_item = False
    while not selected_item:
        
        if update_menu:
            display_menu(menu)
            update_menu = False
        
        if button():
            time.sleep(0.1)
            if button():
                selected_item = menu.get_selected_item()
                print("Selected:", selected_item.name, selected_item.value)
                time.sleep(0.05)
                update_menu = True
        
        encoder_value = encoder.value()
        if encoder_value > prev_encoder_value:
            menu.navigate("down")
            update_menu = True
        elif encoder_value < prev_encoder_value:
            menu.navigate("up")
            update_menu = True
        
        prev_encoder_value = encoder_value

    clear_display()
    return selected_item