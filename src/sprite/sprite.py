"""sprite module"""

from dataclasses import dataclass
import json
import uuid
import threading

from src.sprite.rotate import horizontal_symetry
from src.exceptions.exception import SpriteError

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

    def __init__(self):
        self.id = uuid.uuid4()
        self.pos = Position(0, 0)
        self.size = Size(0, 0)

        self.name = NeedLoad(str)
        self.content = NeedLoad(list)
        self.color = NeedLoad(int)

    def load_from_file(self, filepath: str):
        """
            It will assign the class properties with ones in templates file
            example: (./data/pets/model.json)
        """

        data = {}

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for attr in self.__dict__:
            value = self.__getattribute__(attr)

            if isinstance(value) != NeedLoad:
                continue

            if not attr in data.keys():
                raise SpriteError(f"Missing attribute: {attr} in {filepath}")
            if value.gettype() != type(data[attr]):
                raise SpriteError(f"Wrong type: {attr} in {filepath}")
            self.__setattr__(attr, data[attr])

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

    def run(self):
        """
            It's just a model, it will be override anyway
        """

class Sprites(threading.Thread):
    """
        This object groups and manipulates sprites
    """

    def __init__(self, stdscr: object):
        threading.Thread.__init__(self, target = self.run, args=(stdscr, ))

        self.sprites = []
        self.stdscr = stdscr

    def add(self, sprite: Sprite):
        """
            Append a sprite to the group
        """

        self.sprites += [sprite]

    def run(self):
        """
            This method will be call in the main loop every k seconds
        """
