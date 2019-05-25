import random

import pygame

from src.model.characters.has_inventory import HasInventory
from src.model.characters.mobs.mob import Mob, MobFactory
from src.model.items.item import Item, ItemFactory
from src.model.world_graph_node import WorldGraphNode
from src.model.characters.player import Player
import src.model.terrain.gen_terrain as gt
from src.util.enums import UserEvents


class WorldModel:
    def __init__(self):
        # init graphic representation
        self.graph_repr = {
            'terrain': pygame.sprite.Group(),
            'player': pygame.sprite.GroupSingle(),
            'mobs': pygame.sprite.Group(),
            'items': pygame.sprite.Group(),
        }

        self.current_location = None

        self.location_terrain = gt.gen_terrain()
        self.world_graph = self.terrain_to_world_graph(self.location_terrain)

        self.player = Player()
        self.spawn_object_and_update_graph(self.player)

        for col in self.location_terrain:
            for cell in col:
                self.graph_repr['terrain'].add(cell)

        self.mobs = MobFactory.create_random_mobs(20)
        for mob in self.mobs:
            self.spawn_object_and_update_graph(mob)
            self.graph_repr['mobs'].add(mob)

        self.items = ItemFactory.create_random_items(100)
        for item in self.items:
            self.spawn_object_and_update_graph(item)
            self.graph_repr['items'].add(item)

        self.graph_repr['player'].add(self.player)

    def do_ai_turn(self):
        for mob in self.mobs:
            self.move_logic(mob, mob.get_next_turn((self.player.x, self.player.y), self.world_graph))
        pygame.event.pump()

    def move_player(self, dir):
        self.move_logic(self.player, self.player.get_next_turn(dir))

    def check_player(self):
        if not self.player.is_alive():
            pygame.event.post(pygame.event.Event(UserEvents.GAME_OVER, {}))

    def check_mob(self, mob):
        if not mob.is_alive():
            self.world_graph[(mob.x, mob.y)].object = None
            self.mobs.remove(mob)
            self.graph_repr['mobs'].remove(mob)

            self.player.add_experience(mob.experience_from_killing)

    def spawn_object_and_update_graph(self, obj):
        possible_poss = list(
            filter(lambda x: self.world_graph[x].object is None,
                   self.world_graph.keys()))
        obj.set_coordinates(random.choice(possible_poss))
        self.world_graph[(obj.x, obj.y)].object = obj

    def move_logic(self, obj, next_move):
        if next_move not in self.world_graph.keys():
            next_move = (obj.x, obj.y)
        other_obj = self.world_graph[next_move].object

        if other_obj is not None:
            self._collision_process(obj, other_obj)

        if self.world_graph[next_move].object is None:
            self.world_graph[(obj.x, obj.y)].object = None

            obj.set_coordinates(next_move)
            self.world_graph[next_move].object = obj

    def _collision_process(self, obj, other_obj):
        if isinstance(obj, Player) and issubclass(other_obj.__class__,
                                                  Mob) or issubclass(
                obj.__class__, Mob) and isinstance(other_obj, Player):
            self._battle_process(obj, other_obj)
        elif isinstance(obj, Player) and isinstance(other_obj,
                                                    Item) or issubclass(
                obj.__class__, Mob) and isinstance(other_obj, Item):
            self._item_pickup_process(obj, other_obj)

    def _battle_process(self, obj, other_obj):
        obj.attack(other_obj)
        other_obj.damage(obj.strength)
        other_obj.attack(obj)
        obj.damage(other_obj.strength)

        self.check_player()

        if issubclass(obj.__class__, Mob):
            self.check_mob(obj)
        else:
            self.check_mob(other_obj)

    def _item_pickup_process(self, with_inventory: HasInventory, item: Item):
        self.world_graph[(item.x, item.y)].object = None
        self.items.remove(item)
        self.graph_repr['items'].remove(item)

        with_inventory.pickup_item(item)

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
