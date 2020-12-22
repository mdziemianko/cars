import math

class World:
    @classmethod
    def from_bmp(cls, path, renderer):
        from PIL import Image
        import numpy as np

        img = Image.open(path)
        map = np.transpose(np.array(img)[:, :, 0])
        return World(map, renderer)

    def __init__(self, route, renderer):
        self._route = route
        self._cars = []
        self._epoch = 0
        self._renderer = renderer
        renderer.set_route(self)
        self._selected = []
        self._generation = 0


    def add_selected(self, selected):
        self._selected.append(selected)

    def clear_selected(self):
        self._selected = []

    def get_selected(self):
        return self._selected

    def reset(self):
        self._epoch = 0
        self._cars = []
        self._generation = self._generation + 1

    def get_epoch(self):
        return self._epoch

    def distance_to_barrier(self, position, direction, max_range):
        for i in range(max_range, 0, -1):
            dx = math.cos(direction) * i
            dy = -math.sin(direction) * i
            (x, y) = position
            if self._route[round(x + dx), round(y + dy)] != 0:
                return i * 1.0 / max_range
        return 0

    def get_size(self):
        return self._route.shape

    def set_cars(self, cars):
        self._cars = cars

    def get_cars(self):
        return self._cars

    def get_route(self):
        return self._route

    def get_generation(self):
        return self._generation

    def epoch(self):
        self._epoch = self._epoch + 1
        for car in self._cars:
            if car.is_alive():
                car.move()

                (x, y) = car.get_position()
                if self._route[x, y] == 0:
                    car.set_alive(False)
                else:
                    car.steer(self)

    def evolve(self):
        self._renderer.clear()
        self.epoch()
        self._renderer.render(self._selected)

__all__ = ["World"]