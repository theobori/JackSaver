"""JackSaver main file"""

import curses
import os
import signal
from sys import stderr, exit
from datetime import datetime

from src.sprite.pet import Pet
from src.sprite.sprite import Position, Size, Sprites, Sprite
from src.arguments.args import Parser, parse_cli_scheme
from src.exceptions.exception import JackError
from src.utils.repeat import RepeatFunc
from src.hotkeys.binds import Binds
from src.sprite.box import Boxes, Box

class JackSaver(Binds):
    """
        This object contains every main functions for the screen saver
    """

    def __init__(self, stdscr: object, cli_args: object):
        super().__init__()

        self.stdscr = stdscr
        self.args = cli_args
        self.drawables_groups = []
        self.drawables = {}
        self.boxes = Boxes()
        self.loop_func = None

        self.init()

    def init_colors():
        """
            Generating pair colors
        """

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    def init_binds(self):
        """
            Adding key binds to the Binds class
        """

        self.add_bind("q", self.leave)
        self.add_bind("c", self.boxes.switch_selected)
        self.add_bind("d", self.boxes.move_selected, self.stdscr, 1, 0)
        self.add_bind("a", self.boxes.move_selected, self.stdscr, -1, 0)
        self.add_bind("w", self.boxes.move_selected, self.stdscr, 0, -1)
        self.add_bind("s", self.boxes.move_selected, self.stdscr, 0, 1)
        self.add_bind("r", self.boxes.reset_selected)
        self.add_bind("n", self.boxes.select_next)

    def init_sprites(self):
        """
            Generating additional sprites (Sprite) (not pets)
        """

        rows, _ = self.stdscr.getmaxyx()

        # Trees
        for x in range(0, 81, 40):
            tree = Sprite(path="./data/sprites/palm_tree.json")
            tree.move_to_ground(rows)
            tree.set_pos(x, 0)
            self.drawables[f"tree_{x}"] = tree

        # Clouds
        for x in range(20, 80, 40):
            cloud = Sprite(path="./data/sprites/cloud_1.json")
            cloud.move_to_ground(rows)
            cloud.set_pos(x, 0)
            self.drawables[f"cloud_{x}"] = cloud
    
    def init_boxes(self):
        """
            Generating the text boxes
        """

        clock = Box("clock", self.stdscr, Position(0, 0), Size(9, 2))
        self.boxes.add(clock)

        version = Box("version", self.stdscr, Position(0, 3), Size(6, 2), "v 0.1")
        self.boxes.add(version)

    def load_scheme(self, pets_path: str = "./data/pets/"):
        """
            Load a pet scheme from cli arg
        """

        scheme = parse_cli_scheme(self.args.schema)
        available_pets = os.listdir(pets_path)
        inc = 0

        for name, amount in scheme.items():
            name += ".json"
            for _ in range(amount):
                full_path = pets_path + name

                if not name in available_pets:
                    raise JackError(f"Wrong pet name, check {full_path}")

                pet = Pet(path=full_path)
                self.drawables[f"pet_{inc}"] = pet
                inc += 1

    def init_pets(self):
        """
            Generating pets object
        """

        if self.args.schema:
            self.load_scheme()
            return

        for pet_count in range(self.args.count):
            pet = Pet()
            pet.load_random()
            self.drawables[f"pet_{pet_count}"] = pet

    def init_drawables(self):
        """
            Generating every drawable object
        """

        pet_in = 0
        sprites = Sprites(self.stdscr)

        self.init_sprites()
        self.init_pets()

        for name, drawable in self.drawables.items():
            if pet_in >= self.args.sprite_per_thread:
                self.drawables_groups.append(sprites)
                sprites = Sprites(self.stdscr)
                pet_in = 0
            sprites.add(drawable)
            pet_in += 1

        if not self.drawables_groups or not self.drawables_groups[-1] is sprites:
            self.drawables_groups.append(sprites)

    def init(self):
        """
            Calling initializers
        """

        self.init_boxes()
        self.init_drawables()
        self.init_binds()
        JackSaver.init_colors()

    def update(self):
        """
            Update stuff in the main thread,
            like the boxes, etc...
        """

        _time = str(datetime.now())[11:-7]

        self.boxes["clock"].setContent(_time)

    def loop(self):
        """
            Function called every n seconds
        """

        self.stdscr.clear()

        self.update()
        for drawable_group in self.drawables_groups:
            drawable_group.draw()
        self.boxes.run()

        self.stdscr.refresh()

    def run(self, n: int = 0.1):
        """
            Main function for the screen saver
        """

        curses.nocbreak()
        curses.noecho()
        curses.raw()
        curses.curs_set(0)
        self.stdscr.keypad(False)
        curses.echo()

        self.run_threads()
        self.loop_func = RepeatFunc(n, self.loop)

        while 1:
            key = self.stdscr.getkey()
            self.try_call_from_bind(key)

            if key == "q":
                exit()

    def leave(self):
        """
            Kill process
        """

        self.loop_func.stop()
        for x in self.drawables_groups:
            x._stop()

    def run_threads(self):
        """
            Call the method start from every thread
            It will executes it
        """

        for thread in self.drawables_groups:
            thread.start()

def main(stdscr: object):
    """
        Program main function
    """

    try:
        jack_saver = JackSaver(stdscr, args)
        jack_saver.run(0.08)
    except JackError as error:
        print(error, file=stderr)

if __name__ == "__main__":
    parser = Parser()
    args = parser.parse_args()

    curses.wrapper(main)
