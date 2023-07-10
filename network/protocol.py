# -*- coding: utf-8 -*-

import time
from abc import ABC

import arcade

from twisted.internet.protocol import DatagramProtocol
from twisted.logger import Logger

from flatbuffers import Builder

from fbs import Frame, Command, Sender, Response, Player, Cube

from .base import SizedPacketProtocol
from .builder import FlatbuffersBuilder

from model import player


class GameProtocol(ABC, SizedPacketProtocol):
    __logger = Logger(__name__)

    def __init__(self, player_manager: player.PlayerManager, cube_list: arcade.SpriteList):
        super().__init__()
        self.uid = -1
        self.fb_builder = FlatbuffersBuilder()
        self.player_manager = player_manager
        self.cube_list = cube_list

    def connectionMade(self):
        self.__logger.info('New Connection')
        fb_data = self.fb_builder.send_welcome()
        self.write(fb_data)

    def connectionLost(self, reason):
        self.__logger.info('Lost Connection: (reason: {})'.format(reason.getErrorMessage()))
        self.player_manager.remove_player(self.uid)
        print(self.player_manager.get_players())

    def packetReceived(self, data: bytes):
        self.__logger.debug('received packet raw data: {}'.format(str(data)))
        received_frame = Frame.Frame.GetRootAsFrame(data, 0)

        data = received_frame.Data()
        if received_frame.Command() == Command.Command.response:
            response = Response.Response()
            response.Init(data.Bytes, data.Pos)
            self.__logger.debug('<- Response: Command: {}'.format(response.RequestedCommand()))
            self.__logger.debug('<- Response: ErrorCode: {}'.format(response.ErrorCode()))
            self.__logger.debug('<- Response: Detail: {}'.format(response.Detail()))
            if response.RequestedCommand() == Command.Command.ping:
                self.__logger.info(f'respone ping ok (uid:{self.uid})')
            else:
                self.__logger.warn(('invalid requested command'))
        elif received_frame.Command() == Command.Command.welcome:
            fbs_player = Player.Player()
            fbs_player.Init(data.Bytes, data.Pos)
            p = player.Player(
                fbs_player.Uid(),
                fbs_player.Username(),
                fbs_player.ImageUrl(),
                fbs_player.Score(),
                fbs_player.Status(),
                fbs_player.Battery(),
                fbs_player.Controller(),
                fbs_player.Glass(),
                self
            )
            self.__logger.info(str(p))
            self.uid = p.uid
            self.player_manager.add_player(p)
            self.__logger.info(str(self.player_manager))
            self.__logger.info(str(self.player_manager.get_players()))
        elif received_frame.Command() == Command.Command.ping:
            self.__logger.info('received ping command')

            fbs_player = Player.Player()
            fbs_player.Init(data.Bytes, data.Pos)
            p = player.Player(
                fbs_player.Uid(),
                fbs_player.Username(),
                fbs_player.ImageUrl(),
                fbs_player.Score(),
                fbs_player.Status(),
                fbs_player.Battery(),
                fbs_player.Controller(),
                fbs_player.Glass(),
                self
            )
            self.__logger.info(str(p))
            self.player_manager.add_player(p)

            fb_data = self.fb_builder.response_ping()
            self.write(fb_data)
        elif received_frame.Command() == Command.Command.game_ready:
            p = self.player_manager.get_player(self.uid)
            p.status = player.PlayerStatus.ready
        elif received_frame.Command() == Command.Command.game_start:
            ...
            # TODO:
        elif received_frame.Command() == Command.Command.game_finish:
            ...
            # TODO:
        elif received_frame.Command() == Command.Command.player_get:
            self.__logger.info('received player get command')
            p = self.player_manager.get_player(self.uid)
            fb_data = self.fb_builder.response_player(p)
            self.write(fb_data)
        elif received_frame.Command() == Command.Command.player_status:
            self.__logger.info('received player status command')
            ps = self.player_manager.get_players()
            fb_data = self.fb_builder.response_player_status(ps)
            self.write(fb_data)
        elif received_frame.Command() == Command.Command.player_checkin:
            ...
            # TODO:
        elif received_frame.Command() == Command.Command.cube_create:
            ...
            # TODO:
        elif received_frame.Command() == Command.Command.cube_remove:
            self.__logger.info('received cube remove command')
            fbs_cube = Cube.Cube()
            fbs_cube.Init(data.Bytes, data.Pos)
            for c in self.cube_list:
                if c.uid == fbs_cube.Uid():
                    c.remove_from_sprite_lists()
            self.__logger.info(f'removed {str(fbs_cube.Uid())} cube')
        elif received_frame.Command() == Command.Command.cube_status:
            ...
            # TODO:
        else:
            ...
            # TODO:


class RingggoClientProtocol(ABC, SizedPacketProtocol):
    __logger = Logger(__name__)

    def __init__(self):
        super().__init__()

    def connectionMade(self):
        self.__logger.info('New Connection')

    def connectionLost(self, reason):
        self.__logger.info('Lost Connection: (reason: {})'.format(reason.getErrorMessage()))

    def packetReceived(self, data: bytes):
        self.__logger.debug('received packet raw data: {}'.format(str(data)))
        # TODO:
        ...
