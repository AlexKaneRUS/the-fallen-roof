import pygame
import sys
from collections import defaultdict

from src.util.game_core import GameCore
from src.util.world_model import WorldModel
import src.util.config as conf

from src.characters.player import Player


class FallenRoof(GameCore):
    def __init__(self):
        super().__init__(title=conf.title,
                         screen_width=conf.screen_width,
                         screen_height=conf.screen_height,
                         fps=conf.fps)

        self._init_keyboard_handlers()
        self._init_graphic_repr()

        self.world_model = WorldModel(self.groups)

    def _init_keyboard_handlers(self):
        pass

    def _init_graphic_repr(self):
        #self.groups['terrain'] = pygame.sprite.Group()
        self.groups['player'] = pygame.sprite.GroupSingle()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.world_model.handle_key(event.key)

    def update(self):
        pass

    def draw(self):
        for group in self.groups.values():
            group.draw(self.main_surface)