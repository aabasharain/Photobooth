from unittest.mock import MagicMock

import pytest

from photobooth.config import Config
from photobooth.controller.photobooth_controller import (
    PhotoboothController,
    State,
)


@pytest.fixture
def config():
    return Config(image_directory="/tmp/")


@pytest.fixture
def mocks():
    return {
        "camera": MagicMock(),
        "printer": MagicMock(),
        "input_handler": MagicMock(),
        "view": MagicMock(),
        "photo_strip": MagicMock(),
    }


def make_ctrl(config, mocks):
    mocks["camera"].start.return_value = True
    mocks["camera"].capture.return_value = True
    mocks["camera"].preview.return_value = b"jpeg"
    mocks["printer"].start.return_value = True
    mocks["printer"].get_name.return_value = "Printer"
    mocks["view"].frame_time.return_value = 0.1
    mocks["photo_strip"].compose.return_value = "/tmp/final.jpg"
    return PhotoboothController(**mocks, config=config)


def test_initial_state_is_setup(config, mocks):
    ctrl = make_ctrl(config, mocks)
    assert ctrl._state == State.SETUP


def test_setup_to_opening_on_confirm(config, mocks):
    mocks["input_handler"].wait.side_effect = ["DWN", "ESC"]
    ctrl = make_ctrl(config, mocks)
    ctrl.run()
    assert ctrl._state == State.EXIT
    mocks["camera"].start.assert_called_once()
    mocks["printer"].start.assert_called_once()
    mocks["view"].show_setup.assert_called_once()
    mocks["view"].show_opening.assert_called_once()


def test_escape_from_setup(config, mocks):
    mocks["input_handler"].wait.side_effect = ["ESC"]
    ctrl = make_ctrl(config, mocks)
    ctrl.run()
    assert ctrl._state == State.EXIT


def test_full_photo_cycle(config, mocks):
    mocks["input_handler"].wait.side_effect = ["DWN", "DWN", "ESC"]
    ctrl = make_ctrl(config, mocks)
    ctrl.run()
    assert ctrl._state == State.EXIT
    assert len(ctrl._images) == 3
    assert mocks["camera"].capture.call_count == 3
    mocks["photo_strip"].compose.assert_called_once()


def test_f4_refreshes_setup(config, mocks):
    mocks["input_handler"].wait.side_effect = ["DWN", "F4", "DWN", "ESC"]
    ctrl = make_ctrl(config, mocks)
    ctrl.run()
    assert ctrl._state == State.EXIT
    assert mocks["camera"].start.call_count == 2


def test_f1_toggles_fullscreen(config, mocks):
    mocks["input_handler"].wait.side_effect = ["F1", "DWN", "ESC"]
    ctrl = make_ctrl(config, mocks)
    ctrl.run()
    mocks["view"].toggle_fullscreen.assert_called_once()


def test_printer_change_in_setup(config, mocks):
    mocks["input_handler"].wait.side_effect = ["F2", "DWN", "ESC"]
    ctrl = make_ctrl(config, mocks)
    ctrl.run()
    mocks["printer"].change_default_printer.assert_called_once()
