# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from .utils import convert_bytes_to_hexstring


class _Byteable(metaclass=ABCMeta):
    DEFAULT_HEADER = None
    BYTES_LENGTH = 0
    LISTABLE = False

    def __init__(self):
        self.__bytes: bytes = bytes()

    @staticmethod
    @abstractmethod
    def from_bytes(source):
        return _Byteable()

    @abstractmethod
    def to_bytes(self):
        return bytes()


class ParsingException(Exception):
    def __init__(self, source):
        super().__init__("Parsing Exception: \n" + convert_bytes_to_hexstring(source))


class EmptyException(Exception):
    pass
