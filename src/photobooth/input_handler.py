import pygame as pg
from gpiozero import Button


class InputHandler:

    def __init__(self, gpio_pin: int = 25):
        self.button = Button(gpio_pin)

    def wait(self) -> str:
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
                return "BTN"
