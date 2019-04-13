import pygame
from src.util.game_core import GameCore
from src.handlers.keyboard_handler import KeyboardHandler
from src.util.world_model import WorldModel
from src.util.enums import TurnOwner
import src.util.config as conf


class FallenRoof(GameCore):
    def __init__(self):
        super().__init__(title=conf.title,
                         screen_width=conf.screen_width,
                         screen_height=conf.screen_height,
                         fps=conf.fps,
                         turn_delay=conf.turn_delay)

        self._init_graphic_repr()
        self.world_model = WorldModel(self.groups)
        self.keyboard_handler = KeyboardHandler(self.world_model)

    def _init_graphic_repr(self):
        self.groups['terrain'] = pygame.sprite.Group()
        self.groups['player'] = pygame.sprite.GroupSingle()

    def process_player_action(self):
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return self.keyboard_handler.handle(event.key)
        return TurnOwner.PLAYER_TURN

    def do_ai_turn(self):
        pygame.event.pump()

    def draw(self):
        for group in self.groups.values():
            group.draw(self.main_surface)
