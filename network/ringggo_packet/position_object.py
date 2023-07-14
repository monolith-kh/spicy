# -*- coding: utf-8 -*-

import struct
from dataclasses import dataclass

from .header import Header
from .position_noti import PositionNoti
from .body import Body


@dataclass(frozen=True)
class __PositionObject:
    object_number: int
    position_noti: PositionNoti


class PositionObject(__PositionObject, Body):
    DEFAULT_HEADER = Header.PK_POSITION_OBJECTS
    LISTABLE = True
    BYTES_LENGTH = 20

    __STRUCT = struct.Struct('<H18s')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.object_number,
                self.position_noti.to_bytes()
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        (
            object_number,
            position_noti_bytes
        ) = PositionObject.__STRUCT.unpack(source)

        result = PositionObject(
            object_number=object_number,
            position_noti=PositionNoti.from_bytes(position_noti_bytes)
        )
        result.__bytes = source

        return result
