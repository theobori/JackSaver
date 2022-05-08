from src.sprite.sprite import NeedLoad, Sprite, Sprites, Position

import os, random

class Pet(Sprite):
    """
        Default object that represents a pet
    """

    def __init__(self):
        super().__init__()

        self.next_position = self.pos

        self.health = NeedLoad(float)
        self.damage = NeedLoad(float)
        self.level = NeedLoad(float)
        self.exp = NeedLoad(float)
        self.next_level_xp = NeedLoad(float)
        self.xp_per_second = NeedLoad(float)
        self.xp_earn_per_level = NeedLoad(float)
    
    def load_random(self, dir_path: str="./data/pets/"):
        pets = os.listdir(dir_path)
        filename = random.choice(pets)

        self.load_from_file(dir_path + filename)

class Pets(Sprites):
    """
        This objects manages a group of pets, its a kind of pool
    """

    def __init__(self, stdscr: object):
        super().__init__(stdscr)
    
    def run(self):
        pass