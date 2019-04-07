import pygame
from abc import abstractmethod, ABC
from collections import defaultdict

class GameCore(ABC):
    def __init__(self, title='game', screen_width=800, screen_height=600, fps=60):
        # init pygame
        pygame.init()

        # init display
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

        # init user-action handlers
        self.keyboard_handlers = {}

        # init game end flag
        self.game_over = False

    @abstractmethod
    def process_events(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    def run(self):
        while not self.game_over:
            self.main_surface.blit(self.background, (0, 0))

            self.process_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.fps)
