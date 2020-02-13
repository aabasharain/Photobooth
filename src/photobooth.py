# Photobooth. Python application designed to run a photobooth setup with
# a Raspberry Pi, DSLR camera and a printer.
# Copyright (C) 2020  Aaron Basharain

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from camera import Camera
from user_interface import UserInterface
from printer import Printer
import sys
import os
import time

DEBUG = True

FOLDER_NAME = time.strftime("%Y%m%d/")
IMAGE_DIRECTORY = "../images/"
SAVE_DIRECTORY = IMAGE_DIRECTORY + FOLDER_NAME

class Photobooth():

    def __init__(self):
        self.camera = Camera()
        self.printer = Printer()
        self.ui = UserInterface()
        self.setup()

    def setup(self):
        #need error checking here
        #must have everything confirmed working before starting photobooth
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
            elif key_pressed == "DWN" or key_pressed == "BTN":
                connected = True
                self.ui.wait(300)
        if not os.path.exists(SAVE_DIRECTORY):
            if DEBUG:
                print("Creating a new folder at: {}".format(SAVE_DIRECTORY))
            os.makedirs(SAVE_DIRECTORY)

    def start(self):
        self.ui.update_screen()
        while True:
            if DEBUG:
                print("Showing Opening screen.")
            self.ui.update_screen() 
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
            elif key_pressed == "DWN" or key_pressed == "BTN":
                self.ui.update_screen()
                self.start_picture_process()

    def start_picture_process(self, num_pics = 3):
        if DEBUG:
            print("Starting picture process: {} pictures...".format(num_pics))
        images = [] #the file paths to each picture
        for i in range(num_pics):
            if DEBUG:
                print("Showing {} of {} screen.".format(i + 1, num_pics))
            self.ui.x_of_y_screen(i + 1, num_pics)
            self.ui.wait(3000)
            
            if DEBUG:
                print("Showing countdown screen.")
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
        self.printer.print_image(final_image_location)


    def take_one_picture(self):
        time_name = time.strftime("%H%M%S")
        target = "{}{}.jpg".format(SAVE_DIRECTORY, time_name)
        if DEBUG:
            print("Taking one picture {}".format(time_name))
            print('Copying image to', target)
        success = False
        while not success:
            success = self.camera.get_camera_capture(target)
            self.ui.wait(1000)

        return target
