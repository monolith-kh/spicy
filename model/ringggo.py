# -*- coding: utf-8 -*_

from dataclasses import dataclass, field
from typing import List, Dict

from twisted.logger import Logger


@dataclass
class Ringggo:
    no: int
    position_x: float
    position_y: str
    timestamp: int


class RingggoManager:
    __logger = Logger(__name__)

    def __init__(self):
        self.__ringggos: Dict[int, Ringggo] = dict()

    def add_ringggo(self, ringggo: Ringggo) -> None:
        self.__ringggos[ringggo.no] = ringggo

    def remove_ringggo(self, no) -> None:
        if no in self.__ringggos:
            self.__ringggos.pop(no)

    def get_ringggos(self) -> Dict[int, Ringggo]:
        return self.__ringggos
    
    def get_ringggo(self, no) -> Ringggo:
        if no in self.__ringggos:
            return self.__ringggos[no]
