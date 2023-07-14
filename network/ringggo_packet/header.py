# -*- coding: utf-8 -*-

import struct
from abc import ABC
from dataclasses import dataclass

from .utils import convert_bytes_to_hexstring

from ._byteable import _Byteable


@dataclass(frozen=True)
class __Header:
    code: int
    sender: int
    length: int
    car_number: int


class Header(__Header, _Byteable, ABC):
    BYTES_LENGTH = 8

    PK_WHO_ARE_YOU_ANS = 0x90
    PK_IAM_ANS = 0x92
    PK_GAME_EVENT_NOTI = 0xA1
    PK_GAME_STEP_CHANGE_NOTI = 0xA2
    PK_CHECKCONNECTION_REQ = 0xB1
    PK_CHECKCONNECTION_ANS = 0xB2
    PK_NFC_NOTI = 0xC1
    PK_BATTERY_NOTI = 0xC2
    PK_CARSPEED_NOTI = 0xC3
    PK_CARLED_NOTI = 0xC4
    PK_CARSOUND_NOTI = 0xC5
    PK_CARACTIVEMODE_NOTI = 0xC6
    PK_BUMP_NOTI = 0xC7
    PK_POSITION_NOTI = 0xD1
    PK_POSITION_REMOVE = 0xD2
    PK_POSITION_LISTEN = 0xD3
    PK_POSITION_LISTEN_STOP = 0xD4
    PK_POSITION_OBJECTS = 0xD5
    PK_POSITION_RELAY = 0xD6
    PK_POSITION_RELAY_STOP = 0xD7
    PK_REMOTE_SET = 0xE1

    SENDER_SERVER = 3
    SENDER_ADMIN = 4
    SENDER_CAR = 6
    SENDER_RTLS = 7

    __STRUCT = struct.Struct('<BBHHxx')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.code,
                self.sender,
                self.length,
                self.car_number)

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        try:
            (
                code,
                sender,
                length,
                car_number) = Header.__STRUCT.unpack(source)
            result = Header(
                code=code,
                sender=sender,
                length=length,
                car_number=car_number)
            result.__bytes = source
        except Exception as e:
            raise Header.WrongHeaderException(source) from e

        return result

    class WrongHeaderException(Exception):

        def __init__(self, header_bytes):
            super().__init__("Maybe Wrong Header: \n" + convert_bytes_to_hexstring(header_bytes))
