import unittest
from car import Car
from car.car import MAX_SPEED
import math


class TestCar(unittest.TestCase):
    def test_move(self):
        car = Car(None)
        car.set_speed(10)
        car.move()
        assert(car.get_position() == (10, 0))

        car.set_direction(math.pi / 2.0)
        car.move()
        assert(car.get_position() == (10, 10))

        car.set_direction(math.pi)
        car.move()
        assert (car.get_position() == (0, 10))

        # over max speed
        car.set_direction(5.0 / 4.0 * math.pi)
        car.set_speed(MAX_SPEED + 1)
        car.move()
        assert (car.get_position() == (-7, 3))

