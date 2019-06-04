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
        """
        Moves Player according to given direction.

        :param dir: Direction where Player should be moved.
        :return: None.
        """

        next_move = self.player.get_next_turn(dir)
        self.move_logic(self.player, next_move)

    def check_player(self):
        """
        Method checks whether Player is alive. If not, the GAME_OVER event is
        posted.

        :return: None.
        """

        if not self.player.is_alive():
            pygame.event.post(pygame.event.Event(UserEvents.GAME_OVER, {}))

    def check_mob(self, mob):
        """
        Method checks whether mob is alive. If not, it is removed from list of
        active mobs and from the screen.

        :param mob: Mob to be checked.
        :return: None.
        """

        if not mob.is_alive():
            self.world_graph[(mob.x, mob.y)].object = None
            self.mobs.remove(mob)
            self.graph_repr['mobs'].remove(mob)

    def spawn_object_and_update_graph(self, obj):
        """
        Given object finds its place in the world_graph and places it there.
        :param obj: Object to be placed.
        :return: None.
        """

        possible_poss = list(
            filter(lambda x: self.world_graph[x].object is None,
                   self.world_graph.keys()))
        obj.set_coordinates(random.choice(possible_poss))
        self.world_graph[(obj.x, obj.y)].object = obj

    def move_logic(self, obj, next_move):
        """
        Method decides how given object obj should be moved
        considering its next_move. It may depend on whether next_move tile
        is taken by some other object.

        :param obj: Object to be moved.
        :param next_move: Coordinates where object wants to go.
        :return: None.
        """

        other_obj = self.world_graph[next_move].object
        if other_obj is not None and (
                (isinstance(obj, Player) and isinstance(other_obj,
                                                        Mob)) or (
                        isinstance(obj, Mob) and isinstance(
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
        """
        Converts terrain object to graph consisting of WorldGraphNodes.

        :param terrain: Terrain to be converted.
        :return: Graph consisting of WorldGraphNodes.
        """

        world_graph = {}
        for i in range(len(terrain)):
            for j in range(len(terrain[i])):
                if terrain[i][j].isPassable():
                    possible_directions = [(i - 1, j), (i + 1, j), (i, j - 1),
                                           (i, j + 1)]

                    world_graph[(i, j)] = WorldGraphNode(
                        list(filter(lambda x: self._good_dir(terrain, x, i),
                                    possible_directions)))

        return world_graph

    @staticmethod
    def _good_dir(terrain, d, i):
        """
        Checks that terrain piece exists and is passable.

        :param terrain: Terrain itself.
        :param d: Coordinates of terrain piece.
        :param i: Current line in terrain.
        :return: True is piece of terrain is valid and is passable. False otherwise.
        """

        x, y = d
        return 0 <= x < len(terrain) and 0 <= y < len(
            terrain[i]) and \
               terrain[x][y].isPassable()
