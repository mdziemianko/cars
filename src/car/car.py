import math

MAX_SPEED = 10
MAX_ACCELERATION = 3
MAX_DIRECTION = 45

SENSORS = [math.pi/2, math.pi/4, 0, 7 * math.pi / 4, 3 * math.pi / 2]
SENSOR_RANGE = 25

class Car:
    @classmethod
    def breed_from_selected(cls, parents):
        cars = []
        for p in parents:
            car = Car(p.get_driver())
            car.set_position((600, 120))
            cars.append(car)
            for i in range(0, 25):
                car = Car(p.get_driver().mutate())
                car.set_position((600, 120))
                cars.append(car)
        return cars


    def __init__(self, driver):
        self._alive = True
        self._driver = driver
        self._direction = 0
        self._speed = 0
        self._position = (0, 0)
        self._sensor_readings = None

    def get_driver(self):
        return self._driver

    def set_speed(self, speed):
        self._speed = MAX_SPEED if speed > MAX_SPEED else speed

    def set_direction(self, direction):
        self._direction = _normalize_direction(direction)

    def set_position(self, position):
        self._position = position

    def read_sensors(self, route):
        self._sensor_readings = [route.distance_to_barrier(self._position, _normalize_direction(sensor + self._direction), SENSOR_RANGE) for sensor in SENSORS]
        return self._sensor_readings

    def is_alive(self):
        return self._alive

    def set_alive(self, alive):
        self._alive = alive

    def get_position(self):
        return self._position

    def get_direction(self):
        return self._direction

    def get_speed(self):
        return self._speed

    def move(self):
        dx = math.cos(self._direction) * self._speed
        dy = -math.sin(self._direction) * self._speed
        (x, y) = self._position
        self.set_position((round(x + dx), round(y + dy)))

    def steer(self, route):
        situation = self.read_sensors(route)
        (d_acceleration, d_direction) = self._driver.steer(situation, self._speed, self._direction)

        self.set_speed(_normalize_speed(d_acceleration * MAX_ACCELERATION + self._speed))
        self.set_direction(_normalize_direction((d_direction * math.pi / 4) + self._direction))

def _normalize_speed(speed):
    if speed > MAX_SPEED:
        return MAX_SPEED
    elif speed < -MAX_SPEED:
        return -MAX_SPEED
    return speed

def _normalize_direction(direction):
    while direction < 0:
        direction = direction + 2 * math.pi
    while direction > 2 * math.pi:
        direction = direction - 2 * math.pi
    return direction

__all__ = ["Car"]