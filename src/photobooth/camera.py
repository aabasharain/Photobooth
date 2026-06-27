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
            preview_file = self.camera.capture_preview()
            preview_file_data = preview_file.get_data_and_size()

            #this is loadable with pygame through pygame.image.load()
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
            camera_file = self.camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
            camera_file.save(save_dest)
            success = True
        except gp.GPhoto2Error:
            success = False

        return success
