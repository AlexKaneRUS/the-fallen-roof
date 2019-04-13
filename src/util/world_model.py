from src.characters.player import Player
import src.terrain.gen_terrain as gt


class WorldModel:
    def __init__(self, graph_repr):
        self.graph_repr = graph_repr

        self.current_location = None

        self.location_terrain = gt.gen_terrain()
        for col in self.location_terrain:
            for cell in col:
                self.graph_repr['terrain'].add(cell)
        self.player = Player()
        self.graph_repr['player'].add(self.player)

    def move_player(self, dir):
        self.player.handle_movement(dir, self.location_terrain)

