from photobooth.config import Config
from photobooth.controller.photobooth_controller import PhotoboothController

config = Config()
controller = PhotoboothController.from_config(config)
controller.run()
