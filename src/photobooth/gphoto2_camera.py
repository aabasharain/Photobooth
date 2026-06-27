import gphoto2 as gp
import io

from photobooth._base import CameraBase


class Gphoto2Camera(CameraBase):

    def __init__(self):
        self.connected = False
        self._camera = None

    def start(self) -> bool:
        success = False
        try:
            self._camera = gp.Camera()
            self._camera.init()
            success = True
        except gp.GPhoto2Error:
            print("GPhoto2 error when trying to initialize camera...")
            success = False
        return success

    def stop(self) -> None:
        if self._camera:
            try:
                self._camera.exit()
            except gp.GPhoto2Error:
                pass

    def preview(self) -> bytes | None:
        try:
            preview_file = self._camera.capture_preview()
            return preview_file.get_data_and_size()
        except gp.GPhoto2Error:
            print("Error creating preview file...")
            return None

    def capture(self, dest: str | Path) -> bool:
        success = False
        try:
            file_path = self._camera.capture(gp.GP_CAPTURE_IMAGE)
            camera_file = self._camera.file_get(
                file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
            )
            camera_file.save(str(dest))
            success = True
        except gp.GPhoto2Error:
            success = False
        return success
