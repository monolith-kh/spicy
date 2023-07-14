# -*- coding: utf-8 -*-

from .body import Body


class Blank(Body):
    DEFAULT_HEADER = None
    BYTES_LENGTH = 0
    LISTABLE = False

    @staticmethod
    def from_bytes(_):
        return Blank()

    def to_bytes(self):
        return bytes()

