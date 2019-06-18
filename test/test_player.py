import unittest

from src.model.characters.player import Player
from src.model.terrain.floor import Floor
from src.model.terrain.wall import Wall
import src.util.config as config
from src.util.config import tile_width
from src.util.enums import Direction


def gen_terrain():
    n = 5
    m = 5
    config.screen_width = n * tile_width
    config.screen_height = m * tile_width
    terrain = [
        [Floor(0, 0), Wall(0, 1), Floor(0, 2), Floor(0, 3), Wall(0, 4)],
        [Floor(1, 0), Floor(1, 1), Floor(1, 2), Wall(1, 3), Wall(1, 4)],
        [Floor(2, 0), Floor(2, 1), Wall(2, 2), Wall(2, 3), Wall(2, 4)],
        [Wall(3, 0), Floor(3, 1), Floor(3, 2), Floor(3, 3), Wall(3, 4)],
        [Floor(4, 0), Wall(4, 1), Floor(4, 2), Floor(4, 3), Floor(4, 4)]
    ]
    return terrain


def get_player_at_position(x, y):
    player = Player()
    player.x = x
    player.y = y
    player.rect.move_ip(x * tile_width, y * tile_width)
    return player


class TestMovement(unittest.TestCase):
    def test_left_good(self):
        terrain = gen_terrain()

        player = get_player_at_position(2, 1)
        player.handle_movement(Direction.LEFT, terrain)
        self.assertEqual((player.x, player.y), (1, 1))

        player = get_player_at_position(4, 2)
        player.handle_movement(Direction.LEFT, terrain)
        self.assertEqual((player.x, player.y), (3, 2))

    def test_left_bound(self):
        terrain = gen_terrain()

        player = get_player_at_position(0, 0)
        player.handle_movement(Direction.LEFT, terrain)
        self.assertEqual((player.x, player.y), (0, 0))

        player = get_player_at_position(0, 3)
        player.handle_movement(Direction.LEFT, terrain)
        self.assertEqual((player.x, player.y), (0, 3))

    def test_left_wall(self):
        terrain = gen_terrain()

        player = get_player_at_position(4, 0)
        player.handle_movement(Direction.LEFT, terrain)
        self.assertEqual((player.x, player.y), (4, 0))

        player = get_player_at_position(1, 1)
        player.handle_movement(Direction.LEFT, terrain)
        self.assertEqual((player.x, player.y), (1, 1))

    def test_right_good(self):
        terrain = gen_terrain()

        player = get_player_at_position(0, 2)
        player.handle_movement(Direction.RIGHT, terrain)
        self.assertEqual((player.x, player.y), (1, 2))

        player = get_player_at_position(3, 3)
        player.handle_movement(Direction.RIGHT, terrain)
        self.assertEqual((player.x, player.y), (4, 3))

    def test_right_bound(self):
        terrain = gen_terrain()

        player = get_player_at_position(4, 2)
        player.handle_movement(Direction.RIGHT, terrain)
        self.assertEqual((player.x, player.y), (4, 2))

        player = get_player_at_position(4, 4)
        player.handle_movement(Direction.RIGHT, terrain)
        self.assertEqual((player.x, player.y), (4, 4))

    def test_right_wall(self):
        terrain = gen_terrain()

        player = get_player_at_position(2, 0)
        player.handle_movement(Direction.RIGHT, terrain)
        self.assertEqual((player.x, player.y), (2, 0))

        player = get_player_at_position(1, 2)
        player.handle_movement(Direction.RIGHT, terrain)
        self.assertEqual((player.x, player.y), (1, 2))

    def test_down_good(self):
        terrain = gen_terrain()

        player = get_player_at_position(1, 1)
        player.handle_movement(Direction.DOWN, terrain)
        self.assertEqual((player.x, player.y), (1, 2))

        player = get_player_at_position(3, 1)
        player.handle_movement(Direction.DOWN, terrain)
        self.assertEqual((player.x, player.y), (3, 2))

    def test_down_bound(self):
        terrain = gen_terrain()

        player = get_player_at_position(4, 4)
        player.handle_movement(Direction.DOWN, terrain)
        self.assertEqual((player.x, player.y), (4, 4))

    def test_down_wall(self):
        terrain = gen_terrain()

        player = get_player_at_position(0, 0)
        player.handle_movement(Direction.DOWN, terrain)
        self.assertEqual((player.x, player.y), (0, 0))

        player = get_player_at_position(3, 3)
        player.handle_movement(Direction.DOWN, terrain)
        self.assertEqual((player.x, player.y), (3, 3))

    def test_up_good(self):
        terrain = gen_terrain()

        player = get_player_at_position(1, 2)
        player.handle_movement(Direction.UP, terrain)
        self.assertEqual((player.x, player.y), (1, 1))

        player = get_player_at_position(4, 4)
        player.handle_movement(Direction.UP, terrain)
        self.assertEqual((player.x, player.y), (4, 3))

    def test_up_bound(self):
        terrain = gen_terrain()

        player = get_player_at_position(1, 0)
        player.handle_movement(Direction.UP, terrain)
        self.assertEqual((player.x, player.y), (1, 0))

        player = get_player_at_position(2, 0)
        player.handle_movement(Direction.UP, terrain)
        self.assertEqual((player.x, player.y), (2, 0))

    def test_up_wall(self):
        terrain = gen_terrain()

        player = get_player_at_position(3, 1)
        player.handle_movement(Direction.UP, terrain)
        self.assertEqual((player.x, player.y), (3, 1))

        player = get_player_at_position(4, 2)
        player.handle_movement(Direction.UP, terrain)
        self.assertEqual((player.x, player.y), (4, 2))
