from photobooth.config import Config


def test_defaults():
    config = Config()
    assert config.screen_size == (1280, 720)
    assert config.fullscreen is False
    assert config.font_size == 48
    assert config.fps == 30
    assert config.gpio_pin == 25
    assert config.num_pictures == 3
    assert config.countdown_seconds == 3.0
    assert config.image_directory == "images/camera_pictures/"
    assert config.print_dimensions == (2, 6)
    assert config.dpi == 300
    assert config.camera_backend == "gphoto2"
    assert config.hdmi_device == 0


def test_custom_config():
    config = Config(
        screen_size=(1920, 1080),
        fullscreen=True,
        camera_backend="hdmi",
        num_pictures=4,
    )
    assert config.screen_size == (1920, 1080)
    assert config.fullscreen is True
    assert config.camera_backend == "hdmi"
    assert config.num_pictures == 4
