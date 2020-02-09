import pygame as pg
from gpiozero import Button

BUTTON_GPIO_PIN = 25


class UserInterface():

    def __init__(self, size = (1280, 720), fullscreen = False, font_size = 48):
        #Colors and sizes
        self.size = size
        self.fullscreen = fullscreen
        self.colors_dict = {"black": pg.Color(0, 0, 0), "white": pg.Color(255, 255, 255), "green": pg.Color(0, 200, 0), "red": pg.Color(255, 0, 0)}
        self.ui_surfaces = {}

        self.center_screen = (int(self.size[0] / 2), int(self.size[1] / 2))

        #initialize pygame, it's background, font and clock
        pg.init()
        pg.display.set_caption('Photobooth')
        pg.font.init()
        if fullscreen:
            self.screen = pg.display.set_mode(size, flags = pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(size)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("TimesNewRoman", font_size)

        #for the physical button on the outside of the photobooth
        self.button = Button(BUTTON_GPIO_PIN)

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

    def scale_and_convert(self, file, scale = (1280, 720)):
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
                    elif event.key == pg.K_F3:
                        pg.event.clear()
                        return "F3"
                    elif event.key == pg.K_F4:
                        pg.event.clear()
                        return "F4"
                    elif event.key == pg.K_UP:
                        pg.event.clear()
                        return "UP"
                    elif event.key == pg.K_DOWN:
                        pg.event.clear()
                        return "DWN"


            if self.button.is_pressed:
                pg.event.clear()
                return "BUTTON"

    def setup_screen(self, camera_status, printer_status, camera_color = "red", printer_color = "red"):
        #setup here
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()

        camera_text = self.font.render("Camera status: {}".format(camera_status), True, self.colors_dict[camera_color])
        pos_x = self.center_screen[0]
        pos_y = self.center_screen[1] - 75
        camera_text_rect = camera_text.get_rect(center = (pos_x, pos_y))

        printer_text = self.font.render("Printer status: {}".format(printer_status), True, self.colors_dict[printer_color])
        printer_text_rect = printer_text.get_rect(center = (pos_x, pos_y + 75))

        instruction_text = self.font.render("Press Down to continue. Press F4 to refresh connection.", True, self.colors_dict["black"])
        instruction_text_rect = instruction_text.get_rect(center = (pos_x, pos_y + 225))


        surface.fill(self.colors_dict["white"])
        surface.blit(camera_text, camera_text_rect)
        surface.blit(printer_text, printer_text_rect)
        surface.blit(instruction_text, instruction_text_rect)
        self.set_screen_display(surface, surface_rect)

    def opening_screen(self):
        opening_image, opening_rect = self.scale_and_convert("../images/photobooth_opening.png")
        self.set_screen_display(opening_image, opening_rect)

    def x_of_y_screen(self, x, y):
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()

        text_surface = self.font.render("{} of {}".format(x, y), True, self.colors_dict["black"])
        text_rect = text_surface.get_rect(center = self.center_screen)
        surface.fill(self.colors_dict["white"])
        surface.blit(text_surface, text_rect)
        self.set_screen_display(surface, surface_rect)

    #needs testing to make sure camera works
    def countdown_screen(self, camera, total_countdown_seconds = 3.0):
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()

        alpha_surface = pg.Surface((surface_rect.width, surface_rect.height))
        alpha_surface = alpha_surface.convert_alpha()
        alpha_surface.fill(pg.Color(0, 0, 0, 0))

        count = total_countdown_seconds
        while count > 0:
            self.set_screen_display(surface, surface_rect)

            #get preview image and text surfaces from camera
            preview_image, preview_image_rect = self.scale_and_convert(camera.get_camera_preview())
            text_surface = self.font.render("{:.0f}".format(count), True, self.colors_dict["black"])
            text_rect = text_surface.get_rect(center = self.center_screen)

            #fill to reset surfaces, so it doesn't leave traces of previous frame
            surface.fill(self.colors_dict["white"])
            alpha_surface.fill(pg.Color(0, 0, 0, 0))

            #draw circle and blit everything in order onto surfaces
            circle_rect = pg.draw.circle(alpha_surface, pg.Color(255, 255, 255, 175), self.center_screen, int(size[0] / 16))
            alpha_surface.blit(text_surface, text_rect)

            surface.blit(preview_image, preview_image_rect)
            surface.blit(alpha_surface, (0, 0))

            #the clock get_time() gets the time between the last 2 clock ticks
            #the clock ticks every time the screen is updated
            count -= self.clock.get_time() / 1000.0

        surface.fill(self.colors_dict["white"])
        text_surface = self.font.render("Strike a pose!", True, self.colors_dict["black"])
        text_rect = text_surface.get_rect(center = self.center_screen)
        surface.blit(text_surface, text_rect)

        self.set_screen_display(surface, surface_rect)

    def image_screen(self, img):
        surface = pg.Surface(self.size)
        img_surface, img_rect = self.scale_and_convert(img)

        surface.blit(img_surface, img_rect)
        self.set_screen_display(surface, surface.get_rect())

    def print_screen(self, img):
        """
        Takes in the location of the 'final image' and makes a screen to show,
        the final image and inform the user that the photobooth is printing.
        """
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()
        img_surface, img_rect = self.scale_and_convert(img, scale = (100, 300))

        text = self.font.render("Printing...", True, self.colors_dict["black"])
        text_rect = text.get_rect(center = (self.center_screen[0], self.center_screen[1] + 150))

        surface.fill(self.colors_dict["white"])
        surface.blit(text, text_rect)
        surface.blit(img_surface, (int(self.center_screen[0] - img_rect.width / 2), int(img_rect.height / 2)))
        self.set_screen_display(surface, surface_rect)

    def create_final_image(images, print_dimensions = (2, 6), dpi = 300):
        """
        From 3 images, creates a final image to be used for printing, default
        settings is to be printed on a 2in x 6in photo strip at 300dpi.

        return - final image location
        """
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()
        image_surface = pg.Surface((print_dimensions[0] * dpi, print_dimensions[1] * dpi))
        image_surface.fill(self.colors_dict["white"])
        image_scale = 720.0 / 1800.0
        time_name = time.strftime("%H%M")

        image_positions = [(0, 0), (0, 455), (0, 455*2)]

        for i in range(len(imgs)):
            current_image = self.scale_and_convert(images[i], scale = (600, 403))
            image_surface.blit(current_image_scaled, image_positions[i])

        surface.fill(white)
        #scale to fit inside display since printed image is different resolution than what gets displayed
        image_surface_scaled = pg.transform.scale(image_surface, (int(image_surface.get_rect().width * image_scale),\
                                                                  int(image_surface.get_rect().height * image_scale)))
        surface.blit(image_surface_scaled, (int(surface_rect.width * 0.25), 0))
        surface.blit(image_surface_scaled, (int(surface_rect.width * 0.5), 0))

        target = "{}final_image_{}.jpg".format(SAVE_DIRECTORY, time_name)

        pg.image.save(image_surface, target)

        return target
