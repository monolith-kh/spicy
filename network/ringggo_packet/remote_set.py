# -*- coding: utf-8 -*-

import struct
from dataclasses import dataclass

from . import Header
from .body import Body


@dataclass(frozen=True)
class __RemoteSet:
    right_rpm: int
    left_rpm: int


class RemoteSet(__RemoteSet, Body):
    DEFAULT_HEADER = Header.PK_REMOTE_SET
    BYTES_LENGTH = 4

    __STRUCT = struct.Struct('<hh')

    __bytes: bytes = bytes()

    def to_bytes(self):
        if len(self.__bytes) == 0:
            self.__bytes = self.__STRUCT.pack(
                self.right_rpm,
                self.left_rpm,
            )

        return self.__bytes

    @staticmethod
    def from_bytes(source):
        (
            right_rpm,
            left_rpm,
        ) = RemoteSet.__STRUCT.unpack(source)

        result = RemoteSet(
            right_rpm=right_rpm,
            left_rpm=left_rpm,
        )
        result.__bytes = source

        return result
