import gphoto2 as gp
import io

class Camera():
    
    def __init__(self):
        self.connected = False
        self.camera = initialize_camera()
        
    def is_connected(self):
        return self.connected
    
    def initialize_camera(self):
        try:
            camera = gp.Camera()
            camera.init()
            self.connected = True
            return camera
        except gp.GPhoto2Error:
            self.connected = False
                
    def get_camera_preview(self):
        success = False
        try:
            preview_file = camera.capture_preview()
            preview_file_data = preview_file.get_data_and_size()
        
            #this is loadable with pygame through pygame.image.load()
            loadable_preview_file = io.BytesIO(preview_file_data)
            success = True
        except gp.GPhoto2Error:
            loadable_preview_file = ""
            success = False
        
        return loadable_preview_file, success
    
    def get_camera_capture(self, save_dest):
        """
        Captures an image from the camera and saves it at the passed in destination. Since the destination is passed in, it is not necessary to
        return the final image path.
        
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
    
