import gphoto2 as gp
context = gp.gp_context_new()
error, camera = gp.gp_camera_new()
error = gp.gp_camera_init(camera, context)
error, text = gp.gp_camera_get_summary(camera, context)
print("Summary")
print(text.text)
error = gp.gp_camera_exit(camera, context)

