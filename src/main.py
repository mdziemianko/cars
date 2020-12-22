import pygame as pg
from renderer.pygame import Renderer
from route import World
from car import Car
from car.car import SENSORS
from driver import NN

import sys

renderer = Renderer()
route = World.from_bmp("../resources/route1.bmp", renderer)
route.add_selected(Car(NN.blank_driver(len(SENSORS), 10)))

clock = pg.time.Clock()

done = False

generation = 0
while True:
    round_done = False

    route.reset()
    print(f"Starting generation {route.get_generation()}...")
    print(f"{len(route.get_selected())} parents available...")

    route.set_cars(Car.breed_from_selected(route.get_selected()))
    route.clear_selected()

    print(f"Generated {len(route.get_cars())} new drivers...")

    parents = []
    while not done and not round_done:
        clock.tick(10)
        route.evolve()

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                for c in route.get_cars():
                    (x, y) = c.get_position()
                    if abs(x - event.pos[0]) < 5 and abs(y - event.pos[1]) < 5:
                        route.add_selected(c)
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and len(route.get_selected()) > 0:
                    round_done = True





