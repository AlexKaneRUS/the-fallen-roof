from enum import Enum
from src.characters.player import Player
import src.terrain.gen_terrain as gt


class WorldModel:

    class Location(Enum):
        KT = 0
        RF = 1
        EP = 2

    def __init__(self, graph_repr):
        self.graph_repr = graph_repr

        self.current_location = WorldModel.Location.KT

        self.location_terrain = gt.gen_terrain()
        for col in self.location_terrain:
            for cell in col:
                self.graph_repr['terrain'].add(cell)
        self.player = Player()
        self.graph_repr['player'].add(self.player)

    def handle_key(self, key):
        self.player.handle_movement(key, self.location_terrain)

