import pygame
from enum import Enum, IntEnum


class TurnOwner(Enum):
    PLAYER_TURN = 1
    AI_TURN = 0


class Direction(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3


class Location(Enum):
    KT = 0
    RF = 1
    EP = 2


class UserEvents(IntEnum):
    GAME_OVER = pygame.USEREVENT + 1
