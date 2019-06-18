import pygame
from src.model.characters.player import Player
import src.model.terrain.gen_terrain as gt


class WorldModel:
    '''
    Object that represents whole game world.
    '''
    def __init__(self, graph_repr):
        """
        :param graph_repr: Graphical representation.
        """
        # actual state
        self.graph_repr = graph_repr
        self.current_location = None
        self.player = Player()
        self.map = None # will be tile grid
        self.npc = [] # will be list of active npc


        # temporary code

        self.location_terrain = gt.gen_terrain()
        for col in self.location_terrain:
            for cell in col:
                self.graph_repr['terrain'].add(cell)

        self.graph_repr['player'].add(self.player)

    def do_ai_turn(self):
        """
        Describes logic of AI turn.
        """
        pygame.event.pump()

    def move_player(self, dir):
        """
        Moves player in specific direction.
        :param dir:
        """
        self.player.handle_movement(dir, self.location_terrain)

