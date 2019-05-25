from abc import ABC, abstractmethod

import pygame

from src.model.characters import has_battle_system
from src.model.characters.has_battle_system import HasBattleSystem
from src.model.items.item import Item
from src.util.button import Button
from src.util.enums import Color, UserEvents
from copy import deepcopy


class HasInventory(ABC, HasBattleSystem):
    def __init__(self, health, strength):
        HasBattleSystem.__init__(self, health, strength)

        self.items = {}
        self.equipped_items = []

    def pickup_item(self, item: Item):
        item.x = None
        item.y = None

        self.items[len(self.items)] = item

        self.on_pickup()

    @abstractmethod
    def on_pickup(self):
        pass

    def equip_item(self, i):
        if i not in self.equipped_items:
            self.equipped_items.append(i)

            self.health += self.items[i].health_buff
            self.strength += self.items[i].strength_buff

    def unequip_item(self, i):
        if i in self.equipped_items:
            self.equipped_items.remove(i)

            self.health -= self.items[i].health_buff
            self.strength -= self.items[i].strength_buff

    class Inventory:
        def __init__(self, player, x=0, y=0, width=300, height=200, new_game_command=None):
            self.player = player

            self.image = None
            self.rect = None
            self.items = []
            self.text_rect = None

            self.reinit(x, y, width, height, new_game_command)

        class Command:
            def __init__(self, j, inv, new_game_command):
                self.j = j
                self.inv = inv
                self.new_game_command = new_game_command

            def __call__(self):
                if self.j in self.inv.player.equipped_items:
                    self.inv.player.unequip_item(self.j)
                else:
                    self.inv.player.equip_item(self.j)
                self.inv.reinit(self.inv.rect.topleft[0], self.inv.rect.topleft[1], self.inv.rect.width,
                                self.inv.rect.height, self.new_game_command)
                pygame.event.post(pygame.event.Event(UserEvents.EMPTY, {}))

        def _draw_items(self, bot_left_txt, new_game_command):
            bot_left_x, bot_left_y = bot_left_txt
            n = len(self.player.items)

            if n == 0:
                return

            item_height = min(int((self.rect.midbottom[1] - bot_left_y) / n),
                              50)
            item_width = 325

            for i, item in self.player.items.items():
                item_text = '{}: health +{}, strength +{}'.format(item.name,
                                                                  item.health_buff,
                                                                  item.strength_buff)
                button = Button(item_text,
                                width=item_width, height=item_height - 1,
                                command=self.Command(i, self, new_game_command),
                                image_over=item.generate_image(), toggled=i in self.player.equipped_items)
                button.rect.topleft = bot_left_txt
                button.rect.top += 1
                bot_left_txt = button.rect.bottomleft
                button.rect = button.image.get_rect(
                    midtop=(self.rect.midtop[0], button.rect.midtop[1]))

                self.image.blit(button.image, button.rect)
                self.items.append(button)

        def update_stat(self):
            health_strength_level = 'Health: {} Strength: {} Level: {} Experience: {}/{}'.format(
                self.player.health, self.player.strength, self.player.level,
                self.player.experience, self.player.next_level)

            font_stats = pygame.font.SysFont('comicsansmsttf', 19)
            health_strength_level_image = font_stats.render(
                health_strength_level, True,
                Color.BLACK.value)

            health_strength_level_rect = health_strength_level_image.get_rect(
                midbottom=(
                    self.text_rect.midbottom[0],
                    self.text_rect.midbottom[1] + 20))

            self.image.blit(health_strength_level_image,
                            health_strength_level_rect)

            return health_strength_level_rect.bottomleft

        def reinit(self, x, y, width, height, new_game_command):
            self.image = pygame.Surface((width, height))
            self.image.fill(Color.GREY.value)
            self.rect = self.image.get_rect()

            font = pygame.font.SysFont('comicsansmsttf', 29)

            text_image = font.render('Inventory', True, Color.BLACK.value)
            self.text_rect = text_image.get_rect(midtop=self.rect.midtop)
            self.image.blit(text_image, self.text_rect)

            self.new_game_button = Button("New game", width=80, height=30, command=new_game_command)
            self.new_game_button.rect.topright = self.rect.topright
            self.image.blit(self.new_game_button.image, self.new_game_button.rect)

            prev_bot = self.update_stat()

            self.items = []
            self._draw_items(prev_bot, new_game_command)

            self.rect = self.image.get_rect(topleft=(x, y))

        def update(self):
            pass

        def draw(self, surface):
            surface.blit(self.image, self.rect)

        def handle_event(self, event):
            if hasattr(event, 'pos'):
                event.pos = (event.pos[0] - self.rect.topleft[0],
                             event.pos[1] - self.rect.topleft[1])

            for item in self.items:
                item.handle_event(event)

            self.new_game_button.handle_event(event)
