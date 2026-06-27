import os
import sys
import time
from pathlib import Path

from photobooth._base import create_camera, create_printer
from photobooth.config import Config
from photobooth.input_handler import InputHandler
from photobooth.photo_strip import PhotoStrip
from photobooth.user_interface import UserInterface

DEBUG = True


class Photobooth:

    def __init__(self, config: Config):
        self.config = config
        self.camera = create_camera(config.camera_backend)
        self.printer = create_printer()
        self.input_handler = InputHandler(gpio_pin=config.gpio_pin)
        self.photo_strip = PhotoStrip(
            print_dimensions=config.print_dimensions,
            dpi=config.dpi,
        )
        self.ui = UserInterface(
            size=config.screen_size,
            fullscreen=config.fullscreen,
            font_size=config.font_size,
        )
        self._save_dir: Path | None = None
        self._setup()

    def _setup(self):
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

            key_pressed = self.input_handler.wait()
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

        self._save_dir = Path(self.config.image_directory) / time.strftime("%Y%m%d/")
        if not self._save_dir.exists():
            if DEBUG:
                print("Creating a new folder at: {}".format(self._save_dir))
            self._save_dir.mkdir(parents=True)

    def start(self):
        while True:
            if DEBUG:
                print("Showing Opening screen.")
            self.ui.opening_screen()
            key_pressed = self.input_handler.wait()

            if DEBUG:
                print("{} Key was pressed.".format(key_pressed))

            if key_pressed == "ESC":
                sys.exit()
                return
            elif key_pressed == "F1":
                self.ui.toggle_fullscreen()
            elif key_pressed == "F4":
                self._setup()
            elif key_pressed in ("DWN", "BTN"):
                self.camera.preview()
                self.start_picture_process()

    def start_picture_process(self, num_pics: int | None = None):
        if num_pics is None:
            num_pics = self.config.num_pictures
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
            self.ui.countdown_screen(self.camera, total_countdown_seconds=self.config.countdown_seconds)

            if DEBUG:
                print("Taking one picture and showing it on screen.")
            images.append(self.take_one_picture())
            self.ui.image_screen(images[i])
            self.ui.wait(3000)
            if DEBUG:
                print("Saving image #{} at: {}".format(i, images[i]))

        target = str(self._save_dir / "final_image_{}.jpg".format(time.strftime("%H%M")))
        final_image_location = self.photo_strip.compose(images, target)
        if DEBUG:
            print("Saving final image at {} and showing print screen.".format(final_image_location))
        self.ui.print_screen(final_image_location)
        self.ui.wait(5000)
        self.printer.print_file(final_image_location)

    def take_one_picture(self):
        time_name = time.strftime("%H%M%S")
        target = str(self._save_dir / "{}.jpg".format(time_name))
        if DEBUG:
            print("Taking one picture {}".format(time_name))
            print('Copying image to', target)
        success = False
        while not success:
            success = self.camera.capture(target)
            self.ui.wait(1000)
        return target
