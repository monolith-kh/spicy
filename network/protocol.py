# -*- coding: utf-8 -*-

import time
from abc import ABC

from twisted.internet.protocol import DatagramProtocol
from twisted.logger import Logger

from flatbuffers import Builder

from fbs import Frame, Command, Sender, Response, Player

from .base import SizedPacketProtocol
from .builder import FlatbuffersBuilder

from model import player

from .ringggo_packet import Header, PositionObject, PositionNoti, Packet


class GameProtocol(ABC, SizedPacketProtocol):
    __logger = Logger(__name__)

    def __init__(self, player_manager: player.PlayerManager):
        super().__init__()
        self.uid = -1
        self.fb_builder = FlatbuffersBuilder()
        self.player_manager = player_manager

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
                self
            )
            self.__logger.info(str(p))
            self.uid = p.uid
            self.player_manager.add_player(p)
            self.__logger.info(str(self.player_manager))
            self.__logger.info(str(self.player_manager.get_players()))
        elif received_frame.Command() == Command.Command.ping:
            self.__logger.info('received ping command')
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
            ...
            # TODO:
        elif received_frame.Command() == Command.Command.cube_status:
            ...
            # TODO:
        else:
            ...
            # TODO:


class RtlsProtocol(DatagramProtocol):
    __logger = Logger(__name__)

    def __init__(self):
        self.host = '192.168.40.254'
        self.port = 9999

    def startProtocol(self):
        self.__logger.info('New connection')
        self.transport.connect(self.host, self.port)

        packet = Packet(
            sender=Header.SENDER_ADMIN,
            code=Header.PK_POSITION_RELAY)
        self.transport.write(packet.to_bytes())

    def stopProtocol(self):
        self.__logger.info('Disconnected')

    def datagramReceived(self, data, addr):
        # self.__logger.debug('received {} from {}'.format(data, addr))
        p = Packet.from_bytes(data)
        self.__logger.debug('header code: {}'.format(p.header.code))
        for c in p.body:
            # RtlsService().cars[c.object_number] = dict(
            #     x=c.position_noti.position_x,
            #     y=c.position_noti.position_y
            # )
            self.__logger.debug('{}, {}, {}'.format(c.object_number, c.position_noti.position_x, c.position_noti.position_y))
        # self.log.debug('car list: {cars}'.format(cars=RtlsService().cars))
        # packet = Packet(
        #     sender=Header.SENDER_ADMIN,
        #     code=Header.PK_POSITION_LISTEN_STOP)
        # self.transport.write(packet.to_bytes())

    def connectionRefused(self):
        self.__logger.info('No one listening')