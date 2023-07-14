# -*- coding: utf-8 -*-

import struct
from dataclasses import dataclass

from .header import Header
from .body import Body


@dataclass(frozen=True)
class __GameEventNoti:
    event: int


class GameEventNoti(__GameEventNoti, Body):
    DEFAULT_HEADER = Header.PK_GAME_EVENT_NOTI
    BYTES_LENGTH = 1

    EVENT_STOP = 0
    EVENT_START = 1
    EVENT_PAUSE = 2
    EVENT_UNPAUSE = 3
    EVENT_NEXTSTEP = 4

    __STRUCT = struct.Struct('<B')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.event
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        if len(source) == 0:
            return bytes()

        (
            event,
        ) = GameEventNoti.__STRUCT.unpack(source)

        result = GameEventNoti(
            event=event
        )
        result.__bytes = source

        return result
