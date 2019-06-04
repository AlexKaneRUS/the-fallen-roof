class WorldGraphNode:
    """
    Class representing one tile in the game and what is placed on that tile.
    """

    def __init__(self, neighbour_tiles):
        self.object = None
        self.neighbour_tiles = neighbour_tiles
