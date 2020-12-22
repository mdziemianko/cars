import pygame as pg
import numpy as np
import math
from car.car import SENSORS, _normalize_direction, SENSOR_RANGE

class Renderer:
    def __init__(self):
        self._route = None
        self._screen = None
        self._background = None
        self._car_sprite = pg.image.load("../resources/car.png")
        pg.font.init()
        self._font = pg.font.SysFont('Comic Sans MS', 30)

    def set_route(self, route):
        self._route = route
        size = route.get_size()
        self._screen = pg.display.set_mode(size)
        background = np.zeros([size[0], size[1], 3])
        background[:, :, 0] = route.get_route()
        background[:, :, 1] = route.get_route()
        background[:, :, 2] = route.get_route()
        self._background = pg.surfarray.make_surface(background)


        self._screen.blit(self._background, (0, 0))



    def clear(self):
        self._screen.blit(self._background, (0, 0)) #rect, rect)

    def render(self, selected_cars):
        info_text = (
            f"Generation: {self._route.get_generation()}, " +
            f"epoch: {self._route.get_epoch()}"
        )
        rendered_info = self._font.render( info_text , False, (255, 0, 0))

        self._screen.blit(rendered_info, (10, 10))

        for c in self._route.get_cars():
            render_car(self._screen, self._car_sprite, c.get_position(), c.get_direction() * 180 / math.pi)
            for s in SENSORS:
                direction = _normalize_direction(s + c.get_direction())

                dx = math.cos(direction) * SENSOR_RANGE
                dy = -math.sin(direction) * SENSOR_RANGE
                (x, y) = c.get_position()
                pg.draw.line(self._screen, (0,0,255), (x, y), (x + dx, y+dy))
            #endfor
            if c in selected_cars:
                pg.draw.circle(self._screen, (255, 0, 0), c.get_position(), 15, 2)
        #endfor
        pg.display.update()


def render_car(surf, image, pos, angle):
    w, h = image.get_size()
    img_center = (w / 2, h / 2)

    bounding_box = [pg.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    rotated_box = [p.rotate(angle) for p in bounding_box]

    top_left = (min(rotated_box, key=lambda p: p[0])[0], min(rotated_box, key=lambda p: p[1])[1])
    bottom_right = (max(rotated_box, key=lambda p: p[0])[0], max(rotated_box, key=lambda p: p[1])[1])

    pivot = pg.math.Vector2(img_center[0], -img_center[1])
    rotated_pivot = pivot.rotate(angle)
    new_pivot = rotated_pivot - pivot

    position = (pos[0] - img_center[0] + top_left[0] - new_pivot[0], pos[1] - img_center[1] - bottom_right[1] + new_pivot[1])

    rotated_image = pg.transform.rotate(image, angle)

    surf.blit(rotated_image, position)

__all__ = ["Renderer"]
