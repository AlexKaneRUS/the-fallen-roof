# will be removed, just for simplicity

from src.util.config import screen_height, screen_width, tile_width
from src.model.terrain.floor import Floor
from src.model.terrain.wall import Wall
import random

def gen_terrain():
    n = screen_height // tile_width
    m = screen_width // tile_width
    terrain = [[None for i in range(n)] for j in range(m)]
    for i in range(n):
        for j in range(m):
            type = random.randrange(10)
            if type < 3:
                terrain[j][i] = Wall(j, i)
            else:
                terrain[j][i] = Floor(j, i)
    terrain[0][0] = Floor(0, 0)
    return terrain
