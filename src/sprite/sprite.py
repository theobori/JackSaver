"""sprite module"""

from dataclasses import dataclass
from enum import Enum
from time import sleep
import json
import uuid
import threading

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
    LEFT = 0
    RIGHT = 1

class NeedLoad:
    """
        This object is used to assign a value loaded from a file to a variable
    """

    def __init__(self, __type: type):
        self.type = __type

    def __repr__(self) -> str:
        return self.__class__.__name__

    def gettype(self) -> type:
        """
            Returns the needed type
        """

        return self.type

class Sprite:
    """
        This object details a sprite
    """

    left = True
    right = False

    def __init__(self):
        self.id = uuid.uuid4()
        self.pos = Position(0, 0)
        self.size = Size(0, 0)
        self.side = Side.LEFT

        self.name = NeedLoad(str)
        self.content = NeedLoad(list)
        self.color = NeedLoad(int)

    def load(self, data: json):
        """
            Load properties by setting up attributes the class
        """
        for attr in self.__dict__:
            value = self.__getattribute__(attr)

            if type(value) != NeedLoad:
                continue

            if not attr in data.keys():
                raise JackError(f"Missing attribute: {attr}")
            if value.gettype() != type(data[attr]):
                raise JackError(f"Wrong type: {attr}")
            self.__setattr__(attr, data[attr])

    def load_from_file(self, filepath: str):
        """
            It will assign the class properties with ones in templates file
            example: (./data/pets/model.json)
        """
        data = {}

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.load(data)

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

    def update(self, stdscr: object):
        """
            Update the sprite values
        """

        pass

    def draw(self, stdscr: object):
        """
            Drawing the sprite to stdscr
        """

        for y, line in enumerate(self.content):
            for x, char in enumerate(line):
                if (char in (" ", "\t")):
                    continue
                try:
                    stdscr.addstr(self.pos.y + y, self.pos.x + x, char)
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
        threading.Thread.__init__(self, target = self.run, args=(stdscr, ))

        self.objs = []
        self.stdscr = stdscr
        self.clock = Clock(0.5)

    def add(self, sprite: Sprite):
        """
            Append a sprite to the group
        """

        self.objs += [sprite]

    def run(self):
        """
            This method will be call in the main loop every k seconds
        """

        while 1:
            sleep(0.5)

            self.stdscr.clear()

            for sprite in self.objs:
                sprite.run(self.stdscr)

            self.stdscr.refresh()
