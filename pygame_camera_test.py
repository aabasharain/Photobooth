import pygame as pg
import sys
import gphoto2 as gp
import io
import os
import time
from gpiozero import Button

DEBUG = True

FOLDER_NAME = time.strftime("%Y%m%d/")
IMAGE_DIRECTORY = "/home/pi/myphotobooth/images/"
SAVE_DIRECTORY = IMAGE_DIRECTORY + FOLDER_NAME
if not os.path.exists(SAVE_DIRECTORY):
    if DEBUG:
        print("Creating a new folder at: {}".format(SAVE_DIRECTORY))
    os.makedirs(SAVE_DIRECTORY)

#Colors and sizes
size = (1280, 720)
black = (0, 0, 0)
white = (255, 255, 255)
gray_half_alpha = pg.Color(127, 127, 127, a = 125)

#initialize pygame, it's background, font and clock
pg.init()
screen = pg.display.set_mode(size)
clock = pg.time.Clock()
pg.font.init()
font = pg.font.SysFont("TimesNewRoman", 36)

#img = pg.image.load("SAM_0138.JPG")
#img = pg.transform.scale(img, screen.get_size())
#imgrect = img.get_rect()
#img.convert()



#initialize camera
camera_connected = False
while not camera_connected:
    try:
        camera = gp.Camera()
        camera.init()
        camera_connected = True
    except gp.GPhoto2Error:
        print("Camera not detected, please turn camera on. Attempting to connect again in 3 seconds...")
        pg.time.wait(3000)

#initilize button
button = Button(25)

def update_screen():
    pg.display.flip()
    clock.tick(30)
#returns scaled camera preview image along with its corresponding rect
def get_camera_preview():
    preview_file = camera.capture_preview()
    preview_file_data = preview_file.get_data_and_size()
    preview_image = pg.image.load(io.BytesIO(preview_file_data))
    preview_image_scaled = pg.transform.scale(preview_image, screen.get_size())
    preview_image_convert = preview_image_scaled.convert()
    preview_image_rect = preview_image_scaled.get_rect()
    
    return preview_image_convert, preview_image_rect

def take_one_picture():
    time_name = time.strftime("%H%M%S")
    success = False
    while not success:
        try:
            file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
            success = True
        except gp.GPhoto2Error:
            print("Error taking picture, trying again in 1 second.")
            pg.time.wait(1000)
    
    
    target = "{}{}_{}".format(SAVE_DIRECTORY, time_name, file_path.name)
    
    if DEBUG:
        print('Camera file path: {0}{1}'.format(file_path.folder, file_path.name))
        print('Copying image to', target)
    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)

    camera_file.save(target)
    #capture_file_data = capture_file.get_data_and_size()
    capture_image = pg.image.load(target)
    capture_image_scaled = pg.transform.scale(capture_image, screen.get_size())
    capture_image_convert = capture_image_scaled.convert()
    capture_image_rect = capture_image_scaled.get_rect()
    
    return capture_image_convert, capture_image_rect, target

def take_pictures(surface, num_pics = 3, total_countdown_seconds = 3.0):
    surface_rect = surface.get_rect()
    center_screen = (int(surface_rect.width / 2), int(surface_rect.height / 2))
    #text_center_screen = (center_screen[0], center_screen[1])
    alpha_surface = pg.Surface((surface_rect.width, surface_rect.height))
    alpha_surface = alpha_surface.convert_alpha()
    alpha_surface.fill(pg.Color(0, 0, 0, 0))
    
    images = []
    
    for i in range(num_pics):
        text_surface = font.render("{} of {}".format(i+1, num_pics), True, black)
        text_rect = text_surface.get_rect(center = center_screen)
        surface.fill(white)
        surface.blit(text_surface, text_rect)
        update_screen()
        pg.time.wait(2000)
        update_screen()
        count = total_countdown_seconds
        while count > 0:
            update_screen()
            #get preview image and text surfaces
            preview_image, preview_image_rect = get_camera_preview()
            text_surface = font.render("{:.1f}".format(count), True, black)
            text_rect = text_surface.get_rect(center = center_screen)
            
            #fill to reset surfaces, so it doesn't leave traces of previous frame
            surface.fill(white)
            alpha_surface.fill(pg.Color(0, 0, 0, 0))
            
            #draw circle and blit everything in order onto surfaces
            circle_rect = pg.draw.circle(alpha_surface, pg.Color(255, 255, 255, 175), center_screen, int(size[0] / 16))
            #offset for the text because it doesn't get placed in the middle
            alpha_surface.blit(text_surface, text_rect)
            preview_image = preview_image.convert(surface)
            surface.blit(preview_image, preview_image_rect)
            surface.blit(alpha_surface, (0, 0))
            
            if DEBUG:
                print(count)
                print(clock.get_time() / 1000.0)
            count -= clock.get_time() / 1000.0

        surface.fill(white)
        text_surface = font.render("Strike a pose!", True, black)
        text_rect = text_surface.get_rect(center = center_screen)
        surface.blit(text_surface, text_rect)
        update_screen()
        
        capture_image, capture_image_rect, capture_image_target = take_one_picture()
        images.append(capture_image_target)

        screen.fill(white)
        surface.blit(capture_image, capture_image_rect)
        update_screen()
        pg.time.wait(3000)
        update_screen()

    return images

