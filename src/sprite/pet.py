"""pet module"""

import os
import random
from random import randrange

from src.sprite.sprite import NeedLoad, Sprite, Sprites, Side

class Pet(Sprite):
    """
        Default object that represents a pet
    """

    def __init__(self):
        super().__init__()

        self.next_pos = self.pos

        self.level = NeedLoad(float)
        self.exp = NeedLoad(float)
        self.next_level_xp = NeedLoad(float)
        self.xp_per_second = NeedLoad(float)
        self.xp_earn_per_level = NeedLoad(float)
        self.move_range = NeedLoad(dict)

    def random_next_pos(self, stdscr: object):
        """
            Get a new random pos where the pet must go
        """

        rows, cols = stdscr.getmaxyx()
        move_x = randrange(-1 * self.move_range["x"], self.move_range["x"] or 1)
        move_y = randrange(-1 * self.move_range["y"], self.move_range["y"] or 1)

        self.next_pos.x = (self.pos.x + move_x) % cols
        self.next_pos.y = (self.pos.y + move_y) % rows

    def load_random(self, dir_path: str="./data/pets/"):
        """
            Loading a random pet
        """

        pets = os.listdir(dir_path)
        pets = list(filter(lambda name: name != "model.json", pets))
        filename = random.choice(pets)

        self.load_from_file(dir_path + filename)
    
    def update(self, stdscr: object):
        """
            Update the pet values
        """

        if (self.pos.x == self.next_pos.x):
            if (self.pos.y == self.next_pos.y):
                self.random_next_pos(stdscr)
        
        if (self.pos.x < self.next_pos.x):
            if (self.side == Side.LEFT):
                self.side = Side.RIGHT
                self.horizontal_rotate()
            self.pos.x += self.move_range["x"]
        else:
            if (self.side == Side.RIGHT):
                self.side = Side.LEFT
                self.horizontal_rotate()
            self.pos.x -= self.move_range["x"]

        if (self.pos.y < self.next_pos.y):
            self.pos.y += self.move_range["y"]
        else:
            self.pos.y -= self.move_range["y"]

    def run(self, stdscr: object):
        """
            Pet main function, overriding the run method from Sprite class
        """

        self.update(stdscr)
        self.draw(stdscr)

class Pets(Sprites):
    """
        This objects manages a group of pets, its a kind of pool
    """

    def __init__(self, stdscr: object):
        super().__init__(stdscr)

    # # remove ?
    # def run(self):
    #     """
    #         Overriding the class Sprites method
    #     """

    #     while 1:
    #         if (not self.clock.check()):
    #             continue

            

    #         for sprite in self.objs:
    #             sprite.run(self.stdscr)

    #         self.stdscr.refresh()
