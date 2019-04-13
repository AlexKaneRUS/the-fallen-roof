import pygame
import sys

from src.util.game_core import GameCore
from src.util.game_core import UserEvents
from src.util.world_model import WorldModel
import src.util.config as conf


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
        self.groups['terrain'] = pygame.sprite.Group()
        self.groups['player'] = pygame.sprite.GroupSingle()

    def process_player_action(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            self.world_model.handle_key(event.key)
            pygame.event.clear(pygame.KEYDOWN)
            return False
        return True

    def do_ai_turn(self):
        pygame.event.pump()

    def update(self):
        pass

    def draw(self):
        for group in self.groups.values():
            group.draw(self.main_surface)