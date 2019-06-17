import pygame

from src.model.characters.has_inventory import HasInventory
from src.model.can_move import CanMove, \
    BaseMovementHandlerState, ConfusedMovementHandlerStateDecorator
from src.util.config import HEIGHT_IN_TILES, WIDTH_IN_TILES, TILE_WIDTH
from src.util.singleton import Singleton
from src.model.has_image import HasImage


class Player(CanMove, HasImage, HasInventory):
    def __init__(self, name='2nd year master student'):
        CanMove.__init__(
            self,
            ConfusedMovementHandlerStateDecorator(BaseMovementHandlerState(), 10)
        )
        HasImage.__init__(self)

        self.name = name
        self.next_level = 100
        self.basic_health = 100
        self.basic_strength = 10

        HasInventory.__init__(self, self.basic_health, self.basic_strength)

    def generate_image(self):
        image = pygame.Surface((TILE_WIDTH, TILE_WIDTH))
        image.fill((255, 255, 255))
        return image

    def on_pickup(self):
        pass

    def level_up(self):
        if self.experience >= self.next_level:
            print("Level up!")

            self.level += int(self.experience / self.next_level)
            self.experience %= self.next_level

            self.health = 1.5 ** self.level * self.basic_health
            self.strength = 1.5 ** self.level * self.basic_strength

            for x in self.equipped_items:
                self.unequip_item(x)
                self.equip_item(x)

    def get_next_turn(self, direction):
        direction, self.movement_handler_state = self.movement_handler_state(
            direction)

        x = self.x
        y = self.y

        if direction.contains_down() and y < HEIGHT_IN_TILES:
            y += 1
        if direction.contains_up() and y > 0:
            y -= 1
        if direction.contains_left() and x > 0:
            x -= 1
        if direction.contains_right() and x < WIDTH_IN_TILES:
            x += 1

        return x, y

    def get_health(self):
        return self.health

    def get_strength(self):
        return self.strength

    def get_level(self):
        return self.level

    def get_experience(self):
        return self.experience

    def get_next_level_experience(self):
        return self.next_level
