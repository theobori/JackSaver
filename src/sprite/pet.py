"""pet module"""

import os
import random
from random import randrange

from src.sprite.sprite import NeedLoad, Sprite, Sprites, Side, Position

class Pet(Sprite):
    """
        Default object that represents a pet
    """

    def __init__(self, **kwargs: object):

        self.next_pos = Position(0, 0)

        self.level = NeedLoad(float)
        self.exp = NeedLoad(float)
        self.next_level_xp = NeedLoad(float)
        self.xp_per_second = NeedLoad(float)
        self.xp_earn_per_level = NeedLoad(float)
        self.move_range = NeedLoad(dict)
        super().__init__(**kwargs)

    def random_next_pos(self, rows: int, cols: int):
        """
            Get a new random pos where the pet must go
        """

        move_x = randrange(-1 * self.move_range["x"] + 1, self.move_range["x"] or 2)
        move_y = randrange(-1 * self.move_range["y"], self.move_range["y"] or 1)

        self.next_pos.x = self.pos.x + move_x
        self.next_pos.y = self.pos.y + move_y

        if self.next_pos.x < 0 or self.next_pos.x > (cols - self.size.w):
            self.next_pos.x = self.pos.x

        if self.next_pos.y < 0 or self.next_pos.y > (cols - self.size.w):
            self.next_pos.y = self.pos.y

    def load_random(self, dir_path: str = "./data/pets/"):
        """
            Loading a random pet
        """

        pets = os.listdir(dir_path)
        pets = list(filter(lambda name: name != "model.json", pets))
        filename = random.choice(pets)

        self.load_from_file(dir_path + filename)

    def move_to_ground(self, ground_y: int):
        """
            Overriding the Sprite method
            Place the sprite on the "ground", on the bottom of the screen
        """

        y_pet_pos = ground_y - self.size.h

        if self.pos.y == y_pet_pos:
            return

        self.pos.y = y_pet_pos
        self.next_pos.y = self.pos.y

    def keep_inside(self, cols: int):
        """
            Manage the terminal width
        """

        x_pos = cols - self.size.w
        pos_changed = True

        if self.pos.x >= x_pos:
            self.pos.x = x_pos
        elif self.pos.x < 0:
            self.pos.x = 0
        else:
            pos_changed = False

        if pos_changed:
            self.next_pos.x = self.pos.x

    def term_size_handling(self, rows: int, cols: int):
        """
            It keeps the pet inside the terminal box
        """

        self.move_to_ground(rows)
        self.keep_inside(cols)

    def update(self, stdscr: object):
        """
            Update the pet values
        """

        rows, cols = stdscr.getmaxyx()
        self.term_size_handling(rows, cols)

        if self.pos.x == self.next_pos.x:
            if self.pos.y == self.next_pos.y:
                self.random_next_pos(rows, cols)

        if self.pos.x < self.next_pos.x:
            if self.side == Side.LEFT:
                self.side = Side.RIGHT
                self.horizontal_rotate()
            self.pos.x += 1
        elif self.pos.x > self.next_pos.x:
            if self.side == Side.RIGHT:
                self.side = Side.LEFT
                self.horizontal_rotate()
            self.pos.x -= 1

        if self.pos.y < self.next_pos.y:
            self.pos.y += 1
        elif self.pos.y > self.next_pos.y:
            self.pos.y -= 1

class Pets(Sprites):
    """
        This objects manages a group of pets, its a kind of pool
    """

    def __init__(self, stdscr: object):
        super().__init__(stdscr)
