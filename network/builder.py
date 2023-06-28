# -*- coding: utf-8 -*-

import time
import random

from typing import Dict, TYPE_CHECKING, List

from twisted.logger import Logger

from flatbuffers import Builder

from fbs import Frame, Command, Sender, Response, Player, PlayerList, Cube, CubeList, CubeType, Vec3

from model import player

if TYPE_CHECKING:
    from game import cube


class FlatbuffersBuilder:
    __logger = Logger(__name__)

    def send_welcome(self):
        builder = Builder(0)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.welcome)
        Frame.AddData(builder, 0)
        return self._finishing(builder)

    def response_welcome(self, p: player.Player):
        builder = Builder(0)

        data = self._get_player(builder, p)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.welcome)
        Frame.AddData(builder, data)

        return self._finishing(builder)

    def send_ping(self):
        builder = Builder(0)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.ping)
        Frame.AddData(builder, 0)
        return self._finishing(builder)

    def game_start(self):
        builder = Builder(0)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.game_start)
        Frame.AddData(builder, 0)
        return self._finishing(builder)

    def game_finish(self):
        builder = Builder(0)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.game_finish)
        Frame.AddData(builder, 0)
        return self._finishing(builder)

    def response_ping(self):
        builder = Builder(0)

        detail = builder.CreateString('pong')
        Response.Start(builder)
        Response.AddRequestedCommand(builder, Command.Command.ping)
        Response.AddErrorCode(builder, 0)
        Response.AddDetail(builder, detail)
        data = Response.End(builder)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.response)
        Frame.AddData(builder, data)
        return self._finishing(builder)

    def get_player(self):
        builder = Builder(0)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.player_get)
        Frame.AddData(builder, 0)
        return self._finishing(builder)

    def get_player_list(self):
        builder = Builder(0)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.player_status)
        Frame.AddData(builder, 0)
        return self._finishing(builder)

    def game_ready(self):
        builder = Builder(0)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.game_ready)
        Frame.AddData(builder, 0)
        return self._finishing(builder)

    def response_player(self, p: player.Player):
        builder = Builder(0)

        data = self._get_player(builder, p)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.player_get)
        Frame.AddData(builder, data)

        return self._finishing(builder)

    def _get_player(self, builder, p: player.Player):
        username = builder.CreateString(p.username)
        image_url = builder.CreateString(p.image_url)

        Player.Start(builder)
        Player.AddUid(builder, p.uid)
        Player.AddUsername(builder, username)
        Player.AddImageUrl(builder, image_url)
        Player.AddScore(builder, p.score)
        Player.AddStatus(builder, p.status)

        return Player.End(builder)

    def response_player_status(self, ps: Dict[int, player.Player]):
        builder = Builder(0)

        data = self._get_player_status(builder, ps)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.player_status)
        Frame.AddData(builder, data)

        return self._finishing(builder)

    def _get_player_status(self, builder, ps: Dict[int, player.Player]):
        p_list = [self._get_player(builder, p) for p in ps.values()]
        PlayerList.StartPlayersVector(builder, len(p_list))
        for p in p_list:
            builder.PrependUOffsetTRelative(p)
        vector_pos = builder.EndVector()

        PlayerList.Start(builder)
        PlayerList.PlayerListAddPlayers(builder, vector_pos)

        return PlayerList.End(builder)

    def send_cube_create(self, cs: List['cube.Cube']):
        builder = Builder(0)

        data = self._get_cube_status(builder, cs)

        self._append_frame_header(builder)
        Frame.AddCommand(builder, Command.Command.cube_create)
        Frame.AddData(builder, data)

        return self._finishing(builder)

    def _get_cube(self, builder, c: 'cube.Cube'):
        Cube.Start(builder)
        Cube.AddUid(builder, c.uid)
        # transform to unity axis (x, z, y)
        # transform cetimeter to meter
        pos_cur = Vec3.CreateVec3(builder, c.center_x/100., 0., c.center_y/100.)
        Cube.AddPosCur(builder, pos_cur)
        pos_target = Vec3.CreateVec3(builder, (c.center_x+c.change_x)/100., 0., (c.center_y+c.change_y)/100.)
        Cube.AddPosTarget(builder, pos_target)
        Cube.AddSpeed(builder, 1)
        Cube.AddType(builder, c._type)

        return Cube.End(builder)

    def _get_cube_status(self, builder, cs: List['cube.Cube']):
        c_list = [self._get_cube(builder, c) for c in cs]
        CubeList.StartCubesVector(builder, len(c_list))
        for c in c_list:
            builder.PrependUOffsetTRelative(c)
        vector_pos = builder.EndVector()

        CubeList.Start(builder)
        CubeList.CubeListAddCubes(builder, vector_pos)

        return CubeList.End(builder)

    def _append_frame_header(self, builder):
        timestamp = int(time.time() * 1000)

        Frame.Start(builder)
        Frame.AddTimestamp(builder, timestamp)
        Frame.AddSender(builder, Sender.Sender.server)

    def _finishing(self, builder):
        request_pos = Frame.End(builder)
        builder.Finish(request_pos)
        return builder.Output()
