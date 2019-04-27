import random

import pygame

from src.model.characters.mobs.mob import Mob, MobFactory
from src.model.world_graph_node import WorldGraphNode
from src.model.characters.player import Player
import src.model.terrain.gen_terrain as gt
from src.util.enums import UserEvents


class WorldModel:
    def __init__(self, graph_repr):

        # actual state
        self.graph_repr = graph_repr
        self.current_location = None

        self.location_terrain = gt.gen_terrain()
        self.world_graph = self.terrain_to_world_graph(self.location_terrain)

        self.player = Player(self.world_graph)
        self.spawn_object_and_update_graph(self.player)

        for col in self.location_terrain:
            for cell in col:
                self.graph_repr['terrain'].add(cell)

        self.mobs = MobFactory.create_random_mobs(self.world_graph, 10)
        for mob in self.mobs:
            self.spawn_object_and_update_graph(mob)
            self.graph_repr['mobs'].add(mob)

        self.graph_repr['player'].add(self.player)

    def do_ai_turn(self):
        for mob in self.mobs:
            next_move = mob.get_next_turn((self.player.x, self.player.y))
            self.move_logic(mob, next_move)
        pygame.event.pump()

    def move_player(self, dir):
        next_move = self.player.get_next_turn(dir)
        self.move_logic(self.player, next_move)

    def check_player(self):
        if not self.player.is_alive():
            pygame.event.post(pygame.event.Event(UserEvents.GAME_OVER, {}))

    def check_mob(self, mob):
        if not mob.is_alive():
            self.world_graph[(mob.x, mob.y)].object = None
            self.mobs.remove(mob)
            self.graph_repr['mobs'].remove(mob)

    def spawn_object_and_update_graph(self, obj):
        possible_poss = list(
            filter(lambda x: self.world_graph[x].object is None,
                   self.world_graph.keys()))
        obj.set_coordinates(random.choice(possible_poss))
        self.world_graph[(obj.x, obj.y)].object = obj

    def move_logic(self, obj, next_move):
        other_obj = self.world_graph[next_move].object
        if other_obj is not None and (
                (isinstance(obj, Player) and issubclass(other_obj.__class__,
                                                        Mob)) or (
                        issubclass(obj.__class__, Mob) and isinstance(
                    other_obj, Player))):
            other_obj.damage(obj.strength)
            obj.damage(other_obj.strength)

            self.check_player()

            if issubclass(obj.__class__, Mob):
                self.check_mob(obj)
            else:
                self.check_mob(other_obj)

        if self.world_graph[next_move].object is None:
            self.world_graph[(obj.x, obj.y)].object = None

            obj.set_coordinates(next_move)
            self.world_graph[next_move].object = obj

    def terrain_to_world_graph(self, terrain):
        world_graph = {}
        for i in range(len(terrain)):
            for j in range(len(terrain[i])):
                if terrain[i][j].isPassable():
                    possible_directions = [(i - 1, j), (i + 1, j), (i, j - 1),
                                           (i, j + 1)]

                    def good_dir(d):
                        x, y = d
                        return 0 <= x < len(terrain) and 0 <= y < len(
                            terrain[i]) and \
                               terrain[x][y].isPassable()

                    world_graph[(i, j)] = WorldGraphNode(
                        list(filter(lambda x: good_dir(x),
                                    possible_directions)))

        return world_graph
