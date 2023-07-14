# -*- coding: utf-8 -*-
import struct
from dataclasses import dataclass

from .header import Header
from .body import Body


@dataclass(frozen=True)
class __CarSoundNoti:
    cmd: int
    value: int


class CarSoundNoti(__CarSoundNoti, Body):
    DEFAULT_HEADER = Header.PK_CARSOUND_NOTI
    BYTES_LENGTH = 2

    COMMAND_STOP = 0
    COMMAND_PLAY = 1
    COMMAND_EFFECT = 2
    COMMAND_VOLUME = 3

    BG_START = 0
    BG_STOP_1 = 2
    BG_STOP_2 = 18
    BG_STOP = BG_STOP_1

    EFFECT_DING_DONG = 6
    EFFECT_NFC_READED = 9
    EFFECT_NFC_CHECKING = 10
    EFFECT_NFC_CHECKIN_SUCCESS = 11
    EFFECT_NFC_CHECKIN_FAIL = 12
    EFFECT_NFC_READ_ERROR = 13
    EFFECT_COUNTDOWN_2 = 14
    EFFECT_BUMP_ATTACK = 15
    EFFECT_BUMP_CRASHED_SIZE = 16
    EFFECT_BUMP_CRASHED_BEHINE = 17
    EFFECT_APPLAUSE = 19
    
    __STRUCT = struct.Struct('<BB')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.cmd,
                self.value
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        if len(source) == 0:
            return bytes()

        (
            cmd,
            value
        ) = CarSoundNoti.__STRUCT.unpack(source)

        result = CarSoundNoti(
            cmd=cmd,
            value=value
        )
        result.__bytes = source

        return result
