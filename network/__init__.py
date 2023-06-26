# -*- coding:utf-8 -*-

BUFFER_SIZE = 1460
ENDIAN = 'big'
SIZE_BYTES_LENGTH = 2

from .protocol import GameProtocol, RtlsProtocol
from .factory import GameServerFactory, Worker, WorkerAction
