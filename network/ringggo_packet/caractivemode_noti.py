# -*- coding: utf-8 -*-

import struct
from dataclasses import dataclass

from .header import Header
from .body import Body


@dataclass(frozen=True)
class __CarActiveModeNoti:
    signal: int


class CarActiveModeNoti(__CarActiveModeNoti, Body):
    DEFAULT_HEADER = Header.PK_CARACTIVEMODE_NOTI
    BYTES_LENGTH = 1

    SIGNAL_STOP = 0
    SIGNAL_START = 1
    SIGNAL_SUSPEND = 2
    SIGNAL_RESUME = 3
    SIGNAL_REMOTE_ON = 4
    SIGNAL_REMOTE_OFF = 5

    __STRUCT = struct.Struct('<B')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.signal
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        if len(source) == 0:
            return bytes()

        (
            signal,
        ) = CarActiveModeNoti.__STRUCT.unpack(source)

        result = CarActiveModeNoti(
            signal=signal
        )
        result.__bytes = source

        return result
