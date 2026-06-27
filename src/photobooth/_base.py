from abc import ABC, abstractmethod
from pathlib import Path

from photobooth.exceptions import CameraBackendError


class CameraBase(ABC):
    @abstractmethod
    def start(self) -> bool: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def preview(self) -> bytes | None: ...

    @abstractmethod
    def capture(self, dest: str | Path) -> bool: ...


class PrinterBase(ABC):
    @abstractmethod
    def start(self) -> bool: ...

    @abstractmethod
    def print_file(self, path: str) -> bool: ...


def create_camera(backend: str = "gphoto2") -> CameraBase:
    if backend == "gphoto2":
        from photobooth.model.gphoto2_camera import Gphoto2Camera  # noqa: PLC0415

        return Gphoto2Camera()
    if backend == "hdmi":
        from photobooth.model.hdmi_camera import HDMICamera  # noqa: PLC0415

        return HDMICamera()
    raise CameraBackendError(backend)


def create_printer() -> PrinterBase:
    from photobooth.model.cups_printer import CupsPrinter  # noqa: PLC0415

    return CupsPrinter()
