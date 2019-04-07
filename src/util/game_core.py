import pygame
from abc import abstractmethod, ABC
from collections import defaultdict

class GameCore(ABC):
    def __init__(self, title='game', screen_width=800, screen_height=600, fps=60):
        # init pygame
        pygame.init()

        # init display
        pygame.display.set_caption(title)
        pygame.font.init()
        self.main_surface = pygame.display.set_mode((screen_width, screen_height))

        # init graphic representation
        self.groups = []

        # init sound
        pygame.mixer.pre_init(44100, 16, 2, 4096)

        # init clock
        self.fps = fps
        self.clock = pygame.time.Clock()

        # init user-action handlers
        self.keyboard_handlers = defaultdict(list)

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
            self.process_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.fps)
