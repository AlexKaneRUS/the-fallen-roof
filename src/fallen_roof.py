import pygame
from src.game_core import GameCore
from src.handlers.keyboard_handler import KeyboardHandler
from src.model.characters.inventory import Inventory
from src.model.terrain.gen_terrain import gen_terrain
from src.model.terrain.read_terrain import read_terrain
from src.model.world_model import WorldModel
from src.util.enums import TurnOwner
import src.util.config as conf
import pickle
import os.path


class FallenRoof(GameCore):
    def __init__(self):
        super().__init__(title=conf.TITLE,
                         screen_width=conf.WIDTH_IN_TILES * conf.TILE_WIDTH,
                         screen_height=conf.HEIGHT_IN_TILES * conf.TILE_WIDTH,
                         fps=conf.FPS,
                         turn_delay=conf.TURN_DELAY)

        self.init_world_model()
        self.keyboard_handler = KeyboardHandler(
            lambda direction: self.world_model.move_player(direction, self.sprites),
            lambda: self.close_inventory() if self.in_inventory else self.open_inventory(),
        )
        self.in_inventory = False

    def process_player_action(self):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return TurnOwner.PLAYER_TURN
        if event.type == pygame.KEYDOWN:
            return self.keyboard_handler.handle(event.key)

        return TurnOwner.PLAYER_TURN

    def do_ai_turn(self):
        self.world_model.do_ai_turn(self.sprites)
        with open(conf.SAVE_FILE_PATH, "wb") as file:
            pickle.dump(self.world_model, file)

    def draw(self):
        self.sprites.draw(self.main_surface)

    def open_inventory(self):
        self.in_inventory = True

        def new_game_command():
            self.remove_save_file()
            self.init_world_model()
            self.close_inventory()

        inv = Inventory(
            self.world_model.player,
            x=(self.background.get_width() - 500) / 2,
            y=(self.background.get_height() - 400) / 2,
            width=500,
            height=400,
            new_game_command=new_game_command,
        )
        self.to_draw.append(inv)

    def close_inventory(self):
        self.in_inventory = False

        self.to_draw = list(filter(
            lambda x: not isinstance(x, Inventory),
            self.to_draw))

    def run(self):
        super().run()
        self.remove_save_file()

    def remove_save_file(self):
        if os.path.isfile(conf.SAVE_FILE_PATH):
            os.remove(conf.SAVE_FILE_PATH)

    def init_world_model(self):
        if os.path.isfile(conf.SAVE_FILE_PATH):
            with open(conf.SAVE_FILE_PATH, "rb") as file:
                self.world_model = pickle.load(file)
        else:
            self.world_model = WorldModel.generate(read_terrain("map.XY") or gen_terrain())
        # init graphic representation
        self.sprites = self.world_model.build_sprites()
