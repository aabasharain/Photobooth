from dataclasses import dataclass, field


@dataclass
class Config:
    screen_size: tuple[int, int] = (1280, 720)
    fullscreen: bool = False
    font_size: int = 48
    fps: int = 30
    gpio_pin: int = 25
    num_pictures: int = 3
    countdown_seconds: float = 3.0
    image_directory: str = "images/camera_pictures/"
    print_dimensions: tuple[int, int] = (2, 6)
    dpi: int = 300
    camera_backend: str = "gphoto2"
    hdmi_device: int = 0
