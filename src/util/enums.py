import pygame
from enum import Enum, IntEnum


class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    BROWN = (174, 152, 105)
    YELLOW = (205, 216, 55)


class TurnOwner(Enum):
    PLAYER_TURN = 1
    AI_TURN = 0


class Direction(Enum):
    UP = 0
    UP_RIGHT = 1
    RIGHT = 2
    DOWN_RIGHT = 3
    DOWN = 4
    DOWN_LEFT = 5
    LEFT = 6
    UP_LEFT = 7

    def turn_clockwise(self, angle):
        return Direction((self.value + angle) % len(Direction))

    def contains_up(self):
        return self == Direction.UP or self == Direction.UP_LEFT or self == Direction.UP_RIGHT

    def contains_right(self):
        return self == Direction.RIGHT or self == Direction.UP_RIGHT or self == Direction.DOWN_RIGHT

    def contains_down(self):
        return self == Direction.DOWN or self == Direction.DOWN_LEFT or self == Direction.DOWN_RIGHT

    def contains_left(self):
        return self == Direction.LEFT or self == Direction.UP_LEFT or self == Direction.DOWN_LEFT


class Location(Enum):
    KT = 0
    RF = 1
    EP = 2


class UserEvents(IntEnum):
    GAME_OVER = pygame.USEREVENT + 1
    EMPTY = pygame.USEREVENT + 2
