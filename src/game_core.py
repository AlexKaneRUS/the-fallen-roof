import pygame
import sys
from abc import abstractmethod, ABC
from src.util.enums import TurnOwner, UserEvents


class GameCore(ABC):
    def __init__(self, title='game', screen_width=800, screen_height=600, fps=60, turn_delay=60):

        # init display
        pygame.display.init()
        self.background = pygame.Surface((screen_width, screen_height))
        self.background.fill((0, 0, 0))
        pygame.display.set_caption(title)
        self.main_surface = pygame.display.set_mode((screen_width, screen_height))

        # init graphic representation
        self.groups = {}

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

    def process_global_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == UserEvents.GAME_OVER:
                self.game_over = True


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
        while not self.game_over:
            pygame.time.wait(0)
            self.main_surface.blit(self.background, (0, 0))

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

            pygame.display.update()
            self.clock.tick(self.fps)

            self.process_global_events()
