import os
import random
from enum import Enum

import pygame

from src.model.has_coordinates import HasCoordinates
from src.util.config import tile_width

max_buff = 10

offensive_item_prefixes = ['Sword', 'Gun', 'Cannon', 'Knife']
offensive_item_suffixes = ['of infinite power', 'of wisdom', 'of Great Day',
                           'of fun', 'of friendship']

defensive_item_prefixes = ['Shield', 'Armor', 'Helmet', 'Jacket']
defensive_item_suffixes = ['of good defense', 'of love', 'the Defender',
                           'the Cool Guy', 'Good Boy']


class ItemType(Enum):
    OFFENSIVE = 'offensive'
    DEFENSIVE = 'defensive'


class Item(HasCoordinates):
    def __init__(self, name, health_buff, strength_buff, image_generator, item_type):
        self.name = name

        self.image_generator = image_generator
        HasCoordinates.__init__(self, tile_width)

        self.health_buff = health_buff
        self.strength_buff = strength_buff

        self.item_type = item_type

    def generate_image(self):
        return self.image_generator


class ItemFactory:
    @staticmethod
    def _create_item(item_type):
        path = os.path.join(os.path.dirname(__file__), "resources", item_type.value)
        images = [
            pygame.transform.scale(pygame.image.load(os.path.join(path, x)),
                                   (tile_width, tile_width))
            for x in os.listdir(path)]

        name = None

        health = 0
        strength = 0

        if item_type == ItemType.DEFENSIVE:
            name = random.choice(
                defensive_item_prefixes) + ' ' + random.choice(
                defensive_item_suffixes)

            health = random.randint(0, max_buff)
        elif item_type == ItemType.OFFENSIVE:
            name = random.choice(
                offensive_item_prefixes) + ' ' + random.choice(
                offensive_item_suffixes)

            strength = random.randint(0, max_buff)

        return Item(
            name,
            health,
            strength,
            random.choice(images),
            item_type
        )

    @staticmethod
    def create_offensive_item():
        return ItemFactory._create_item(ItemType.OFFENSIVE)

    @staticmethod
    def create_defensive_item():
        return ItemFactory._create_item(ItemType.DEFENSIVE)

    @staticmethod
    def create_random_items(n=1):
        return [random.choice([ItemFactory.create_offensive_item,
                               ItemFactory.create_defensive_item])() for
                _
                in range(n)]
