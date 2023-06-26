# -*- coding: utf-8 -*_

from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING, Dict

from twisted.logger import Logger

if TYPE_CHECKING:
    from network.protocol import GameProtocol


@dataclass
class PlayerStatus:
    idle = 0
    ready = 1
    game = 2

@dataclass
class Player:
    uid: int
    username: str
    image_url: str
    score: int
    status: PlayerStatus
    protocol: 'GameProtocol'

class PlayerManager:
    __logger = Logger(__name__)

    def __init__(self):
        self.__players: Dict[int, Player] = dict()

    def add_player(self, player: Player) -> None:
        self.__players[player.uid] = player

    def remove_player(self, uid) -> None:
        if uid in self.__players:
            self.__players.pop(uid)

    def get_players(self) -> Dict[int, Player]:
        return self.__players
    
    def get_player(self, uid) -> Player:
        if uid in self.__players:
            return self.__players[uid]