def create_final_image(surface, imgs, print_dimensions = (2, 6), dpi = 300):
    image_surface = pg.Surface((print_dimensions[0] * dpi, print_dimensions[1] * dpi))
    border_thickness = 25
    image_scale = 0.25
    time_name = time.strftime("%H%M")
    
    """
    vertical_middle = surface.get_rect().height / 2.0
    horizontal_middle = surface.get_rect().width / 2.0
    
    border_bar = pg.Rect(0, 0, surface.get_rect().width, surface.get_rect().height)
    vertical_bar = pg.Rect(horizontal_middle, 0, border_thickness, surface.get_rect().height)
    horizontal_bar = pg.Rect(0, vertical_middle, surface.get_rect().width, border_thickness)
    pg.draw.rect(surface, black, border_bar, border_thickness)
    pg.draw.rect(surface, black, vertical_bar)
    pg.draw.rect(surface, black, horizontal_bar)
    
    
    font_surface = font.render("EVENT NAME Photos!\nDATE", True, black)
    surface.blit(font_surface, (10, 10))
    """
    img_positions = [(0, 0), \
                     (0, image_surface.get_rect().height * 0.25), \
                     (0, image_surface.get_rect().height * 0.25)]
    
    for i in range(len(imgs)):
        current_image = pg.image.load(imgs[i])
        current_image_scaled = pg.transform.scale(current_image, (int(image_surface.get_rect().width), \
                                                              int(image_surface.get_rect().height * image_scale)))
        image_surface.blit(current_image_scaled, img_positions[i])
        
    surface.fill(white)
    image_surface_scaled = pg.transform.scale(image_surface, (int(image_surface.get_rect().width * 0.5),\
                                                              int(image_surface.get_rect().height * 0.5)))
    surface.blit(image_surface, (int(surface.get_rect().width * 0.33), 0))
    surface.blit(image_surface, (int(surface.get_rect().width * 0.66), 0))
    update_screen()
    pg.time.wait(5000)
    target = "{}final_image_{}.jpg".format(SAVE_DIRECTORY, time_name)
    if DEBUG:
        print("Saving final image to: {}".format(target))
    pg.image.save(surface, target)
    return target

def start_picture_process():
    if DEBUG:
        print("Taking pictures...")
    three_imgs = take_pictures(screen, num_pics = 3)
    final_img = create_final_image(screen, three_imgs)
    
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            if DEBUG:
                print("Exiting program...")
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F1:
                if DEBUG:
                    print("Entering Fullscreen...")
                screen = pg.display.set_mode(size, flags = pg.FULLSCREEN)
            elif event.key == pg.K_F2:
                if DEBUG:
                    print("Exiting Fullscreen...")
                screen = pg.display.set_mode(size)
            elif event.key == pg.K_SPACE:
                start_picture_process()
                
                #clears all pygame events, so that if you press space bar multiple
                #times it will only register the first one
                pg.event.clear()
            

    if button.is_pressed:
        if DEBUG:
            print("Pressed")
        start_picture_process()
            
    preview_image, preview_image_rect = get_camera_preview()
    opening_image = pg.image.load("{}photobooth_opening.png".format(IMAGE_DIRECTORY))
    opening_image_scaled = pg.transform.scale(opening_image, size)
    opening_image_rect = opening_image_scaled.get_rect()
    screen.fill(white)

    screen.blit(opening_image_scaled, opening_image_rect)
    update_screen()
