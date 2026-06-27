import sys
import time
from enum import Enum, auto
from pathlib import Path

from photobooth._base import CameraBase, PrinterBase, create_camera, create_printer
from photobooth.config import Config
from photobooth.controller.input_handler import InputHandler
from photobooth.exceptions import StateError
from photobooth.model.photo_strip import PhotoStrip
from photobooth.view.screens import View


class State(Enum):
    SETUP = auto()
    OPENING = auto()
    PROGRESS = auto()
    COUNTDOWN = auto()
    SHOW_CAPTURE = auto()
    COMPOSE = auto()
    PRINT = auto()
    EXIT = auto()


class PhotoboothController:
    def __init__(
        self,
        camera: CameraBase,
        printer: PrinterBase,
        input_handler: InputHandler,
        view: View,
        photo_strip: PhotoStrip,
        config: Config,
    ):
        self.camera = camera
        self.printer = printer
        self.input_handler = input_handler
        self.view = view
        self.photo_strip = photo_strip
        self.config = config

        self._state = State.SETUP
        self._pic_index = 0
        self._images: list[str] = []
        self._save_dir: Path | None = None

        self._handlers = {
            State.SETUP: self._do_setup,
            State.OPENING: self._do_opening,
            State.PROGRESS: self._do_progress,
            State.COUNTDOWN: self._do_countdown,
            State.SHOW_CAPTURE: self._do_show_capture,
            State.COMPOSE: self._do_compose,
            State.PRINT: self._do_print,
            State.EXIT: self._do_exit,
        }

    @classmethod
    def from_config(cls, config: Config) -> "PhotoboothController":
        camera = create_camera(config.camera_backend)
        printer = create_printer()
        input_handler = InputHandler(gpio_pin=config.gpio_pin)
        view = View(
            size=config.screen_size,
            fullscreen=config.fullscreen,
            font_size=config.font_size,
        )
        photo_strip = PhotoStrip(
            print_dimensions=config.print_dimensions,
            dpi=config.dpi,
        )
        return cls(
            camera=camera,
            printer=printer,
            input_handler=input_handler,
            view=view,
            photo_strip=photo_strip,
            config=config,
        )

    def run(self) -> None:
        while self._state != State.EXIT:
            handler = self._handlers.get(self._state)
            if handler is None:
                raise StateError(self._state)
            self._state = handler()

    def _handle_input(self) -> str | None:
        key = self.input_handler.wait()
        if key == "ESC":
            sys.exit()
        if key == "F1":
            self.view.toggle_fullscreen()
            return None
        return key

    def _do_setup(self) -> State:
        connected: bool = False
        while not connected:
            camera_ok = self.camera.start()
            printer_ok = self.printer.start()

            camera_status = "Connected" if camera_ok else "Not Connected"
            printer_status = "Connected" if printer_ok else "Not Connected"
            printer_name = self.printer.get_name()

            self.view.show_setup(camera_status, printer_status, printer_name)

            key = self.input_handler.wait()
            if key == "ESC":
                return State.EXIT
            if key == "F1":
                self.view.toggle_fullscreen()
            elif key == "F2":
                self.printer.change_default_printer()
            elif key in ("DWN", "BTN"):
                connected = True
                self.view.wait(300)

        self._save_dir = Path(self.config.image_directory) / time.strftime("%Y%m%d/")
        if not self._save_dir.exists():
            self._save_dir.mkdir(parents=True)
        return State.OPENING

    def _do_opening(self) -> State:
        self.view.show_opening()
        key = self.input_handler.wait()

        if key == "ESC":
            return State.EXIT
        if key == "F1":
            self.view.toggle_fullscreen()
            return State.OPENING
        if key == "F4":
            return State.SETUP
        if key in ("DWN", "BTN"):
            self._pic_index = 0
            self._images = []
            self.camera.preview()
            return State.PROGRESS
        return State.OPENING

    def _do_progress(self) -> State:
        self.view.show_progress(self._pic_index + 1, self.config.num_pictures)
        self.view.wait(3000)
        return State.COUNTDOWN

    def _do_countdown(self) -> State:
        count = self.config.countdown_seconds
        while count > 0:
            preview_data = self.camera.preview()
            self.view.show_countdown_frame(preview_data, count)
            count -= self.view.frame_time()
        self.view.show_caption("Strike a pose!")
        return State.SHOW_CAPTURE

    def _do_show_capture(self) -> State:
        time_name = time.strftime("%H%M%S")
        assert self._save_dir is not None
        target = str(self._save_dir / f"{time_name}.jpg")

        success = False
        while not success:
            success = self.camera.capture(target)
            self.view.wait(1000)

        self._images.append(target)
        self.view.show_image(target)
        self.view.wait(3000)

        self._pic_index += 1
        if self._pic_index < self.config.num_pictures:
            return State.PROGRESS
        return State.COMPOSE

    def _do_compose(self) -> State:
        target = str(
            self._save_dir / "final_image_{}.jpg".format(time.strftime("%H%M"))
        )
        self.photo_strip.compose(self._images, target)
        return State.PRINT

    def _do_print(self) -> State:
        target = str(
            self._save_dir / "final_image_{}.jpg".format(time.strftime("%H%M"))
        )
        self.view.show_print(target)
        self.view.wait(5000)
        self.printer.print_file(target)
        return State.OPENING

    def _do_exit(self) -> State:
        self.camera.stop()
        return State.EXIT
