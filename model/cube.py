# -*- coding: utf-8 -*_

from dataclasses import dataclass, field
from typing import List


@dataclass
class CubeType:
    normal = 0
    event = 1

@dataclass
class Vec3:
    x: float
    y: float
    z: float

@dataclass
class Cube:
    uid: int
    pos_cur: Vec3
    pos_target: Vec3
    speed: float
    type_: CubeType

@dataclass
class CubeList:
    Cubes: List[Cube] = field(default_factory=list)
