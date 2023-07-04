# -*- coding: utf-8 -*-

from enum import Enum, auto
import dataclasses
import os.path

import yaml

import arcade

from twisted.internet import reactor
from twisted.logger import Logger

from game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SPLASH_TIME, PING_ALL_TIME

from network.factory import GameServerFactory, WorkerAction, Worker

from .views.idle import IdleView
from .views.menu import MenuView
from .views.ready import ReadyView
from .views.game import GameView
from .views.result import ResultView
from .views.pause import PauseView
from .views.settings import SettingsView


class ArcadeState(Enum):
    idle = auto()
    menu = auto()
    ready = auto()
    game = auto()
    result = auto()
    pause = auto()
    settings = auto()


@dataclasses.dataclass
class Settings:
    __logger = Logger(__name__)

    number_of_players: int = 4
    basic_spawn_count: int = 20
    auto_spawn_count: int = 3
    auto_spawn_time: float = 3.0
    max_spawn_count: int = 140

    def to_json(self):
        return dataclasses.asdict(self)

    __filename = './config.yaml'

    def load_file(self):
        if os.path.isfile(self.__filename):
            with open(self.__filename, 'r') as f:
                conf = yaml.safe_load(f)
                self.number_of_players = conf['number_of_players']
                self.basic_spawn_count = conf['basic_spawn_count']
                self.auto_spawn_count = conf['auto_spawn_count']
                self.auto_spawn_time = conf['auto_spawn_time']
                self.max_spawn_count = conf['max_spawn_count']
                self.__logger.info('config file loaded')
        else:
            self.__logger.warn('no config file')
    
    def save(self, conf: dict):
        self.number_of_players = conf['number_of_players']
        self.basic_spawn_count = conf['basic_spawn_count']
        self.auto_spawn_count = conf['auto_spawn_count']
        self.auto_spawn_time = conf['auto_spawn_time']
        self.max_spawn_count = conf['max_spawn_count']

    def save_file(self):
        with open(self.__filename, 'w') as f:
            yaml.dump(self.to_json(), f)
            self.__logger.info('config file saved')


class ArcadeWindow(arcade.Window):

    __logger = Logger(__name__)

    def __init__(self, game_server_factory: GameServerFactory):
        super().__init__(int(SCREEN_WIDTH), int(SCREEN_HEIGHT), SCREEN_TITLE)
        self.game_server_factory: GameServerFactory = game_server_factory
        self.state = None

        self.settings = Settings()
        self.settings.load_file()

        self.__logger.debug(str(self.game_server_factory))
        arcade.set_background_color(arcade.color.SPACE_CADET)

    def setup(self):
        ''' Set up the game and initialize the variables. '''
        self.set_state(ArcadeState.idle)

        arcade.schedule(self.move_menu, SPLASH_TIME)
        arcade.schedule(self.send_ping_all, PING_ALL_TIME)
    
    def close(self):
        super().close()
        arcade.exit()
        reactor.callFromThread(reactor.stop)

    def move_menu(self, delta_time: float):
        self.set_state(ArcadeState.menu)
        arcade.unschedule(self.move_menu)

    def set_state(self, state: ArcadeState):
        self.state = state
        if state == ArcadeState.idle:
            self.show_view(IdleView())
        elif state == ArcadeState.menu:
            self.show_view(MenuView())
        elif state == ArcadeState.ready:
            self.show_view(ReadyView())
        elif state == ArcadeState.game:
            self.show_view(GameView())
        elif state == ArcadeState.result:
            self.show_view(ResultView())
        elif state == ArcadeState.pause:
            self.show_view(PauseView())
        elif state == ArcadeState.settings:
            self.show_view(SettingsView())
        self.__logger.info(str(self.state))

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        return super().on_mouse_press(x, y, button, modifiers)
    
    def send_ping_all(self, delta_time: float):
        self.__logger.info('ping test')
        self.game_server_factory.q.put(Worker(WorkerAction.ping_all))
        self.__logger.info(str(self.game_server_factory.q.queue))


def start_arcade(game_server_factory: GameServerFactory):
    window = ArcadeWindow(game_server_factory)
    window.setup()
    arcade.run()


def exit_arcade():
    arcade.exit()
