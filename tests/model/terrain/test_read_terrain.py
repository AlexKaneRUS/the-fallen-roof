import os
from unittest import TestCase

from src.model.terrain.read_terrain import read_terrain
from src.model.terrain.terrain import Terrain
from src.model.terrain.wall import Wall


class TestRead_terrain(TestCase):
    def test_read_terrain(self):
        terrain = read_terrain(os.path.join(os.path.dirname(__file__), "map.XY"))
        self.assertIsInstance(terrain[0][0], Wall)
        self.assertIsInstance(terrain[1][1], Terrain)

        self.assertIsNone(read_terrain("foo"))
