# -*- coding: utf-8 -*-

import random

from typing import List

from twisted.logger import Logger

import arcade

from game import FONT, FONT_THIN, SCREEN_WIDTH, SCREEN_HEIGHT
from game import app, cube

from network.factory import Worker, WorkerAction

player_count = 4
basic_spawn_count = 20
extra_spawn_count = 3
extra_spawn_time = 3.0
cube_max_count = 140

cube_size = 0.04

class GameView(arcade.View):
    __logger = Logger(__name__)

    def __init__(self):
        super().__init__()
        self.cube_index = 0
        self.cube_list: arcade.SpriteList = None
        self.pillar_1: arcade.Sprite = None
        self.pillar_2: arcade.Sprite = None

    def setup(self):
        self.cube_index = 0
        self.cube_list = arcade.SpriteList()
        cl = self.create_cube(basic_spawn_count * player_count, 0)
        arcade.get_window().game_server_factory.q.put(Worker(WorkerAction.cube_create, cl))
        self.cube_list.extend(cl)

        self.pillar_1 = arcade.Sprite('./game/resources/images/pillar.png', 0.39, center_x=940, center_y=662)
        self.pillar_2 = arcade.Sprite('./game/resources/images/pillar.png', 0.39, center_x=1710, center_y=662)

        arcade.set_background_color(arcade.color.SPACE_CADET)
        arcade.set_viewport(0, arcade.get_window().width, 0, arcade.get_window().height)

    def on_show_view(self):
        self.setup()
        arcade.schedule(self.extra_cube, extra_spawn_time)

    def on_draw(self):
        self.clear()
        self.cube_list.draw()
        self.pillar_1.draw()
        self.pillar_2.draw()
        output = f'Cube: {len(self.cube_list):03d}'
        arcade.draw_text(output, 10, SCREEN_HEIGHT-40, arcade.color.GREEN, 14)
        output = f'Cube index: {self.cube_index:03d}'
        arcade.draw_text(output, 10, SCREEN_HEIGHT-60, arcade.color.GREEN, 14)
        
    def on_update(self, delta_time: float):
        self.cube_list.update()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.unschedule(self.extra_cube)
        arcade.get_window().game_server_factory.q.put(Worker(WorkerAction.game_finish))
        arcade.get_window().set_state(app.ArcadeState.result)

    def extra_cube(self, delta_time: float) -> None:
        if len(self.cube_list) <= cube_max_count - extra_spawn_count:
            cl = self.create_cube(extra_spawn_count*player_count, 1)
            arcade.get_window().game_server_factory.q.put(Worker(WorkerAction.cube_create, cl))
            self.cube_list.extend(cl)
            self.__logger.info(f'added {extra_spawn_count*player_count} cube')
        else:
            self.__logger.info(f'can\'t add cube(max: {cube_max_count})')

    def create_cube(self, count, _type) -> List:
        cl = list()
        for i in range(count):
            c = cube.Cube(self.cube_index, _type, cube_size)
            sz = self.get_spawn_zone(random.randrange(0, 2))
            c.center_x = random.randrange(sz[0][0], sz[0][1])
            c.center_y = random.randrange(sz[1][0], sz[1][1])
            c.change_x = random.randrange(-1, 2)
            c.change_y = random.randrange(-1, 2)
            cl.append(c)
            self.cube_index += 1
        return cl

    def get_spawn_zone(self, area):
        if area == 0:
            return [
                (940-100, 940+100),
                (662-100, 662+100)
            ]
        elif area == 1:
            return [
                (1710-100, 1710+100),
                (662-100, 662+100)
            ]
        else:
            return [
                (0, SCREEN_WIDTH),
                (0, SCREEN_HEIGHT)
            ]
