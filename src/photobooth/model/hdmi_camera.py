import logging
from pathlib import Path

import cv2

from photobooth._base import CameraBase

logger = logging.getLogger(__name__)


class HDMICamera(CameraBase):

    def __init__(self, device: int = 0, resolution: tuple[int, int] | None = None):
        self._device = device
        self._resolution = resolution
        self._cap: cv2.VideoCapture | None = None

    def start(self) -> bool:
        self._cap = cv2.VideoCapture(self._device)
        if not self._cap.isOpened():
            logger.warning("Could not open video device %d", self._device)
            self._cap = None
            return False
        if self._resolution:
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._resolution[0])
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._resolution[1])
        return True

    def stop(self) -> None:
        if self._cap:
            self._cap.release()
            self._cap = None

    def preview(self) -> bytes | None:
        if self._cap is None:
            return None
        ret, frame = self._cap.read()
        if not ret:
            logger.warning("Failed to read frame from HDMI capture device")
            return None
        _, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return jpeg.tobytes()

    def capture(self, dest: str | Path) -> bool:
        if self._cap is None:
            return False
        ret, frame = self._cap.read()
        if not ret:
            logger.warning("Failed to capture still from HDMI device")
            return False
        cv2.imwrite(str(dest), frame)
        return True
