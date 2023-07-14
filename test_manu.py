# -*- coding: utf-8 -*-

from enum import Enum, auto
from datetime import datetime

import time
import sys
import signal
import threading
import queue

from abc import ABC

import click

from twisted.internet import reactor, protocol, endpoints, task
from twisted.logger import Logger, globalLogPublisher, FilteringLogObserver, LogLevel, LogLevelFilterPredicate, textFileLogObserver

from flatbuffers import Builder

import arcade
import arcade.gui

from fbs import Frame, Command, Sender, Response, Player, Sender, PlayerList, Cube, CubeList

from model import player
from model import cube

from network.base import SizedPacketProtocol
from network.builder import FlatbuffersBuilder
from network.protocol import RingggoClientProtocol
from network.factory import RingggoClientFactory

from game import FONT, FONT_THIN

ARENA_WIDTH = 1900
ARENA_HEIGHT = 1380

SCREEN_SCALING = 0.5
# SCREEN_SCALING = 1.0
SCREEN_WIDTH = ARENA_WIDTH * SCREEN_SCALING
SCREEN_HEIGHT = ARENA_HEIGHT * SCREEN_SCALING
SCREEN_TITLE = 'Cube client'


class RingggoProtocol(protocol.Protocol):
    __logger = Logger(__name__)

    def connectionMade(self):
        self.__logger.info('New Connection')

    def connectionLost(self, reason):
        self.__logger.info('Lost Connection: (reason: {})'.format(reason.getErrorMessage()))

    def dataReceived(self, data):
        print(data)


class RingggoFactory(protocol.ClientFactory):
    __logger = Logger(__name__)

    def __init__(self):
        self.protocol = None

    def buildProtocol(self, addr):
        self.__logger.info('addr: {}'.format(addr))
        self.protocol = RingggoProtocol() 
        return self.protocol


class WorkerAction(Enum):
    ping = auto()
    player_get = auto()
    game_ready = auto()
    player_list = auto()
    test = auto()


class GameClientFactory(protocol.ClientFactory):
    __logger = Logger(__name__)

    def __init__(self, uid):
        self.uid = uid
        self.protocol = None
        self.__logger.info('uid: {}'.format(uid))
        self.fb_builder = FlatbuffersBuilder()
        self.q = queue.Queue()

    def buildProtocol(self, addr):
        self.__logger.info('addr: {}, uid: {}'.format(addr, self.uid))
        self.protocol = GameClientProtocol(self.uid) 
        return self.protocol

    def worker(self):
        if not self.q.empty():
            action = self.q.get()
            self.__logger.info(str(action))
            if action == WorkerAction.ping:
                fb_data = self.fb_builder.send_ping()
                self.protocol.write(fb_data)
            elif action == WorkerAction.player_get:
                fb_data = self.fb_builder.get_player()
                self.protocol.write(fb_data)
            elif action == WorkerAction.game_ready:
                fb_data = self.fb_builder.game_ready()
                self.protocol.write(fb_data)
            elif action == WorkerAction.player_list:
                fb_data = self.fb_builder.get_player_list()
                self.protocol.write(fb_data)
            else:
                self.__logger.warn('invalid action on worker')
        else:
            pass

    def cbWorkerDone(self, result):
        self.__logger.info(result)

    def ebWorkerFailed(cls, failure):
        self.__logger.info(failure.getBriefTraceback())


