import io

import pygame as pg
from pygame._freetype import Font as _FGFont, init as _ft_init


class _Font:
    """Thin wrapper around pygame._freetype.Font that normalizes
    render() to return Surface (matching pygame.font.Font API)."""

    def __init__(self, size: int):
        self._font = _FGFont(None, size)

    def render(
        self,
        text: str,
        antialias: bool,
        color: pg.Color | tuple[int, int, int],
        background: pg.Color | tuple[int, int, int] | None = None,
    ) -> pg.Surface:
        self._font.antialiased = bool(antialias)
        surf, _ = self._font.render(text, color, background)
        return surf


class View:

    def __init__(
        self,
        size: tuple[int, int] = (1280, 720),
        fullscreen: bool = False,
        font_size: int = 48,
    ):
        self.size = size
        self.fullscreen = fullscreen
        self.colors: dict[str, pg.Color] = {
            "black": pg.Color(0, 0, 0),
            "white": pg.Color(255, 255, 255),
            "green": pg.Color(0, 200, 0),
            "red": pg.Color(255, 0, 0),
        }
        self._center = (int(self.size[0] / 2), int(self.size[1] / 2))

        pg.init()
        _ft_init()
        pg.display.set_caption("Photobooth")
        if fullscreen:
            self.screen = pg.display.set_mode(size, flags=pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(size)
        self.clock = pg.time.Clock()
        self.clock.tick(30)
        self.font = _Font(font_size)

    def _update(self) -> None:
        pg.event.clear()
        pg.display.flip()
        self.clock.tick(30)

    def frame_time(self) -> float:
        return self.clock.get_time() / 1000.0

    def wait(self, ms: int) -> None:
        pg.time.wait(ms)
        self._update()
        self._update()

    def _load_and_scale(
        self,
        file: str | bytes,
        scale: tuple[int, int] | None = None,
    ) -> tuple[pg.Surface, pg.Rect]:
        if scale is None:
            scale = self.size
        image = pg.image.load(file)
        scaled = pg.transform.scale(image, scale)
        return scaled.convert(), scaled.get_rect()

    def _set_display(self, surface: pg.Surface, rect: pg.Rect) -> None:
        self.screen.fill(self.colors["white"])
        self.screen.blit(surface, rect)
        self._update()

    def toggle_fullscreen(self) -> None:
        if self.fullscreen:
            self.screen = pg.display.set_mode(self.size)
        else:
            self.screen = pg.display.set_mode(self.size, flags=pg.FULLSCREEN)
        self.fullscreen = not self.fullscreen
        self._update()

    def show_setup(
        self,
        camera_status: str,
        printer_status: str,
        printer_name: str,
    ) -> None:
        self._update()
        surface = pg.Surface(self.size)
        cx, cy = self._center

        camera_color = self.colors["green"] if camera_status == "Connected" else self.colors["red"]
        printer_color = self.colors["green"] if printer_status == "Connected" else self.colors["red"]

        texts = []
        texts.append((self.font.render(f"Camera status: {camera_status}", True, camera_color), (cx, cy - 150)))
        texts.append((self.font.render(f"Printer status: {printer_status}", True, printer_color), (cx, cy - 75)))
        if printer_status == "Connected":
            texts.append((self.font.render(f"Connected to: {printer_name}", True, self.colors["black"]), (cx, cy)))
        texts.append((self.font.render("Press Button or Down Arrow to continue.", True, self.colors["black"]), (cx, cy + 100)))
        texts.append((self.font.render("Press F1 to enter fullscreen.", True, self.colors["black"]), (cx, cy + 150)))
        texts.append((self.font.render("Press F2 to change default printer (in command line).", True, self.colors["black"]), (cx, cy + 200)))
        texts.append((self.font.render("Press F4 to refresh connection.", True, self.colors["black"]), (cx, cy + 250)))

        surface.fill(self.colors["white"])
        for text_surf, pos in texts:
            rect = text_surf.get_rect(center=pos)
            surface.blit(text_surf, rect)
        self._set_display(surface, surface.get_rect())

    def show_opening(self) -> None:
        self._update()
        img, rect = self._load_and_scale("images/photobooth_opening.png")
        self._set_display(img, rect)

    def show_progress(self, current: int, total: int) -> None:
        self._update()
        surface = pg.Surface(self.size)
        text = self.font.render(f"{current} of {total}", True, self.colors["black"])
        rect = text.get_rect(center=self._center)
        surface.fill(self.colors["white"])
        surface.blit(text, rect)
        self._set_display(surface, surface.get_rect())

    def show_countdown_frame(self, preview_data: bytes | None, remaining: float) -> None:
        surface = pg.Surface(self.size)
        surface_rect = surface.get_rect()

        if preview_data:
            preview_img, _ = self._load_and_scale(io.BytesIO(preview_data))
        else:
            preview_img = pg.Surface((surface_rect.width, surface_rect.height))
            preview_img.fill(self.colors["white"])

        alpha = pg.Surface((surface_rect.width, surface_rect.height))
        alpha = alpha.convert_alpha()
        alpha.fill(pg.Color(0, 0, 0, 0))

        text = self.font.render(f"{remaining:.0f}", True, self.colors["black"])
        text_rect = text.get_rect(center=self._center)

        pg.draw.circle(alpha, pg.Color(255, 255, 255, 175), self._center, int(self.size[0] / 16))
        alpha.blit(text, text_rect)

        surface.fill(self.colors["white"])
        surface.blit(preview_img, preview_img.get_rect())
        surface.blit(alpha, (0, 0))

        self._set_display(surface, surface_rect)

    def show_caption(self, text: str) -> None:
        surface = pg.Surface(self.size)
        text_surf = self.font.render(text, True, self.colors["black"])
        rect = text_surf.get_rect(center=self._center)
        surface.fill(self.colors["white"])
        surface.blit(text_surf, rect)
        self._set_display(surface, surface.get_rect())

    def show_image(self, path: str) -> None:
        self._update()
        img_surf, img_rect = self._load_and_scale(str(path))
        surface = pg.Surface(self.size)
        surface.blit(img_surf, img_rect)
        self._set_display(surface, surface.get_rect())

    def show_print(self, path: str) -> None:
        self._update()
        surface = pg.Surface(self.size)
        img_surf, img_rect = self._load_and_scale(str(path), scale=(100, 300))

        text = self.font.render("Printing...", True, self.colors["black"])
        text_rect = text.get_rect(center=(self._center[0], self._center[1] + 150))

        surface.fill(self.colors["white"])
        surface.blit(text, text_rect)
        x = int(self._center[0] - img_rect.width / 2)
        y = int(img_rect.height / 2)
        surface.blit(img_surf, (x, y))
        self._set_display(surface, surface.get_rect())
