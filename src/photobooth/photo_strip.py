import pygame as pg


class PhotoStrip:

    def __init__(self, print_dimensions: tuple[int, int] = (2, 6), dpi: int = 300):
        self._dimensions = (print_dimensions[0] * dpi, print_dimensions[1] * dpi)

    def compose(self, image_paths: list[str], target: str) -> str:
        image_surface, _ = self._load_and_scale("images/template.png", self._dimensions)

        image_positions = [(0, 0), (0, 435), (0, 435 * 2)]
        for i, path in enumerate(image_paths):
            img, _ = self._load_and_scale(path, (600, 403))
            image_surface.blit(img, image_positions[i])

        pg.image.save(image_surface, target)
        return target

    @staticmethod
    def _load_and_scale(file: str, scale: tuple[int, int]):
        image = pg.image.load(file)
        image_scaled = pg.transform.scale(image, scale)
        return image_scaled.convert(), image_scaled.get_rect()
