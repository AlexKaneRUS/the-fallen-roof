import pygame
from src.game_core import GameCore
from src.handlers.keyboard_handler import KeyboardHandler
from src.model.world_model import WorldModel
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
        self.keyboard_handler = KeyboardHandler(self)
        self.in_inventory = False

    def _init_graphic_repr(self):
        self.groups['terrain'] = pygame.sprite.Group()
        self.groups['player'] = pygame.sprite.GroupSingle()
        self.groups['mobs'] = pygame.sprite.Group()
        self.groups['items'] = pygame.sprite.Group()

    def process_player_action(self):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return TurnOwner.PLAYER_TURN
        if event.type == pygame.KEYDOWN:
            return self.keyboard_handler.handle(event.key)

        return TurnOwner.PLAYER_TURN

    def do_ai_turn(self):
        self.world_model.do_ai_turn()

    def draw(self):
        for group in self.groups.values():
            group.draw(self.main_surface)

    def open_inventory(self):
        self.in_inventory = True

        inv = self.world_model.player.Inventory(self.world_model.player,
            x=(self.background.get_width() - 500) / 2,
            y=(self.background.get_height() - 400) / 2, width=500, height=400)
        self.to_draw.append(inv)

    def close_inventory(self):
        self.in_inventory = False

        self.to_draw = list(filter(
            lambda x: not isinstance(x, self.world_model.player.Inventory),
            self.to_draw))
