import sys
sys.path.append("../src/")

from user_interface import UserInterface

ui = UserInterface()

ui.setup_screen("con", "not con")
ui.wait_for_input()

ui.opening_screen()
ui.wait_for_input()

ui.x_of_y_screen(1, 3)
ui.wait_for_input()

ui.print_screen("../images/photobooth_opening.png")
ui.wait_for_input()
