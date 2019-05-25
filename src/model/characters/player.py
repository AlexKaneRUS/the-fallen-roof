import pygame

from src.model.characters.has_inventory import HasInventory
from src.model.has_coordinates import HasCoordinates, \
    BaseMovementHandlerState, ConfusedMovementHandlerStateDecorator
from src.util.config import screen_height, screen_width, tile_width
from src.util.singleton import Singleton


class Player(HasCoordinates, HasInventory, pygame.sprite.Sprite,
             metaclass=Singleton):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        HasCoordinates.__init__(self, tile_width, self.rect,
                                ConfusedMovementHandlerStateDecorator(
                                    BaseMovementHandlerState(), 10))

        self.next_level = 100
        self.basic_health = 100
        self.basic_strength = 10

        HasInventory.__init__(self, self.basic_health, self.basic_strength)

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

        if direction.contains_down() and self.rect.bottom < screen_height:
            y += 1
        if direction.contains_up() and self.rect.top > 0:
            y -= 1
        if direction.contains_left() and self.rect.left > 0:
            x -= 1
        if direction.contains_right() and self.rect.right < screen_width:
            x += 1

        return x, y
