from enum import Enum
from src.characters.player import Player


class WorldModel:

    class Location(Enum):
        KT = 0
        RF = 1
        EP = 2

    def __init__(self, graph_repr):
        self.graph_repr = graph_repr

        self.current_location = WorldModel.Location.KT

        self.location_map = None
        self.player = Player()
        self.graph_repr['player'].add(self.player)

    def handle_key(self, key):
        self.player.handle_movement(key)

