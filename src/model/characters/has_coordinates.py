from abc import ABC, abstractmethod


class HasCoordinates(ABC):
    def __init__(self, tile_width, rect):
        self.x = 0
        self.y = 0
        self.rect = rect
        self.tile_width = tile_width

    def set_coordinates(self, new_coordinates):
        self.rect.move_ip((new_coordinates[0] - self.x) * self.tile_width,
                          (new_coordinates[1] - self.y) * self.tile_width)
        self.x, self.y = new_coordinates

    @abstractmethod
    def get_next_turn(self, *args):
        pass
