import pygame
import pygame.freetype
import sys
from abc import abstractmethod, ABC

from src.util.button import Button
from src.util.enums import TurnOwner, UserEvents, Color
from src.util.text_sprite import TextSurface


class GameCore(ABC):
    def __init__(self, title='game', screen_width=800, screen_height=600,
                 fps=60, turn_delay=60):

        # init display
        pygame.display.init()
        pygame.font.init()
        pygame.freetype.init()

        self.to_draw = []

        self.background = pygame.Surface((screen_width, screen_height))
        self.background.fill(Color.WHITE.value)
        pygame.display.set_caption(title)
        self.main_surface = pygame.display.set_mode(
            (screen_width, screen_height))

        self.global_stats_font = pygame.freetype.SysFont('comicsansmsttf', 20)
        self.local_stats_font = pygame.freetype.SysFont('comicsansmsttf', 15)

        # init sound
        pygame.mixer.pre_init(44100, 16, 2, 4096)

        # init clock
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.turn_delay = turn_delay
        self.turn_ticks = 0

        # init user-action handlers
        self.keyboard_handlers = {}

        # init game end flag
        self.game_over = False
        self.turn = TurnOwner.PLAYER_TURN

    @abstractmethod
    def process_player_action(self):
        pass

    @abstractmethod
    def do_ai_turn(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    def set_turn_ticks(self):
        self.turn_ticks = self.turn_delay

    def run(self):
        game_over_button_is_pressed = False

        def on_button_click():
            nonlocal game_over_button_is_pressed
            game_over_button_is_pressed = True

        game_over_button = Button("Game over!", width=100, height=50, command=on_button_click)
        game_over_button.rect.center = self.background.get_rect().center

        while not self.game_over or not game_over_button_is_pressed:
            if not self.game_over:
                if self.turn_ticks:
                    self.turn_ticks -= 1
                    pygame.event.clear(pygame.KEYDOWN)
                else:
                    if self.turn == TurnOwner.PLAYER_TURN:
                        self.turn = self.process_player_action()

                        if self.turn == TurnOwner.AI_TURN:
                            self.set_turn_ticks()
                    else:
                        self.do_ai_turn()
                        self.turn = TurnOwner.PLAYER_TURN
                        self.set_turn_ticks()

            self.draw()
            for x in self.to_draw:
                x.draw(self.main_surface)

            self.main_surface.blit(self.background, (0, 0))
            self.background.fill(Color.WHITE.value)
            pygame.display.update()
            self.clock.tick(self.fps)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == UserEvents.GAME_OVER:
                    self.game_over = True
                    self.to_draw.append(game_over_button)

                for x in self.to_draw:
                    x.handle_event(event)
