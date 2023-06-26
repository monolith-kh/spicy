# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, ABC
from twisted.internet.protocol import Protocol

from typing import Callable, List

from network import BUFFER_SIZE, SIZE_BYTES_LENGTH, ENDIAN


class BufferedSplitter:
    def __init__(self, buffer_size, get_packetsize_function: Callable[[bytearray], int]):
        self.__get_packetsize_function = get_packetsize_function
        self.__buffer = bytearray(buffer_size * 2)
        self.__remain_size = 0

    def append_data(self, data: bytearray):
        self.__buffer[self.__remain_size:self.__remain_size + len(data)]

        received_size = len(data)
        if received_size <= 0:
            raise EmptyDataException()

        self.__buffer[self.__remain_size:self.__remain_size + received_size] = data
        self.__remain_size += received_size

    def get_split_data(self)-> List[bytearray]:
        result = []
        while self.__remain_size > 0:
            packet_size = self.__get_packetsize_function(self.__buffer)
            if self.__remain_size >= packet_size:
                result.append(self.__buffer[0:packet_size])
                self.__remain_size -= packet_size
                self.__buffer[0:self.__remain_size] = self.__buffer[packet_size:packet_size + self.__remain_size]
            else:
                break

        return result


class EmptyDataException(Exception):
    pass


class BufferedAsyncReceiver:
    def __init__(self, buffer_size, 
                 get_packetsize_function: Callable[[bytearray], int],
                 received_function: Callable[[bytearray], None]):
        self.__buffered_splitter = BufferedSplitter(buffer_size, get_packetsize_function)
        self.__received_function = received_function

    def append_data(self, data: bytearray):
        self.__buffered_splitter.append_data(data)
        split_data = self.__buffered_splitter.get_split_data()

        for data in split_data:
            self.__received_function(data)


class SizedPacketProtocol(Protocol, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()

        def get_packetsize_function(data: bytes):
            return int.from_bytes(data[0:SIZE_BYTES_LENGTH], ENDIAN)

        def received_function(data: bytes):
            self.packetReceived(data[SIZE_BYTES_LENGTH:])

        self.__buffered_async_receiver = BufferedAsyncReceiver(BUFFER_SIZE, get_packetsize_function, received_function)

    def dataReceived(self, data: bytes):
        self.__buffered_async_receiver.append_data(data)

    @abstractmethod
    def packetReceived(self, data: bytes):
        pass

    def write(self, data: bytes):
        sized_data = bytearray(len(data) + SIZE_BYTES_LENGTH)
        sized_data[0:SIZE_BYTES_LENGTH] = (len(sized_data)).to_bytes(SIZE_BYTES_LENGTH, ENDIAN)
        sized_data[SIZE_BYTES_LENGTH:] = data
        self.transport.write(bytes(sized_data))
