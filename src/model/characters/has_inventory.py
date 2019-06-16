from abc import ABC, abstractmethod

import pygame

from src.model.characters import has_battle_system
from src.model.characters.has_battle_system import HasBattleSystem
from src.model.items.item import Item
from src.util.button import Button
from src.util.enums import Color, UserEvents
from copy import deepcopy


class HasInventory(ABC, HasBattleSystem):
    def __init__(self, health, strength):
        HasBattleSystem.__init__(self, health, strength)

        self.items = {}
        self.equipped_items = []

    def pickup_item(self, item: Item):
        item.x = None
        item.y = None

        self.items[len(self.items)] = item

        self.on_pickup()

    @abstractmethod
    def on_pickup(self):
        pass

    def equip_item(self, i):
        if i not in self.equipped_items:
            self.equipped_items.append(i)

            self.health += self.items[i].health_buff
            self.strength += self.items[i].strength_buff

    def unequip_item(self, i):
        if i in self.equipped_items:
            self.equipped_items.remove(i)

            self.health -= self.items[i].health_buff
            self.strength -= self.items[i].strength_buff
