from camera import Camera
from user_interface import UserInterface
from printer import Printer
import sys
import os
import time

DEBUG = True

FOLDER_NAME = time.strftime("%Y%m%d/")
IMAGE_DIRECTORY = "/home/pi/myphotobooth/images/"
SAVE_DIRECTORY = IMAGE_DIRECTORY + FOLDER_NAME

class Photobooth():

    def __init__(self):
        self.ui = UserInterface()
        self.camera = Camera()
        self.printer = Printer()

    def setup(self):
        #need error checking here
        #must have everything confirmed working before starting photobooth
        connected = False
        while not connected:
            camera_status = self.camera.start()
            printer_status = self.printer.start()

            if camera_status and printer_status:
                self.ui.setup_screen("Connected", "Connected", "green", "green")
            elif camera_status and not printer_status:
                self.ui.setup_screen("Connected", "Not Connected", "green", "red")
            elif not camera_status and printer_status:
                self.ui.setup_screen("Not Connected", "Connected", "red", "green")
            else:
                self.ui.setup_screen("Not Connected", "Not Connected", "red", "red")

            input = self.ui.wait_for_input()
            if input == "DWN":
                connected = True
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
