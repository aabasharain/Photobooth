import pygame as pg
from gpiozero import Button

BUTTON_GPIO_PIN = 25


class UserInterface():
    
    def __init__(self, size = (1280, 720), fullscreen = False):
        #Colors and sizes
        self.size = size
        self.fullscreen = fullscreen
        self.colors_dict = {"black": pg.Color(0, 0, 0), "white": pg.Color(255, 255, 255)}
        self.ui_surfaces = {}

        #initialize pygame, it's background, font and clock
        pg.init()
        pg.font.init()
        if fullscreen:
            self.screen = pg.display.set_mode(size, flags = pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(size)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("TimesNewRoman", 48)
        
        #for the physical button on the outside of the photobooth
        self.button = Button(BUTTON_GPIO_PIN)
    
    def construct_surfaces(self):
        surfaces = ["SETUP", "OPENING", "COUNTDOWN", "PICTURE", "PRINTING"]
        for item in surfaces:
            surface = pg.Surface(self.size)
            self.ui_surfaces[item] = (surface, surface.get_rect())
        
        self.ui_surfaces["OPENING"] = (scale_and_convert("photobooth_opening.png"))        
    
    def update_screen(self):
        pg.display.flip()
        self.clock.tick(30)
        
    def toggle_fullscreen(self):
        if self.fullscreen:
            self.screen = pg.display.set_mode(size)
        else:
            self.screen = pg.display.set_mode(size, flags = pg.FULLSCREEN)
        self.fullscreen = not self.fullscreen
        
    def wait(self, amt):
        """
        Waiting functionality accessible outside of this class.
        """
        pg.time.wait(amt)
        self.update_screen()
        
    def scale_and_convert(self, file, scale = self.size):
        """
        Scales and then converts an image file to a pygame surface, convert is used for faster blit.
        
        returns - scaled and convert pygame surface and pygame rect
        """
        image = pg.image.load(file)
        image_scaled = pg.transform.scale(image, scale)
        image_convert = image_scaled.convert()
        image_rect = image_scaled.get_rect()
        
        return image_convert, image_rect
    
    def set_screen_display(self, surface, rect):
        self.screen.fill(self.colors_dict["white"])
        self.screen.blit(surface, rect)
        self.update_screen()
        
    def wait_for_input(self):
        """
        Sits and waits for some type of user input, either through the keyboard or the physical button.
        
        returns - string of the key that was pressed
        "BTN" - Physical button
        "ESC" - Escape key
        "F1" - F1 key
        "F2" - F2 key
        "DWN" - Down arrow key
        "UP" - Up arrow key
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.event.clear()
                    return "ESC"
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_F1:
                        pg.event.clear()
                        return "F1"
                    elif event.key == pg.K_F2:
                        pg.event.clear()
                        return "F2"
                    elif event.key == pg.K_UP:
                        pg.event.clear()
                        return "UP"
                    elif event.key == pg.K_DOWN:
                        pg.event.clear()
                        return "DWN"
                    

            if self.button.is_pressed:
                pg.event.clear()
                return "BUTTON"
            
    def setup_screen(self):
        #setup here
        
    def opening_screen(self):
        opening_image, opening_rect = scale_and_convert("photobooth_opening.png")
        set_screen_display(opening_image, opening_rect)
        
    def x_of_y_screen(self, x, y):
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()
        
        text_surface = self.font.render("{} of {}".format(x, y), True, black)
        text_rect = text_surface.get_rect(center = center_screen)
        surface.fill(white)
        surface.blit(text_surface, text_rect)
        self.set_display_screen(surface, surface.get_rect())
        
    def countdown_screen(self, camera, total_countdown_seconds = 3):
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()
        center_screen = (int(surface_rect.width / 2), int(surface_rect.height / 2))

        alpha_surface = pg.Surface((surface_rect.width, surface_rect.height))
        alpha_surface = alpha_surface.convert_alpha()
        alpha_surface.fill(pg.Color(0, 0, 0, 0))
    
        count = total_countdown_seconds
        while count > 0:
            self.set_screen_display(surface, surface_rect)
            
            #get preview image and text surfaces
            preview_image, preview_image_rect = self.scale_and_convert(camera.get_camera_preview())
            text_surface = self.font.render("{:.1f}".format(count), True, black)
            text_rect = text_surface.get_rect(center = center_screen)
            
            #fill to reset surfaces, so it doesn't leave traces of previous frame
            surface.fill(white)
            alpha_surface.fill(pg.Color(0, 0, 0, 0))
            
            #draw circle and blit everything in order onto surfaces
            circle_rect = pg.draw.circle(alpha_surface, pg.Color(255, 255, 255, 175), center_screen, int(size[0] / 16))
            alpha_surface.blit(text_surface, text_rect)
            
            surface.blit(preview_image, preview_image_rect)
            surface.blit(alpha_surface, (0, 0))

            count -= self.clock.get_time() / 1000.0

        surface.fill(white)
        text_surface = font.render("Strike a pose!", True, black)
        text_rect = text_surface.get_rect(center = center_screen)
        surface.blit(text_surface, text_rect)
        
        self.set_screen_display(surface, surface_rect)
        
    def image_screen(self, img):
        surface = pg.Surface(self.size)
        img_surface, img_rect = scale_and_convert(img)
        
        surface.blit(img_surface, img_rect)
        self.set_screen_display(surface, surface.get_rect())
        
    def create_final_image(images, print_dimensions = (2, 6), dpi = 300):
        image_surface = pg.Surface((print_dimensions[0] * dpi, print_dimensions[1] * dpi))
        image_surface.fill(white)
        image_scale = 720.0 / 1800.0
        time_name = time.strftime("%H%M")

        image_positions = [(0, 0), \
                         (0, 455), \
                         (0, 455*2)]
        
        for i in range(len(imgs)):
            current_image = self.scale_and_convert(images[i], scale = (600, 403))
            image_surface.blit(current_image_scaled, image_positions[i])
            
        surface.fill(white)
        #scale to fit inside display since printed image is different resolution than what gets displayed
        image_surface_scaled = pg.transform.scale(image_surface, (int(image_surface.get_rect().width * image_scale),\
                                                                  int(image_surface.get_rect().height * image_scale)))
        surface.blit(image_surface_scaled, (int(surface.get_rect().width * 0.25), 0))
        surface.blit(image_surface_scaled, (int(surface.get_rect().width * 0.5), 0))
        
        pg.time.wait(5000)
        target = "{}final_image_{}.jpg".format(SAVE_DIRECTORY, time_name)
        if DEBUG:
            print("Saving final image to: {}".format(target))
        pg.image.save(image_surface, target)
        return target
