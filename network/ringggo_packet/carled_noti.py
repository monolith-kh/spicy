# -*- coding: utf-8 -*-
import struct
from dataclasses import dataclass

from .header import Header
from .body import Body


@dataclass(frozen=True)
class __CarLedNoti:
    led_idx: int
    action_type: int
    led_time: int
    color_r: int
    color_g: int
    color_b: int


class CarLedNoti(__CarLedNoti, Body):
    DEFAULT_HEADER = Header.PK_CARLED_NOTI
    BYTES_LENGTH = 7

    LED_OFF = 0
    LED_STATIC = 1
    LED_BLINK = 2
    LED_RANDOM = 0xFF

    COLOR_RINGGGO = 0x00AC30
    COLOR_WHITE = 0x808080
    COLOR_YELLOW = 0xFFFF00
    COLOR_RED = 0xFF0000
    COLOR_DARKRED = 0x8B0000
    COLOR_LIME = 0x00FF00
    COLOR_GREEN = 0x008000
    COLOR_BLUE = 0x0000FF
    COLOR_AQUA = 0x00FFFF

    __STRUCT = struct.Struct('<BBHBBB')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.led_idx,
                self.action_type,
                self.led_time,
                self.color_r,
                self.color_g,
                self.color_b,
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        if len(source) == 0:
            return bytes()

        (
            led_idx,
            action_type,
            led_time,
            color_r,
            color_g,
            color_b,
        ) = CarLedNoti.__STRUCT.unpack(source)

        result = CarLedNoti(
            led_idx=led_idx,
            action_type=action_type,
            led_time=led_time,
            color_r=color_r,
            color_g=color_g,
            color_b=color_b,
        )
        result.__bytes = source

        return result
