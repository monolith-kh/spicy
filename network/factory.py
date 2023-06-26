# -*- coding: utf-8 -*-

from enum import Enum, auto
from typing import Dict, List, Optional
import queue

from twisted.internet import protocol
from twisted.logger import Logger

from .protocol import GameProtocol
from .builder import FlatbuffersBuilder

from model import player


class WorkerAction(Enum):
    ping_all = auto()
    game_start = auto()
    game_finish = auto()
    cube_create = auto()
    test = auto()


class Worker:
    def __init__(self, action: WorkerAction, data: Optional[List] = None):
        self.action = action
        self.data = data


class GameServerFactory(protocol.ServerFactory):
    __logger = Logger(__name__)

    Q_MAX_SIZE = 65536

    def __init__(self):
        self.player_manager = player.PlayerManager()
        self.fb_builder = FlatbuffersBuilder()
        self.q = queue.Queue(self.Q_MAX_SIZE)

    def buildProtocol(self, addr):
        self.__logger.info(str(addr))
        return GameProtocol(self.player_manager)

    def worker(self):
        if not self.q.empty():
            w: Worker = self.q.get()
            self.__logger.info(str(w.action))
            if w.action == WorkerAction.ping_all:
                fb_data = self.fb_builder.send_ping()
                for p in self.player_manager.get_players().values():
                    p.protocol.write(fb_data)
            elif w.action == WorkerAction.game_start:
                fb_data = self.fb_builder.game_start()
                for p in self.player_manager.get_players().values():
                    p.status = player.PlayerStatus.game
                    p.protocol.write(fb_data)
            elif w.action == WorkerAction.game_finish:
                fb_data = self.fb_builder.game_finish()
                for p in self.player_manager.get_players().values():
                    p.status = player.PlayerStatus.idle
                    p.protocol.write(fb_data)
            elif w.action == WorkerAction.cube_create:
                fb_data = self.fb_builder.send_cube_create(w.data)
                for p in self.player_manager.get_players().values():
                    p.protocol.write(fb_data)
            else:
                self.__logger.warn('invalid action on worker')
        else:
            pass

    def cbWorkerDone(self, result):
        self.__logger.info(result)

    def ebWorkerFailed(self, failure):
        self.__logger.info(failure.getBriefTraceback())
