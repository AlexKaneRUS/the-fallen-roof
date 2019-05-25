import pygame

from src.model.characters.has_inventory import HasInventory
from src.model.can_move import CanMove, \
    BaseMovementHandlerState, ConfusedMovementHandlerStateDecorator
from src.util.config import height_in_tiles, width_in_tiles, tile_width
from src.util.singleton import Singleton
from src.model.has_image import HasImage


class Player(CanMove, HasImage, HasInventory, metaclass=Singleton):
    def __init__(self):
        CanMove.__init__(
            self,
            ConfusedMovementHandlerStateDecorator(BaseMovementHandlerState(), 10)
        )
        HasImage.__init__(self)

        self.next_level = 100
        self.basic_health = 100
        self.basic_strength = 10

        HasInventory.__init__(self, self.basic_health, self.basic_strength)

    def generate_image(self):
        image = pygame.Surface((tile_width, tile_width))
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

        if direction.contains_down() and y < height_in_tiles:
            y += 1
        if direction.contains_up() and y > 0:
            y -= 1
        if direction.contains_left() and x > 0:
            x -= 1
        if direction.contains_right() and x < width_in_tiles:
            x += 1

        return x, y
