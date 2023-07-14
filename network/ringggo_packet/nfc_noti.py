# -*- coding: utf-8 -*-

import struct
from dataclasses import dataclass

from .header import Header
from .body import Body


@dataclass(frozen=True)
class __NfcNoti:
    wear_id: str
    uid: bytes


class NfcNoti(__NfcNoti, Body):
    DEFAULT_HEADER = Header.PK_NFC_NOTI
    BYTES_LENGTH = 21

    __STRUCT = struct.Struct('<13sc7s')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.wear_id.encode("ASCII"),
                ','.encode("ASCII"),
                self.uid
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        if len(source) == 0:
            return bytes()

        (
            wear_id,
            splitter,
            uid
        ) = NfcNoti.__STRUCT.unpack(source)

        try:
            result = NfcNoti(
                wear_id=wear_id.decode('ASCII'),
                uid=uid
            )
            result.__bytes = source

            return result
        except UnicodeDecodeError as e:
            raise NfcNoti.NfcWrongWearableIdException(str(e))

    class NfcWrongWearableIdException(Exception):
        pass
