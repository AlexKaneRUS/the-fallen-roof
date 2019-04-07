import pygame
from src.util.config import screen_height, screen_width, tile_width

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()


    def handle_movement(self, key):
        if key == pygame.K_DOWN and self.rect.bottom < screen_height:
            self.rect.move_ip(0, tile_width)
        if key == pygame.K_UP and self.rect.top > 0:
            self.rect.move_ip(0, -tile_width)
        if key == pygame.K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-tile_width, 0)
        if key == pygame.K_RIGHT and self.rect.right < screen_width:
            self.rect.move_ip(tile_width, 0)
