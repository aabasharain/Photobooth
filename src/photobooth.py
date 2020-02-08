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
        if not os.path.exists(SAVE_DIRECTORY):
            if DEBUG:
                print("Creating a new folder at: {}".format(SAVE_DIRECTORY))
            os.makedirs(SAVE_DIRECTORY)
        
    def start(self):
        self.ui.opening_screen()
        key_pressed = self.ui.wait_for_input()
        
        if key_pressed == "ESC":
            sys.exit()
            return
        elif key_pressed == "F1":
            self.ui.toggle_fullscreen()
        elif key_pressed == "DWN":
            self.start_picture_process()
            
    def start_picture_process(self, num_pics = 3):
        images = [] #the file paths to each picture
        for i in range(num_pics):
            self.ui.x_of_y_screen(i, num_pics)
            self.ui.wait(3000)
            self.ui.countdown_screen(self.camera)
            
            images.append(self.take_one_picture())
            self.ui.image_screen(images[i])
            
        
    def take_one_picture():
        time_name = time.strftime("%H%M%S")
        target = "{}{}".format(SAVE_DIRECTORY, time_name)
        if DEBUG:
            print("Taking one picture {}".format(time_name))
            print('Copying image to', target)
        success = False
        while not success:
            success = self.camera.get_camera_capture(target)
            self.ui.wait(1000)
            
        return target
        
        