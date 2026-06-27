import os
import sys
import time

from photobooth._base import create_camera, create_printer
from photobooth.user_interface import UserInterface

DEBUG = True

FOLDER_NAME = time.strftime("%Y%m%d/")
IMAGE_DIRECTORY = "images/camera_pictures/"
SAVE_DIRECTORY = IMAGE_DIRECTORY + FOLDER_NAME


class Photobooth():

    def __init__(self, fullscreen=False):
        self.camera = create_camera()
        self.printer = create_printer()
        self.ui = UserInterface(fullscreen=fullscreen)
        self.setup()

    def setup(self):
        connected = False
        while not connected:
            camera_status = self.camera.start()
            printer_status = self.printer.start()

            printer_name = self.printer.get_name()

            if camera_status and printer_status:
                self.ui.setup_screen("Connected", "Connected", printer_name)
            elif camera_status and not printer_status:
                self.ui.setup_screen("Connected", "Not Connected", printer_name)
            elif not camera_status and printer_status:
                self.ui.setup_screen("Not Connected", "Connected", printer_name)
            else:
                self.ui.setup_screen("Not Connected", "Not Connected", printer_name)

            key_pressed = self.ui.wait_for_input()
            if key_pressed == "ESC":
                sys.exit()
                return
            elif key_pressed == "F1":
                self.ui.toggle_fullscreen()
            elif key_pressed == "F2":
                self.printer.change_default_printer()
            elif key_pressed in ("DWN", "BTN"):
                connected = True
                self.ui.wait(300)
        if not os.path.exists(SAVE_DIRECTORY):
            if DEBUG:
                print("Creating a new folder at: {}".format(SAVE_DIRECTORY))
            os.makedirs(SAVE_DIRECTORY)

    def start(self):
        while True:
            if DEBUG:
                print("Showing Opening screen.")
            self.ui.opening_screen()
            key_pressed = self.ui.wait_for_input()

            if DEBUG:
                print("{} Key was pressed.".format(key_pressed))

            if key_pressed == "ESC":
                sys.exit()
                return
            elif key_pressed == "F1":
                self.ui.toggle_fullscreen()
            elif key_pressed == "F4":
                self.setup()
            elif key_pressed in ("DWN", "BTN"):
                self.camera.preview()
                self.start_picture_process()

    def start_picture_process(self, num_pics=3):
        if DEBUG:
            print("Starting picture process: {} pictures...".format(num_pics))
        images = []
        for i in range(num_pics):
            if DEBUG:
                print("Showing {} of {} screen.".format(i + 1, num_pics))
                print("Clock time since last tick: {}".format(self.ui.clock.get_time()))
            self.ui.x_of_y_screen(i + 1, num_pics)
            self.ui.wait(3000)

            if DEBUG:
                print("Showing countdown screen.")
                print("Clock time since last tick: {}".format(self.ui.clock.get_time()))
            self.ui.countdown_screen(self.camera)

            if DEBUG:
                print("Taking one picture and showing it on screen.")
            images.append(self.take_one_picture())
            self.ui.image_screen(images[i])
            self.ui.wait(3000)
            if DEBUG:
                print("Saving image #{} at: {}".format(i, images[i]))

        target = "{}final_image_{}.jpg".format(SAVE_DIRECTORY, time.strftime("%H%M"))
        final_image_location = self.ui.create_final_image(images, target)
        if DEBUG:
            print("Saving final image at {} and showing print screen.".format(final_image_location))
        self.ui.print_screen(final_image_location)
        self.ui.wait(5000)
        self.printer.print_file(final_image_location)

    def take_one_picture(self):
        time_name = time.strftime("%H%M%S")
        target = "{}{}.jpg".format(SAVE_DIRECTORY, time_name)
        if DEBUG:
            print("Taking one picture {}".format(time_name))
            print('Copying image to', target)
        success = False
        while not success:
            success = self.camera.capture(target)
            self.ui.wait(1000)
        return target
