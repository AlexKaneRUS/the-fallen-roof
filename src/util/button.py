import pygame

from src.util.enums import Color


class Button:
    def __init__(self, text, x=0, y=0, width=100, height=50, command=None,
                 image_over=None, toggled=False):
        self.toggled = toggled
        self.text = text
        self.command = command

        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill(Color.RED.value)

        self.image_toggled = pygame.Surface((width, height))
        self.image_toggled.fill(Color.YELLOW.value)

        self.images = [self.image_normal, self.image_toggled]

        self.image = None
        if self.toggled:
            self.image = self.image_toggled
        else:
            self.image = self.image_normal
        self.rect = self.image.get_rect()

        font = pygame.font.SysFont('comicsansmsttf', 15)

        text_image = font.render(text, True, Color.WHITE.value)
        text_rect = text_image.get_rect(center=self.rect.center)

        for image in self.images:
            image.blit(text_image, text_rect)

        if image_over is not None:
            image_size = min(height - 1, text_rect.topleft[0])
            image_over = pygame.transform.scale(image_over,
                                                (image_size, image_size))

            for image in self.images:
                image.blit(image_over, image_over.get_rect())

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print('Clicked:', self.text)
                if self.command:
                    self.command()
                self.toggled = not self.toggled
