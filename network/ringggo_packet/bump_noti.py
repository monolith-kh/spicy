# -*- coding: utf-8 -*-

import struct
from dataclasses import dataclass

from .header import Header
from .body import Body


@dataclass(frozen=True)
class __BumpNoti:
    bump_point: int


class BumpNoti(__BumpNoti, Body):
    DEFAULT_HEADER = Header.PK_BUMP_NOTI
    BYTES_LENGTH = 1

    BUMP_FRONT = 1
    BUMP_LEFT = 2
    BUMP_RIGHT = 4
    BUMP_BEHIND = 8

    __STRUCT = struct.Struct('<B')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.bump_point
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        if len(source) == 0:
            return bytes()

        (
            bump_point,
        ) = BumpNoti.__STRUCT.unpack(source)

        result = BumpNoti(
            bump_point=bump_point
        )
        result.__bytes = source

        return result
