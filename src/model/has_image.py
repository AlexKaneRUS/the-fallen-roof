from abc import ABC, abstractmethod

import pygame


class HasImage(pygame.sprite.Sprite, ABC):
    def __init__(self, **get_rect_args):
        self.image = self.generate_image()
        self.rect = self.image.get_rect(**get_rect_args)
        pygame.sprite.Sprite.__init__(self)

    @abstractmethod
    def generate_image(self):
        raise NotImplemented
