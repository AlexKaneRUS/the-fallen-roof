# will be removed, just for simplicity

from src.util.config import height_in_tiles, width_in_tiles
from src.model.terrain.floor import Floor
from src.model.terrain.wall import Wall
import random


def gen_terrain():
    return [
        [
            (Wall if (not (x == 0 and y == 0) and random.randrange(10) < 3) else Floor)(x, y)
            for x in range(width_in_tiles)
        ]
        for y in range(height_in_tiles)
    ]
