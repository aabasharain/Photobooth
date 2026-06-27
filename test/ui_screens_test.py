from photobooth.model.gphoto2_camera import Gphoto2Camera
from photobooth.view.screens import View

camera = Gphoto2Camera()
camera.start()

view = View()

view.show_setup("con", "not con", "")
input()

view.show_opening()
input()

view.show_progress(1, 3)
input()

# view.show_countdown_frame(...)
# view.show_caption(...)

capture = camera.capture("/tmp/test_capture.jpg")
print("capture:", capture)

view.show_image("images/photobooth_opening.png")
input()

view.show_print("images/photobooth_opening.png")
input()
