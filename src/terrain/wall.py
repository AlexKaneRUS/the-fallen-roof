from src.terrain.terrain import Terrain


class Wall(Terrain):
    def __init__(self, x, y):
        super().__init__(x, y, color=(5, 5, 5))

    def isPassable(self):
        return False
