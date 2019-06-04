import unittest

from src.model.characters.has_coordinates import BaseMovementHandlerState, \
    ConfusedMovementHandlerStateDecorator
from src.model.characters.mobs.mob import MobFactory
from src.model.characters.mobs.strategy import AggressiveStrategy, \
    FrightenedStrategy, PassiveStrategy
from src.model.characters.player import Player
from src.model.world_graph_node import WorldGraphNode
from src.util.enums import Direction


def create_world_graph(n, without):
    def gen_neighbors(i, j):
        return list(filter(
            lambda x: 0 <= x[0] < n and 0 <= x[1] < n and x not in without,
            [(i + 1, j), (i - 1, j), (i, j + 1),
             (i, j - 1)]))

    world_graph = {(i, j): WorldGraphNode(gen_neighbors(i, j)) for j in
                   range(n) for i in range(n)}

    for x in without:
        world_graph.pop(x, None)

    return world_graph


class TestMobs(unittest.TestCase):

    def test_aggressive_strategy(self):
        world_graph = create_world_graph(10, [(1, 0)])

        self.assertEqual(
            AggressiveStrategy.get_next_move(world_graph, (0, 0), (9, 9)),
            (0, 1))

        world_graph = create_world_graph(10, [(4, 5), (6, 5)])

        self.assertEqual(
            AggressiveStrategy.get_next_move(world_graph, (5, 5), (9, 9)),
            (5, 6))

        world_graph = create_world_graph(10, [(0, 1), (1, 1), (2, 0)])

        self.assertEqual(
            AggressiveStrategy.get_next_move(world_graph, (1, 0), (9, 9)),
            (0, 0))

    def test_frightened_strategy(self):
        world_graph = create_world_graph(10, [(1, 0)])

        self.assertEqual(
            FrightenedStrategy.get_next_move(world_graph, (0, 0), (9, 9)),
            (0, 0))

        world_graph = create_world_graph(10, [(4, 5), (6, 5)])

        self.assertEqual(
            FrightenedStrategy.get_next_move(world_graph, (5, 5), (9, 9)),
            (5, 4))

        world_graph = create_world_graph(10,
                                         [(0, 1), (1, 1), (2, 0)])

        self.assertEqual(
            FrightenedStrategy.get_next_move(world_graph, (1, 0), (9, 9)),
            (1, 0))

    def test_passive_strategy(self):
        world_graph = create_world_graph(10, [(1, 0)])

        self.assertEqual(
            PassiveStrategy.get_next_move(world_graph, (0, 0), (9, 9)),
            (0, 0))

        world_graph = create_world_graph(10, [(4, 5), (6, 5)])

        self.assertEqual(
            PassiveStrategy.get_next_move(world_graph, (5, 5), (9, 9)),
            (5, 5))

        world_graph = create_world_graph(10,
                                         [(0, 1), (1, 1), (2, 0)])

        self.assertEqual(
            PassiveStrategy.get_next_move(world_graph, (1, 0), (9, 9)),
            (1, 0))

    def test_mob_battle_system(self):
        world_graph = create_world_graph(10, [])

        aggressive_mob = MobFactory.create_aggressive_mob(world_graph)
        frightened_mob = MobFactory.create_frightened_mob(world_graph)
        passive_mob = MobFactory.create_passive_mob(world_graph)

        aggressive_mob.damage(aggressive_mob.strength)
        self.assertTrue(aggressive_mob.is_alive())
        aggressive_mob.damage(aggressive_mob.strength)
        self.assertFalse(aggressive_mob.is_alive())

        frightened_mob.damage(passive_mob.strength)
        self.assertTrue(frightened_mob.is_alive())
        frightened_mob.damage(aggressive_mob.strength)
        self.assertFalse(frightened_mob.is_alive())

        passive_mob.damage(aggressive_mob.strength)
        self.assertTrue(passive_mob.is_alive())
        passive_mob.damage(frightened_mob.strength)
        self.assertFalse(passive_mob.is_alive())


class TestPlayer(unittest.TestCase):

    def test_player_movement(self):
        world_graph = create_world_graph(10, [])

        player = Player(world_graph)
        player.movement_handler_state = BaseMovementHandlerState()

        player.x = 0
        player.y = 0

        self.assertEqual(player.get_next_turn(Direction.UP), (0, 0))
        self.assertEqual(player.get_next_turn(Direction.DOWN), (0, 1))
        self.assertEqual(player.get_next_turn(Direction.LEFT), (0, 0))
        self.assertEqual(player.get_next_turn(Direction.RIGHT), (1, 0))

        player.set_coordinates(player.get_next_turn(Direction.DOWN))
        player.set_coordinates(player.get_next_turn(Direction.DOWN))
        player.set_coordinates(player.get_next_turn(Direction.RIGHT))
        player.set_coordinates(player.get_next_turn(Direction.RIGHT))
        self.assertEqual((player.x, player.y), (2, 2))

        player.set_coordinates(player.get_next_turn(Direction.UP))
        player.set_coordinates(player.get_next_turn(Direction.RIGHT))
        player.set_coordinates(player.get_next_turn(Direction.LEFT))
        self.assertEqual((player.x, player.y), (2, 1))

        player.set_coordinates(player.get_next_turn(Direction.DOWN))
        player.set_coordinates(player.get_next_turn(Direction.DOWN))
        player.set_coordinates(player.get_next_turn(Direction.DOWN))
        player.set_coordinates(player.get_next_turn(Direction.DOWN))
        player.set_coordinates(player.get_next_turn(Direction.RIGHT))
        self.assertEqual((player.x, player.y), (3, 5))

    def test_confused_player_movement(self):
        world_graph = create_world_graph(10, [])

        player = Player(world_graph)
        player.movement_handler_state = ConfusedMovementHandlerStateDecorator(
            BaseMovementHandlerState(), 4)

        player.x = 0
        player.y = 0

        lefts = [(0, 0), (0, 1)]
        rights = [(1, 0), (1, 1)]
        ups = [(0, 0), (1, 0)]
        downs = [(0, 1), (1, 1)]

        self.assertTrue(player.get_next_turn(Direction.UP) in ups)
        self.assertTrue(player.get_next_turn(Direction.DOWN) in downs)
        self.assertTrue(player.get_next_turn(Direction.LEFT) in lefts)
        self.assertTrue(player.get_next_turn(Direction.RIGHT) in rights)

        self.assertEqual(player.get_next_turn(Direction.UP), (0, 0))
        self.assertEqual(player.get_next_turn(Direction.DOWN), (0, 1))
        self.assertEqual(player.get_next_turn(Direction.LEFT), (0, 0))
        self.assertEqual(player.get_next_turn(Direction.RIGHT), (1, 0))

    def test_player_battle_system(self):
        world_graph = create_world_graph(10, [])

        player = Player(world_graph)

        for i in range(int(player.health / 10) - 1):
            player.damage(10)
            self.assertTrue(player.is_alive())

        player.damage(10)
        self.assertFalse(player.is_alive())


if __name__ == '__main__':
    unittest.main()
