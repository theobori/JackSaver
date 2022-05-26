"""sprite module"""

from typing import Any
from dataclasses import dataclass
from enum import Enum

import json
import uuid
import threading
import curses

from src.sprite.rotate import horizontal_symetry
from src.exceptions.exception import JackError
from src.utils.clock import Clock

@dataclass
class Position:
    """
        It represents a location
    """

    x: int
    y: int

@dataclass
class Size:
    """
        It represents a size
    """

    w: int
    h: int

class Side(Enum):
    """
        Contains every possible side for a sprite
    """

    LEFT = 0
    RIGHT = 1

class NeedLoad:
    """
        This object is used to assign a value loaded from a file to a variable
    """

    def __init__(self, _type: type, value: Any = None):
        self.type = _type
        self.default = value

    def __repr__(self) -> str:
        return self.__class__.__name__

    def gettype(self) -> type:
        """
            Returns the needed type
        """

        return self.type

class BaseDrawable:
    """
        Common sprite data
    """

    def __init__(self, data: dict = None, path: str = None):
        self.id = uuid.uuid4()
        self.pos = Position(0, 0)
        self.size = Size(0, 0)

        self.content = NeedLoad(list)

        if data:
            self.load(data)
        elif path:
            self.load_from_file(path)

    def load(self, data: json):
        """
            Load properties by setting up attributes the class
        """

        for attr in self.__dict__:
            value = self.__getattribute__(attr)
            attr_value = None

            if not isinstance(value, NeedLoad):
                continue

            if not attr in data.keys():
                if value.default is None:
                    raise JackError(f"Missing attribute: {attr}")
                attr_value = value.default
            else:
                attr_value = data[attr]

            if value.gettype() != type(attr_value):
                raise JackError(f"Wrong type for {attr}")

            self.__setattr__(attr, attr_value)

        self.init_size()

    def load_from_file(self, filepath: str):
        """
            It will assign the class properties with ones in templates file
            example: (./data/pets/model.json)
        """

        data = {}

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.load(data)

    def set_pos(self, x: int, y: int):
        """
            Update the position
        """

        self.pos.x = x
        self.pos.y = y

    def init_size(self):
        """
            Initialize the size of the content
        """

        self.size.h = len(self.content)
        self.size.w = len(max(self.content, key=len))

class Sprite(BaseDrawable):
    """
        This object details a sprite
    """

    def __init__(self, **kwargs: object):
        self.side = Side.LEFT

        self.name = NeedLoad(str)
        self.color = NeedLoad(int)
        self.on_ground = NeedLoad(bool, False)
        super().__init__(**kwargs)

    def horizontal_rotate(self):
        """
            It makes a horizontal symetry with the sprite
        """

        self.content = horizontal_symetry(self.content)

    def move(self, x: int, y: int):
        """
            It moves the sprite with the vector (x, y)
        """

        self.pos.x += x
        self.pos.y += y

    def move_to_ground(self, rows: int):
        """
            Place the sprite on the "ground", on the bottom of the screen
        """

        y_ground_pos = rows - self.size.h

        if self.pos.y == y_ground_pos:
            return

        self.pos.y = y_ground_pos

    def update(self, stdscr: object):
        """
            Update the sprite values
        """

        rows, cols = stdscr.getmaxyx()

        if self.on_ground:
            self.move_to_ground(rows)

    def draw(self, stdscr: object):
        """
            Drawing the sprite to stdscr
        """

        for y, line in enumerate(self.content):
            for x, char in enumerate(line):
                if char in (" ", "\t"):
                    continue
                try:
                    stdscr.addstr(
                        self.pos.y + y,
                        self.pos.x + x,
                        char,
                        curses.color_pair(self.color)
                    )
                except Exception:
                    continue

    def run(self, stdscr: object):
        """
            It's just a model, it will be override anyway
        """

        self.update(stdscr)
        self.draw(stdscr)

class Sprites(threading.Thread):
    """
        This object groups and manipulates sprites
    """

    def __init__(self, stdscr: object):
        threading.Thread.__init__(self, target=self.run)

        self.objs = []
        self.stdscr = stdscr
        self.clock = Clock(0.5)

    def add(self, sprite: Sprite):
        """
            Append a sprite to the group
        """

        self.objs.append(sprite)

    def run(self):
        """
            This method will be call in the main loop every k seconds
        """

        [sprite.run(self.stdscr) for sprite in self.objs]
