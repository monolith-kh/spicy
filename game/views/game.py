# -*- coding: utf-8 -*-

import random

from typing import List

from twisted.logger import Logger

import arcade

from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane

from game import FONT, FONT_THIN, SCREEN_WIDTH, SCREEN_HEIGHT
from game import app, cube

from network.factory import Worker, WorkerAction

cube_size = 0.04


class GameView(arcade.View):
    __logger = Logger(__name__)

    def __init__(self):
        super().__init__()
        self.cube_index = 0
        self.cube_list = self.window.game_server_factory.cube_list
        self.settings: app.Settings = self.window.settings
        self.pillar_1: arcade.Sprite = None
        self.pillar_2: arcade.Sprite = None
        self.manager = UIManager()
        self.number_of_cubes_ui: UITextArea = None
        self.cube_index_ui: UITextArea = None

    def setup(self):
        self.cube_index = 0
        cl = self.create_cube(self.settings.basic_spawn_count * self.settings.number_of_players, 0)
        arcade.get_window().game_server_factory.q.put(Worker(WorkerAction.cube_create, cl))
        self.cube_list.extend(cl)

        self.pillar_1 = arcade.Sprite('./game/resources/images/pillar.png', 0.39, center_x=940, center_y=662)
        self.pillar_2 = arcade.Sprite('./game/resources/images/pillar.png', 0.39, center_x=1710, center_y=662)

        self.settings: app.Settings = self.window.settings

        self.manager.enable()

        v_box = arcade.gui.UIBoxLayout(vertical=True)
        self.number_of_cubes_ui = UITextArea(
            text=f'Number of Cubes: {len(self.cube_list):03d}',
            width=450,
            height=40,
            text_color=arcade.color.GREEN,
            font_size=14,
            font_name=FONT
        )
        v_box.add(self.number_of_cubes_ui.with_space_around(bottom=0))

        self.cube_index_ui = UITextArea(
                    text=f'Cube index: {self.cube_index:03d}',
                    width=450,
                    height=40,
                    text_color=arcade.color.GREEN,
                    font_size=14,
                    font_name=FONT
            )
        v_box.add(self.cube_index_ui.with_space_around(bottom=0))

        v_box.add(
            UITextArea(
                    text=f'Number of Players: {str(self.settings.number_of_players)}',
                    width=450,
                    height=40,
                    text_color=arcade.color.GREEN,
                    font_size=14,
                    font_name=FONT
            ).with_space_around(bottom=0)
        )

        v_box.add(
            UITextArea(
                    text=f'Basic spawn count: {str(self.settings.basic_spawn_count)}',
                    width=450,
                    height=40,
                    text_color=arcade.color.GREEN,
                    font_size=14,
                    font_name=FONT
            ).with_space_around(bottom=0)
        )

        v_box.add(
            UITextArea(
                    text=f'Auto spawn count: {str(self.settings.auto_spawn_count)}',
                    width=450,
                    height=40,
                    text_color=arcade.color.GREEN,
                    font_size=14,
                    font_name=FONT
            ).with_space_around(bottom=0)
        )

        v_box.add(
            UITextArea(
                    text=f'Auto spawn sec tick: {str(self.settings.auto_spawn_time)}',
                    width=450,
                    height=40,
                    text_color=arcade.color.GREEN,
                    font_size=14,
                    font_name=FONT_THIN
            ).with_space_around(bottom=0)
        )

        v_box.add(
            UITextArea(
                    text=f'Max spawn count: {str(self.settings.max_spawn_count)}',
                    width=450,
                    height=40,
                    text_color=arcade.color.GREEN,
                    font_size=14,
                    font_name=FONT
            ).with_space_around(bottom=10)
        )

        finish_button = arcade.gui.UIFlatButton(text="finish", width=200, style={'font_name': FONT})
        v_box.add(finish_button.with_space_around(bottom=10))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                align_x=10.0,
                anchor_y="top",
                align_y=-10.0,
                child=v_box)
        )

        @finish_button.event("on_click")
        def on_click_finish(event):
            print("Finish:", event)
            self.cube_list.clear()
            arcade.unschedule(self.extra_cube)
            arcade.get_window().game_server_factory.q.put(Worker(WorkerAction.game_finish))
            arcade.get_window().set_state(app.ArcadeState.result)

        arcade.set_background_color(arcade.color.SPACE_CADET)
        arcade.set_viewport(0, arcade.get_window().width, 0, arcade.get_window().height)

    def on_show_view(self):
        self.setup()
        arcade.schedule(self.extra_cube, self.settings.auto_spawn_time)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.cube_list.draw()
        self.pillar_1.draw()
        self.pillar_2.draw()
        self.manager.draw()
        arcade.draw_text("In Game", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center",
                         font_name=FONT)
        player_text = ', '.join(
            [f'Player {i.uid:02d}: {i.score} ({i.username}-{i.status})({i.battery}/{i.controller}/{i.glass})' for i in self.window.game_server_factory.player_manager.get_players().values()])
        arcade.draw_text(player_text, self.window.width / 2, self.window.height / 2-150,
                         arcade.color.ORANGE, font_size=24, anchor_x="center",
                         font_name=FONT_THIN)

    def on_update(self, delta_time: float):
        self.cube_list.update()
        self.number_of_cubes_ui.text = f'Number of Cubes: {len(self.cube_list):03d}'
        self.cube_index_ui.text = f'Cube index: {self.cube_index:03d}'

    def extra_cube(self, delta_time: float) -> None:
        if len(self.cube_list) <= self.settings.max_spawn_count - self.settings.auto_spawn_count:
            cl = self.create_cube(self.settings.auto_spawn_count*self.settings.number_of_players, 1)
            arcade.get_window().game_server_factory.q.put(Worker(WorkerAction.cube_create, cl))
            self.cube_list.extend(cl)
            self.__logger.info(f'added {self.settings.auto_spawn_count*self.settings.number_of_players} cube')
        else:
            self.__logger.info(f'can\'t add cube(max: {self.settings.max_spawn_count})')

    def create_cube(self, count, _type) -> List:
        cl = list()
        for i in range(count):
            c = cube.Cube(self.cube_index, _type, cube_size)
            sz = self.get_spawn_zone(3)
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
