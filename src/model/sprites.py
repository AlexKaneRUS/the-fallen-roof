import pygame
from src.util.config import tile_width


class Sprites:
    class Sprite(pygame.sprite.Sprite):
        def __init__(self, image, topleft):
            pygame.sprite.Sprite.__init__(self)
            self.image = image
            self.rect = image.get_rect(topleft=topleft)

    def __init__(self):
        self.group = pygame.sprite.Group()
        self.indexed_sprites = {}

    def add(self, has_image):
        self.indexed_sprites[has_image] = Sprites.Sprite(
            has_image.generate_image(),
            (has_image.x * tile_width, has_image.y * tile_width)
        )
        self.group.add(self.indexed_sprites[has_image])

    def remove(self, has_image):
        self.group.remove(self.indexed_sprites[has_image])
        del self.indexed_sprites[has_image]

    def draw(self, *args):
        return self.group.draw(*args)

    def get_rect(self, has_image):
        return self.indexed_sprites[has_image].rect
