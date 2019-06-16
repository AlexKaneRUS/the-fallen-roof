import pygame
from enum import Enum, IntEnum


class TurnOwner(Enum):
    '''
    Object that shows who holds current turn.
    '''
    PLAYER_TURN = 1
    AI_TURN = 0


class Direction(Enum):
    '''
    Object that describes movement direction.
    '''
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3


class Location(Enum):
    '''
    Object that describes current location:

    KT for Knowledge Temple
    RF for Random Forest
    EP for Exit Point
    '''
    KT = 0
    RF = 1
    EP = 2
