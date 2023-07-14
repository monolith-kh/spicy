# -*- coding: utf-8 -*-

import struct
from dataclasses import dataclass

from .header import Header
from .body import Body


@dataclass(frozen=True)
class __BatteryNoti:
    percentage: int


class BatteryNoti(__BatteryNoti, Body):
    DEFAULT_HEADER = Header.PK_BATTERY_NOTI
    BYTES_LENGTH = 1

    __STRUCT = struct.Struct('<b')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                    self.percentage
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        if len(source) == 0:
            return bytes()

        (
            percentage,
        ) = BatteryNoti.__STRUCT.unpack(source)
    
        result = BatteryNoti(
                percentage=percentage
        )
        result.__bytes = source

        return result

