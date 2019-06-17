# will be removed, just for simplicity

from src.util.config import HEIGHT_IN_TILES, WIDTH_IN_TILES
from src.model.terrain.floor import Floor
from src.model.terrain.wall import Wall
import random


def gen_terrain():
    return [
        [
            (Wall if (not (x == 0 and y == 0) and random.randrange(10) < 3) else Floor)(x, y)
            for x in range(WIDTH_IN_TILES)
        ]
        for y in range(HEIGHT_IN_TILES)
    ]
