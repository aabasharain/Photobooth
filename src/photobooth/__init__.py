from photobooth.config import Config
from photobooth.controller.photobooth_controller import PhotoboothController


def main():
    import sys
    config = Config(fullscreen="-f" in sys.argv)
    controller = PhotoboothController.from_config(config)
    controller.run()
