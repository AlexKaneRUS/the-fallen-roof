import random

import pygame

from src.model.characters.has_inventory import HasInventory
from src.model.characters.mobs.mob import Mob, MobFactory
from src.model.items.item import Item, ItemFactory
from src.model.world_graph_node import WorldGraphNode
from src.model.characters.player import Player
import src.model.terrain.gen_terrain as gt
from src.util.enums import UserEvents
from src.util.config import tile_width


class WorldModel:
    @staticmethod
    def generate():
        terrain = gt.gen_terrain()
        world_graph = WorldModel.terrain_to_world_graph(terrain)

        def spawn_object_and_update_graph(obj):
            possible_poss = list(filter(lambda x: world_graph[x].object is None, world_graph.keys()))
            obj.x, obj.y = random.choice(possible_poss)
            obj.rect.topleft = (obj.x * tile_width, obj.y * tile_width)
            world_graph[(obj.x, obj.y)].object = obj

        player = Player()
        spawn_object_and_update_graph(player)
        mobs = MobFactory.create_random_mobs(20)
        for mob in mobs:
            spawn_object_and_update_graph(mob)
        items = ItemFactory.create_random_items(100)
        for item in items:
            spawn_object_and_update_graph(item)
        return WorldModel(terrain, world_graph, player, mobs, items)

    def __init__(self, terrain, world_graph, player, mobs, items):
        self.location_terrain = terrain
        self.world_graph = world_graph
        self.player = player
        self.mobs = mobs
        self.items = items

    def build_graph_repr(self):
        graph_repr = pygame.sprite.Group()
        for col in self.location_terrain:
            for cell in col:
                graph_repr.add(cell)
        for mob in self.mobs:
            graph_repr.add(mob)
        for item in self.items:
            graph_repr.add(item)
        graph_repr.add(self.player)
        return graph_repr

    def do_ai_turn(self, graph_repr):
        for mob in self.mobs:
            self.move_logic(mob, mob.get_next_turn((self.player.x, self.player.y), self.world_graph), graph_repr)
        pygame.event.pump()

    def move_player(self, dir, graph_repr):
        self.move_logic(self.player, self.player.get_next_turn(dir), graph_repr)

    def check_player(self):
        if not self.player.is_alive():
            pygame.event.post(pygame.event.Event(UserEvents.GAME_OVER, {}))

    def move_logic(self, obj, next_move, graph_repr):
        def battle_process(obj, other_obj):
            def check_mob(mob):
                if not mob.is_alive():
                    self.world_graph[(mob.x, mob.y)].object = None
                    self.mobs.remove(mob)
                    graph_repr.remove(mob)

                    self.player.add_experience(mob.experience_from_killing)

            obj.attack(other_obj)
            other_obj.damage(obj.strength)
            other_obj.attack(obj)
            obj.damage(other_obj.strength)

            self.check_player()

            if issubclass(obj.__class__, Mob):
                check_mob(obj)
            else:
                check_mob(other_obj)

        def item_pickup_process(with_inventory: HasInventory, item: Item):
            self.world_graph[(item.x, item.y)].object = None
            self.items.remove(item)
            graph_repr.remove(item)

            with_inventory.pickup_item(item)

        def collision_process(obj, other_obj):
            if isinstance(obj, Player) and issubclass(other_obj.__class__,
                                                      Mob) or issubclass(
                obj.__class__, Mob) and isinstance(other_obj, Player):
                battle_process(obj, other_obj)
            elif isinstance(obj, Player) and isinstance(other_obj,
                                                        Item) or issubclass(
                obj.__class__, Mob) and isinstance(other_obj, Item):
                item_pickup_process(obj, other_obj)

        if next_move not in self.world_graph.keys():
            next_move = (obj.x, obj.y)
        other_obj = self.world_graph[next_move].object

        if other_obj is not None:
            collision_process(obj, other_obj)

        if self.world_graph[next_move].object is None:
            self.world_graph[(obj.x, obj.y)].object = None

            obj.x, obj.y = next_move
            obj.rect.topleft = (obj.x * tile_width, obj.y * tile_width)
            self.world_graph[next_move].object = obj

    @staticmethod
    def terrain_to_world_graph(terrain):
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
