import gphoto2 as gp
import io

class Camera():

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
            preview_file = camera.capture_preview()
            preview_file_data = preview_file.get_data_and_size()

            #this is loadable with pygame through pygame.image.load()
            loadable_preview_file = io.BytesIO(preview_file_data)
        except gp.GPhoto2Error:
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
            file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
            camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
            camera_file.save(save_dest)
            success = True
        except gp.GPhoto2Error:
            success = False

        return success
