from src.model.terrain.terrain import Terrain


class Floor(Terrain):
    '''
    Object representing 'floor' terrain type.
    '''
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 250, 0))

    def is_passable(self):
        return True
