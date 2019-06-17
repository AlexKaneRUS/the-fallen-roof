# will be removed, just for simplicity
import os
from src.util.config import HEIGHT_IN_TILES, WIDTH_IN_TILES
from src.model.terrain.floor import Floor
from src.model.terrain.wall import Wall


def read_terrain(file_path):
    if not os.path.isfile(file_path):
        return
    with open(file_path) as file:
        terrain = [
            [(Floor if char == ' ' else Wall)(x, y) for x, char in enumerate(line)]
            for y, line in enumerate(file.read().splitlines())
        ]
    if len(terrain) != HEIGHT_IN_TILES:
        raise Exception("expected height " + str(HEIGHT_IN_TILES) + " but got " + str(len(terrain)))
    for row in terrain:
        if len(row) != WIDTH_IN_TILES:
            raise Exception("expected width " + str(WIDTH_IN_TILES) + " but got " + str(len(row)))
    return terrain
