import pygame
import sys
from abc import abstractmethod, ABC
from src.util.enums import TurnOwner, UserEvents

class GameCore(ABC):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    class Button():
        def __init__(self, text, x=0, y=0, width=100, height=50, command=None):
            self.text = text
            self.command = command

            self.image_normal = pygame.Surface((width, height))
            self.image_normal.fill(GameCore.RED)

            self.image_hovered = pygame.Surface((width, height))
            self.image_hovered.fill(GameCore.BLUE)

            self.image = self.image_normal
            self.rect = self.image.get_rect()

            font = pygame.font.SysFont('comicsansmsttf', 15)

            text_image = font.render(text, True, GameCore.WHITE)
            text_rect = text_image.get_rect(center=self.rect.center)

            self.image_normal.blit(text_image, text_rect)
            self.image_hovered.blit(text_image, text_rect)

            # you can't use it before `blit`
            self.rect.topleft = (x, y)

            self.hovered = False
            # self.clicked = False

        def update(self):
            if self.hovered:
                self.image = self.image_hovered
            else:
                self.image = self.image_normal

        def draw(self, surface):
            surface.blit(self.image, self.rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEMOTION:
                self.hovered = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    print('Clicked:', self.text)
                    if self.command:
                        self.command()

    def __init__(self, title='game', screen_width=800, screen_height=600, fps=60, turn_delay=60):

        # init display
        pygame.display.init()
        pygame.font.init()
        self.background = pygame.Surface((screen_width, screen_height))
        self.background.fill(GameCore.BLACK)
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
        button_pressed = False
        def on_button_click():
            nonlocal button_pressed
            button_pressed = True
        game_over_button = GameCore.Button(
            "Game over!",
            x=(self.background.get_width() - 100) / 2,
            y=(self.background.get_height() - 50) / 2,
            width=100,
            height=50,
            command=on_button_click
        )
        while not self.game_over or not button_pressed:
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
            if self.game_over:
                game_over_button.draw(self.main_surface)

            pygame.display.update()
            self.clock.tick(self.fps)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == UserEvents.GAME_OVER:
                    self.game_over = True
                game_over_button.handle_event(event)
