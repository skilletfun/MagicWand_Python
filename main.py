import sys

import numpy as np
from PIL import Image


sys.setrecursionlimit(500000)


class ImageFiller():
    COLORS = {
        "white": (255,255,255),
        "black": (0,0,0),
        "red": (255,0,0),
        "green": (0,255,0),
        "blue": (0,0,255),
    }

    def __init__(self, color_range: int, fill_color: str = "white"):
        # color_range: допустимая разница между значениями канала (R, G, B)
        self.color_range = color_range
        self.fill_color = self.COLORS[fill_color]

    def fill(self, image: Image, point: tuple) -> Image:
        image = np.array(image)
        self.checked_points = set()
        self.contour = set()
        self._check_pixel(image, point)
        self._fill_by_pixels(image, self.contour, "red")

        inner_contour = self._find_outer_contour(min(self.contour))

        self._fill_by_pixels(image, inner_contour, "blue")

        self.checked_points = self.checked_points - inner_contour
        while inner_contour - self.checked_points != set():
            point = inner_contour.pop()
            self._fill_by_contour(image, point)

        return image

    def _find_outer_contour(self, point):
        outer_contour = set()
        outer_contour.add(point)
        self._check_contour_pixel(outer_contour, point)
        return self.contour - outer_contour

    def _check_contour_pixel(self, outer_contour, point):
        for step in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
            temp_point = point[0] + step[0], point[1] + step[1]
            if temp_point in self.contour and temp_point not in outer_contour:
                outer_contour.add(temp_point)
                self._check_contour_pixel(outer_contour, temp_point)

    def _check_pixel(self, image, point: tuple) -> None:
        if self._is_checkable(image, point):
            self.checked_points.add(point)
            if self._check_color(image[point]):
                image[point[0]][point[1]] = self.fill_color
                self._check_pixel(image, (point[0], point[1] + 1))
                self._check_pixel(image, (point[0] - 1, point[1]))
                self._check_pixel(image, (point[0] + 1, point[1]))
                self._check_pixel(image, (point[0], point[1] - 1))
            else:
                self.contour.add(point)
    
    def _is_checkable(self, image, point: tuple):
        return 0 <= point[0] < len(image[0]) and 0 <= point[1] < len(image) and point not in self.checked_points

    def _check_color(self, pix):
        # Проверка цвета пикселя на то, близок ли он по цвету к fill_color,
        # учитывая допустимую разницу color_range
        # True - пиксель попадает в допустимый диапазон, False - не попадает
        RGB_R = abs(pix[0] - self.fill_color[0])
        RGB_G = abs(pix[1] - self.fill_color[1])
        RGB_B = abs(pix[2] - self.fill_color[2])
        return RGB_R <= self.color_range and RGB_G <= self.color_range and RGB_B <= self.color_range

    def _fill_by_pixels(self, image, pixels: set, color: str):
        for pix in pixels:
            image[pix[0]][pix[1]] = self.COLORS[color]

    def _fill_by_contour(self, image, point: tuple):
        if self._is_checkable(image, point):
            self.checked_points.add(point)
            image[point[0]][point[1]] = self.fill_color
            self._fill_by_contour(image, (point[0], point[1] + 1))
            self._fill_by_contour(image, (point[0] - 1, point[1]))
            self._fill_by_contour(image, (point[0] + 1, point[1]))
            self._fill_by_contour(image, (point[0], point[1] - 1))

            self._fill_by_contour(image, (point[0] + 1, point[1] + 1))
            self._fill_by_contour(image, (point[0] - 1, point[1] - 1))
            self._fill_by_contour(image, (point[0] + 1, point[1] - 1))
            self._fill_by_contour(image, (point[0] - 1, point[1] + 1))


if __name__ == "__main__":
    image = Image.open("example.png")

    filler = ImageFiller(color_range=1)
    new_image = filler.fill(image=image, point=(100,40))

    image.close()
    image = Image.fromarray(new_image)
    image.show()
    image.close()
