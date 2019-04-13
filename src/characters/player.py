import pygame
from src.util.enums import Direction
from src.util.config import screen_height, screen_width, tile_width
from src.util.singleton import Singleton


class Player(pygame.sprite.Sprite, metaclass=Singleton):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_width, tile_width))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        self.x = 0
        self.y = 0

        # pygame.event.post(pygame.event.Event(UserEvents.GAME_OVER))

    def handle_movement(self, dir, terrain):
        if dir == Direction.DOWN and self.rect.bottom < screen_height:
            if terrain[self.x][self.y + 1].isPassable():
                self.y += 1
                self.rect.move_ip(0, tile_width)
        if dir == Direction.UP and self.rect.top > 0:
            if terrain[self.x][self.y - 1].isPassable():
                self.y -= 1
                self.rect.move_ip(0, -tile_width)
        if dir == Direction.LEFT and self.rect.left > 0:
            if terrain[self.x - 1][self.y].isPassable():
                self.x -= 1
                self.rect.move_ip(-tile_width, 0)
        if dir == Direction.RIGHT and self.rect.right < screen_width:
            if terrain[self.x + 1][self.y].isPassable():
                self.x += 1
                self.rect.move_ip(tile_width, 0)
