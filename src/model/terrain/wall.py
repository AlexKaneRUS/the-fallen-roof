from src.model.terrain.terrain import Terrain


class Wall(Terrain):
    '''
    Object representing 'wall' terrain type.
    '''
    def __init__(self, x, y):
        super().__init__(x, y, color=(5, 5, 5))

    def is_passable(self):
        return False