from abc import ABC, abstractmethod
from pathlib import Path


class CameraBase(ABC):
    @abstractmethod
    def start(self) -> bool:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...

    @abstractmethod
    def preview(self) -> bytes | None:
        ...

    @abstractmethod
    def capture(self, dest: str | Path) -> bool:
        ...


class PrinterBase(ABC):
    @abstractmethod
    def start(self) -> bool:
        ...

    @abstractmethod
    def print_file(self, path: str) -> bool:
        ...


def create_camera(backend: str = "gphoto2") -> CameraBase:
    if backend == "gphoto2":
        from photobooth.model.gphoto2_camera import Gphoto2Camera
        return Gphoto2Camera()
    elif backend == "hdmi":
        from photobooth.model.hdmi_camera import HDMICamera
        return HDMICamera()
    raise ValueError(f"Unknown camera backend: {backend!r}")


def create_printer() -> PrinterBase:
    from photobooth.model.cups_printer import CupsPrinter
    return CupsPrinter()
