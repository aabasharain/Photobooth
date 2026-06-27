import io

import pygame as pg

from photobooth._base import CameraBase


class UserInterface:

    def __init__(self, size=(1280, 720), fullscreen=False, font_size=48):
        self.size = size
        self.fullscreen = fullscreen
        self.colors_dict = {
            "black": pg.Color(0, 0, 0),
            "white": pg.Color(255, 255, 255),
            "green": pg.Color(0, 200, 0),
            "red": pg.Color(255, 0, 0),
        }

        self.center_screen = (int(self.size[0] / 2), int(self.size[1] / 2))

        pg.init()
        pg.display.set_caption('Photobooth')
        if fullscreen:
            self.screen = pg.display.set_mode(size, flags=pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(size)
        self.clock = pg.time.Clock()
        self.clock.tick(30)
        self.font = pg.font.SysFont("TimesNewRoman", font_size)

    def update_screen(self):
        pg.event.clear()
        pg.display.flip()
        self.clock.tick(30)

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.screen = pg.display.set_mode(self.size)
        else:
            self.screen = pg.display.set_mode(self.size, flags=pg.FULLSCREEN)
        self.fullscreen = not self.fullscreen
        self.update_screen()

    def wait(self, amt):
        pg.time.wait(amt)
        self.update_screen()
        self.update_screen()

    def scale_and_convert(self, file, scale=(1280, 720)):
        image = pg.image.load(file)
        image_scaled = pg.transform.scale(image, scale)
        image_convert = image_scaled.convert()
        image_rect = image_scaled.get_rect()
        return image_convert, image_rect

    def set_screen_display(self, surface, rect):
        self.screen.fill(self.colors_dict["white"])
        self.screen.blit(surface, rect)
        self.update_screen()

    def setup_screen(self, camera_status, printer_status, printer_name):
        self.update_screen()
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()

        if camera_status == "Connected":
            camera_color = self.colors_dict["green"]
        else:
            camera_color = self.colors_dict["red"]

        camera_text = self.font.render("Camera status: {}".format(camera_status), True, camera_color)
        pos_x = self.center_screen[0]
        pos_y = self.center_screen[1] - 150
        camera_text_rect = camera_text.get_rect(center=(pos_x, pos_y))

        if printer_status == "Connected":
            printer_color = self.colors_dict["green"]
            printer_name_text = self.font.render("Connected to: {}".format(printer_name), True, self.colors_dict["black"])
        else:
            printer_color = self.colors_dict["red"]
            printer_name_text = self.font.render("", True, self.colors_dict["black"])

        printer_text = self.font.render("Printer status: {}".format(printer_status), True, printer_color)
        printer_text_rect = printer_text.get_rect(center=(pos_x, pos_y + 75))
        printer_name_rect = printer_name_text.get_rect(center=(pos_x, pos_y + 150))

        instruction_text = self.font.render("Press Button or Down Arrow to continue.", True, self.colors_dict["black"])
        instruction_text_rect = instruction_text.get_rect(center=(pos_x, pos_y + 250))

        instruction_text1 = self.font.render("Press F1 to enter fullscreen.", True, self.colors_dict["black"])
        instruction_text1_rect = instruction_text1.get_rect(center=(pos_x, pos_y + 300))

        instruction_text2 = self.font.render("Press F2 to change default printer (in command line).", True, self.colors_dict["black"])
        instruction_text2_rect = instruction_text2.get_rect(center=(pos_x, pos_y + 350))

        instruction_text3 = self.font.render("Press F4 to refresh connection.", True, self.colors_dict["black"])
        instruction_text3_rect = instruction_text3.get_rect(center=(pos_x, pos_y + 400))

        surface.fill(self.colors_dict["white"])
        surface.blit(camera_text, camera_text_rect)
        surface.blit(printer_text, printer_text_rect)
        surface.blit(printer_name_text, printer_name_rect)
        surface.blit(instruction_text, instruction_text_rect)
        surface.blit(instruction_text1, instruction_text1_rect)
        surface.blit(instruction_text2, instruction_text2_rect)
        surface.blit(instruction_text3, instruction_text3_rect)
        self.set_screen_display(surface, surface_rect)

    def opening_screen(self):
        self.update_screen()
        opening_image, opening_rect = self.scale_and_convert("images/photobooth_opening.png")
        self.set_screen_display(opening_image, opening_rect)

    def x_of_y_screen(self, x, y):
        self.update_screen()
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()

        text_surface = self.font.render("{} of {}".format(x, y), True, self.colors_dict["black"])
        text_rect = text_surface.get_rect(center=self.center_screen)
        surface.fill(self.colors_dict["white"])
        surface.blit(text_surface, text_rect)
        self.set_screen_display(surface, surface_rect)

    def countdown_screen(self, camera: CameraBase, total_countdown_seconds=3.0):
        self.update_screen()
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()

        alpha_surface = pg.Surface((surface_rect.width, surface_rect.height))
        alpha_surface = alpha_surface.convert_alpha()
        alpha_surface.fill(pg.Color(0, 0, 0, 0))

        count = total_countdown_seconds
        while count > 0:
            preview_data = camera.preview()
            if preview_data:
                preview_image, preview_image_rect = self.scale_and_convert(io.BytesIO(preview_data))
            else:
                preview_image = pg.Surface((surface_rect.width, surface_rect.height))
                preview_image_rect = preview_image.get_rect()
                preview_image.fill(self.colors_dict["white"])

            text_surface = self.font.render("{:.0f}".format(count), True, self.colors_dict["black"])
            text_rect = text_surface.get_rect(center=self.center_screen)

            surface.fill(self.colors_dict["white"])
            alpha_surface.fill(pg.Color(0, 0, 0, 0))

            pg.draw.circle(alpha_surface, pg.Color(255, 255, 255, 175), self.center_screen, int(self.size[0] / 16))
            alpha_surface.blit(text_surface, text_rect)

            surface.blit(preview_image, preview_image_rect)
            surface.blit(alpha_surface, (0, 0))

            self.set_screen_display(surface, surface_rect)
            count -= self.clock.get_time() / 1000.0

        surface.fill(self.colors_dict["white"])
        text_surface = self.font.render("Strike a pose!", True, self.colors_dict["black"])
        text_rect = text_surface.get_rect(center=self.center_screen)
        surface.blit(text_surface, text_rect)
        self.set_screen_display(surface, surface_rect)

    def image_screen(self, img):
        self.update_screen()
        surface = pg.Surface(self.size)
        img_surface, img_rect = self.scale_and_convert(img)
        surface.blit(img_surface, img_rect)
        self.set_screen_display(surface, surface.get_rect())

    def print_screen(self, img):
        self.update_screen()
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()
        img_surface, img_rect = self.scale_and_convert(img, scale=(100, 300))

        text = self.font.render("Printing...", True, self.colors_dict["black"])
        text_rect = text.get_rect(center=(self.center_screen[0], self.center_screen[1] + 150))

        surface.fill(self.colors_dict["white"])
        surface.blit(text, text_rect)
        surface.blit(img_surface, (int(self.center_screen[0] - img_rect.width / 2), int(img_rect.height / 2)))
        self.set_screen_display(surface, surface_rect)
