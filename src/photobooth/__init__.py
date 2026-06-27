import logging

from photobooth.config import Config
from photobooth.controller.photobooth_controller import PhotoboothController


def main():
    import sys  # noqa: PLC0415

    level = logging.DEBUG if "-d" in sys.argv or "--debug" in sys.argv else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )
    config = Config(fullscreen="-f" in sys.argv)
    controller = PhotoboothController.from_config(config)
    controller.run()
