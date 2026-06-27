import pygame as pg
from gpiozero import Button


class InputHandler:
    def __init__(self, gpio_pin: int = 25):
        self.button = Button(gpio_pin)

    def wait(self) -> str:
        key_map = {
            pg.K_ESCAPE: "ESC",
            pg.K_F1: "F1",
            pg.K_F2: "F2",
            pg.K_F3: "F3",
            pg.K_F4: "F4",
            pg.K_UP: "UP",
            pg.K_DOWN: "DWN",
        }
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.event.clear()
                    return "ESC"
                if event.type == pg.KEYDOWN and event.key in key_map:
                    pg.event.clear()
                    return key_map[event.key]
            if self.button.is_pressed:
                pg.event.clear()
                return "BTN"
