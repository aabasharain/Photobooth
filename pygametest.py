import sys
import pygame
import gphoto2 as gp

size = width, height = 480, 360 
black = 0, 0, 0

screen = pygame.display.set_mode(size)

context = gp.gp_context_new()
error, camera = gp.gp_camera_new()
error = gp.gp_camera_init(camera, context)

while True:
     for event in pygame.event.get():
           if event.type == pygame.QUIT: sys.exit()

     error, preview = gp.gp_camera_capture_preview(camera, context)
     pygame_preview = pygame.image.load(preview) 
     screen.fill(black)
     screen.blit(preview)
     pygame.display.flip()
 