class ArcadeWindow(arcade.Window):
    __logger = Logger(__name__)

    def __init__(self, game_client_factory: GameClientFactory):
        super().__init__(int(SCREEN_WIDTH), int(SCREEN_HEIGHT), SCREEN_TITLE)
        self.game_client_factory = game_client_factory
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.v_box = arcade.gui.UIBoxLayout()

        player_text = f'Player: #{self.game_client_factory.protocol.player.uid:02d}-{self.game_client_factory.protocol.player.username} ({self.game_client_factory.protocol.player.status})'
        self.player_text_label = arcade.gui.UITextArea(text=player_text,
                                              width=450,
                                              height=100,
                                              font_size=30,
                                              font_name="Kenney Future")
        self.v_box.add(self.player_text_label.with_space_around(bottom=20))
        
        # Create the buttons
        ready_button = arcade.gui.UIFlatButton(text="Ready", width=200, style={'font_name': FONT})
        self.v_box.add(ready_button.with_space_around(bottom=20))

        @ready_button.event("on_click")
        def on_click_ready(event):
            print("Ready:", event)
            self.game_client_factory.protocol.player.status = player.PlayerStatus.ready
            self.game_client_factory.q.put(WorkerAction.game_ready)
            
        # Create the buttons
        player_button = arcade.gui.UIFlatButton(text="Player", width=200, style={'font_name': FONT})
        self.v_box.add(player_button.with_space_around(bottom=20))

        @player_button.event("on_click")
        def on_click_player(event):
            print("player:", event)
            self.game_client_factory.q.put(WorkerAction.player_get)
            
        # Create the buttons
        player_list_button = arcade.gui.UIFlatButton(text="Player List", width=200, style={'font_name': FONT})
        self.v_box.add(player_list_button.with_space_around(bottom=20))

        @player_list_button.event("on_click")
        def on_click_player_list(event):
            print("player_list:", event)
            self.game_client_factory.q.put(WorkerAction.player_list)
            
        # Create the buttons
        ping_button = arcade.gui.UIFlatButton(text="Ping", width=200, style={'font_name': FONT})
        self.v_box.add(ping_button.with_space_around(bottom=20))

        @ping_button.event("on_click")
        def on_click_ping(event):
            print("ping:", event)
            self.game_client_factory.q.put(WorkerAction.ping)
            
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def setup(self):
        ''' Set up the game and initialize the variables. '''
        ...

    def on_draw(self):
        ''' Draw everything '''
        self.clear()
        self.player_text_label.text = f'Player: #{self.game_client_factory.protocol.player.uid:02d}-{self.game_client_factory.protocol.player.username} ({self.game_client_factory.protocol.player.status})'
        self.manager.draw()

    def on_update(self, delta_time):
        ''' Movement and game logic '''
        # self.player_text_label.text = f'Player: #{self.game_client_factory.protocol.player.uid:02d}-{self.game_client_factory.protocol.player.username} ({self.game_client_factory.protocol.player.status})'
        ...

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        return super().on_mouse_press(x, y, button, modifiers)


@click.command()
@click.option('--host', default='192.168.40.254', type=click.STRING, required=True, help='set ringggo server host(default: 192.168.40.254)')
@click.option('--port', default=9996, type=click.INT, required=True, help='set server port(default: 9996)')
def main(host, port):
    predicate = LogLevelFilterPredicate(defaultLogLevel=LogLevel.debug)
    observer = FilteringLogObserver(textFileLogObserver(outFile=sys.stdout), [predicate])
    observer._encoding = 'utf-8'
    globalLogPublisher.addObserver(observer)

    logger = Logger('MainThread')
    logger.info('let\'s go aespa')
    logger.info('Who\'s next Karina?')

    tcp_client_endpoint = endpoints.TCP4ClientEndpoint(reactor, host, port)
    ringggo_client_factory = RingggoFactory()
    tcp_client_endpoint.connect(ringggo_client_factory)

    # worker = task.LoopingCall(game_client_factory.worker)
    # worker_deferred = worker.start(0.1, False)
    # worker_deferred.addCallback(game_client_factory.cbWorkerDone)
    # worker_deferred.addErrback(game_client_factory.ebWorkerFailed)

    def shutdown_handler(_=None, __=None):
        # arcade.exit()
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    threading.Thread(target=reactor.run, args=(False,)).start()

    # arcade_window = ArcadeWindow(ringggo_client_factory)
    # arcade_window.setup()
    # arcade.run()


if __name__ == '__main__':
    main()
