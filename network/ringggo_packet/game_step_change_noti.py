# -*- coding: utf-8 -*-

import struct
from dataclasses import dataclass

from .header import Header
from .body import Body


@dataclass(frozen=True)
class __GameStepChangeNoti:
    step: str


class GameStepChangeNoti(__GameStepChangeNoti, Body):
    DEFAULT_HEADER = Header.PK_GAME_STEP_CHANGE_NOTI
    BYTES_LENGTH = 24

    __STRUCT = struct.Struct('<24s')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.step.encode("UTF-8")
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        if len(source) == 0:
            return bytes()

        (
            step_bytes,
        ) = GameStepChangeNoti.__STRUCT.unpack(source)

        result = GameStepChangeNoti(
            step=step_bytes.decode("UTF-8").strip('\x00')
        )
        result.__bytes = source

        return result
