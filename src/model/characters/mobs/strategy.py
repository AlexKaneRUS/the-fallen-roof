import random
from abc import ABC
from collections import deque

from src.util.singleton import Singleton


class Strategy(ABC, metaclass=Singleton):
    """
    Abstract class that describes object that defines Mob's behaviour.
    """

    @staticmethod
    def _find_path_to_player(world_graph, mob_coordinates, player_coordinates):
        """
        Private method that using world_graph finds shortest path from Mob to a
        Player.

        :param world_graph: Object that contains placement of object in game.
        :param mob_coordinates: Current coordinates of Mob.
        :param player_coordinates: Current coordinates of a Player.
        :return: Shortest path (list of coordinates) from Mob to a Player.
        """

        visited = {x: -1 for x in world_graph}

        to_visit = deque()
        to_visit.append(mob_coordinates)

        while len(to_visit) > 0:
            cur = to_visit.popleft()

            for neigh in world_graph[cur].neighbour_tiles:
                if visited[neigh] == -1:
                    to_visit.append(neigh)
                    visited[neigh] = cur

        if visited[player_coordinates] == -1:
            return None
        else:
            res = []

            cur = player_coordinates
            while cur != mob_coordinates:
                res.append(cur)
                cur = visited[cur]

            return res

    @staticmethod
    def get_next_move(world_graph, mob_coordinates, player_coordinates):
        """
        Method that is responsible for figuring out where Mob will move next turn.

        :param world_graph: Object that contains placement of object in game.
        :param mob_coordinates: Current coordinates of Mob.
        :param player_coordinates: Current coordinates of a Player.
        :return: Coordinate where Mob should be moved to next turn.
        """

        pass


class AggressiveStrategy(Strategy):
    """
    Strategy that, if being used by Mob, defines its behaviour as aggressive.
    """

    @staticmethod
    def get_next_move(world_graph, mob_coordinates, player_coordinates):
        path = Strategy._find_path_to_player(world_graph, mob_coordinates,
                                             player_coordinates)

        if path is None:
            if world_graph[mob_coordinates].neighbour_tiles:
                return random.choice(
                    world_graph[mob_coordinates].neighbour_tiles)
            else:
                return mob_coordinates
        else:
            return path[-1]


class FrightenedStrategy(Strategy):
    """
    Strategy that, if being used by Mob, defines its behaviour as frightened.
    """

    @staticmethod
    def get_next_move(world_graph, mob_coordinates, player_coordinates):
        possible_coords = list(filter(lambda x: world_graph[x].object is None,
                                   world_graph[
                                       mob_coordinates].neighbour_tiles))
        possible_coords.append(mob_coordinates)

        def calculate_distance(x):
            path = Strategy._find_path_to_player(world_graph, x,
                                                 player_coordinates)

            if path is None:
                return -float('inf')
            else:
                return len(path)

        distances = list(map(lambda x: calculate_distance(x), possible_coords))

        max_distance = -float('inf')
        max_ids = [-1]

        for i in range(len(distances)):
            if distances[i] > max_distance:
                max_distance = distances[i]
                max_ids = [i]
            elif distances[i] == max_distance:
                max_ids.append(i)

        return possible_coords[random.choice(max_ids)]


class PassiveStrategy(Strategy):
    """
    Strategy that, if being used by Mob, defines its behaviour as passive.
    """

    @staticmethod
    def get_next_move(world_graph, mob_coordinates, possible_coords):
        return mob_coordinates
