from abc import ABC, abstractmethod
import random
import pygame
from src.model.has_image import HasImage


class HasCoordinates(HasImage, ABC):
    class ImageSprite(pygame.sprite.Sprite):
        def __init__(self, image):
            pygame.sprite.Sprite.__init__(self)
            self.image = image
            self.rect = image.get_rect()

    def __init__(self, tile_width, movement_handler_state=None):
        self.x = 0
        self.y = 0

        HasImage.__init__(self)
        self.tile_width = tile_width

        self.movement_handler_state = movement_handler_state

    def set_coordinates(self, coordinates):
        self.x, self.y = coordinates
        self.rect.topleft = (self.x * self.tile_width, self.y * self.tile_width)


class BaseMovementHandlerState:
    def __init__(self):
        pass

    def __call__(self, direction):
        return direction, self


class ConfusedMovementHandlerStateDecorator:
    def __init__(self, base, duration):
        self._base = base
        self._duration = duration

    def __call__(self, direction):
        direction, base = self._base(direction)
        if self._duration:
            return (
                direction.turn_clockwise(random.randint(-1, 1)),
                ConfusedMovementHandlerStateDecorator(base, self._duration - 1)
            )
        else:
            return direction, base
