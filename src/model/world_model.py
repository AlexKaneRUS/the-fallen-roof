import pygame

from src.model.characters.base_movement_handler_state import BaseMovementHandlerState
from src.model.characters.confused_movement_handler_state_decorator import ConfusedMovementHandlerStateDecorator
from src.model.characters.player import Player
import src.model.terrain.gen_terrain as gt


class WorldModel:
    def __init__(self, graph_repr):

        # actual state
        self.graph_repr = graph_repr
        self.current_location = None
        self.player = Player(ConfusedMovementHandlerStateDecorator(BaseMovementHandlerState(), 10))
        self.map = None # will be tile grid
        self.npc = [] # will be list of active npc


        # temporary code

        self.location_terrain = gt.gen_terrain()
        for col in self.location_terrain:
            for cell in col:
                self.graph_repr['terrain'].add(cell)

        self.graph_repr['player'].add(self.player)


    def do_ai_turn(self):
        pygame.event.pump()

    def move_player(self, dir):
        self.player.handle_movement(dir, self.location_terrain)

