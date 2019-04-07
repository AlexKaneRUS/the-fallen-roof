from src.terrain.terrain import Terrain


class Wall(Terrain):
    def __init__(self, x, y):
        super().__init__(x, y, color=(250, 250, 250))

    def isPassable(self):
        return False
