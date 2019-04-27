import random
from collections import deque

from src.model.characters.player import Player


class Strategy:
    @staticmethod
    def _find_path_to_player(world_graph, mob_coordinates, player_coordinates):
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


class AggressiveStrategy(Strategy):
    @staticmethod
    def get_next_move(world_graph, mob_coordinates, player_coordinates):
        path = Strategy._find_path_to_player(world_graph, mob_coordinates, player_coordinates)

        if path is None:
            if world_graph[mob_coordinates].neighbour_tiles:
                return random.choice(world_graph[mob_coordinates].neighbour_tiles)
            else:
                return mob_coordinates
        else:
            return path[-1]
