# Photobooth. Python application designed to run a photobooth setup with
# a Raspberry Pi, DSLR camera and a printer.
# Copyright (C) 2020  Aaron Basharain

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import gphoto2 as gp
import io

import io
import cv2
import numpy as np


class Camera:
    def __init__(self, device_index=0, width=1920, height=1080, warmup_frames=5):
        self.device_index = device_index
        self.width = width
        self.height = height
        self.warmup_frames = warmup_frames
        self.cap = None

    # ---- internal helpers ----
    @staticmethod
    def _sharpness_score(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    def _capture_sharpest(self, n_frames=5):
        if not self.is_connected():
            return None

        candidates = []
        for _ in range(n_frames):
            ret, frame = self.cap.read()
            if ret:
                candidates.append((self._sharpness_score(frame), frame))

        if not candidates:
            return None

        return max(candidates, key=lambda x: x[0])[1]

    def _frame_to_bytes(self, frame) -> io.BytesIO:
        ok, buf = cv2.imencode(".jpg", frame)
        if not ok:
            return None
        return io.BytesIO(buf.tobytes())

    # ---- public API ----
    def start(self) -> bool:
        self.cap = cv2.VideoCapture(self.device_index, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            self.cap = None
            return False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        for _ in range(self.warmup_frames):
            self.cap.read()

        return True

    def is_connected(self) -> bool:
        return self.cap is not None and self.cap.isOpened()

    def get_camera_preview(self) -> io.BytesIO:
        if not self.is_connected():
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        return self._frame_to_bytes(frame)

    def get_camera_capture(self, save_dest: str, n_frames=5) -> bool:
        frame = self._capture_sharpest(n_frames=n_frames)
        if frame is None:
            return False

        return cv2.imwrite(save_dest, frame)

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None


if __name__ == "__main__":
    cam = CaptureCardCamera(device_index=0)

    if cam.start() and cam.is_connected():
        preview_bytes = cam.get_camera_preview()
        # e.g. in pygame: pygame.image.load(preview_bytes)

        cam.get_camera_capture("capture.jpg")

    cam.release()


class CameraGP:
    def __init__(self):
        self.connected = False

    def is_connected(self):
        return self.connected

    def start(self):
        success = False
        try:
            self.camera = gp.Camera()
            self.camera.init()
            success = True
        except gp.GPhoto2Error:
            print("GPhoto2 error when trying to initialize camera...")
            success = False
        return success

    def get_camera_preview(self):
        try:
            preview_file = self.camera.capture_preview()
            preview_file_data = preview_file.get_data_and_size()

            # this is loadable with pygame through pygame.image.load()
            loadable_preview_file = io.BytesIO(preview_file_data)
        except gp.GPhoto2Error:
            print("Error creating preview file...")
            loadable_preview_file = False

        return loadable_preview_file

    def get_camera_capture(self, save_dest):
        """
        Captures an image from the camera and saves it at the passed in destination.
        Since the destination is passed in, it is not necessary to return the final image path.

        return - boolean of success
        """
        success = False
        try:
            file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            camera_file = self.camera.file_get(
                file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
            )
            camera_file.save(save_dest)
            success = True
        except gp.GPhoto2Error:
            success = False

        return success
