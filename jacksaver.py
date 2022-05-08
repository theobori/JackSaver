"""JackSaver module"""

import curses
from src.sprite.pet import Pet

from src.sprite.sprite import Sprites
from src.arguments.args import Parser

class JackSaver:
    """
        This object contains every main functions for the screen saver
    """

    def __init__(self, stdscr: object, cli_args: object):
        self.stdscr = stdscr
        self.args = cli_args
        self.sprites_groups = []

        self.check_args()
        self.init_sprites()

    def check_args(self):
        """
            TODO
        """

    def init_sprites(self):
        """
            Generating sprites (Sprites) groups aka threads
        """

        for _ in range(self.args.count):
            tmp_sprites = Sprites(self.stdscr)
            for _ in range(self.args.sprite_per_thread):
                sprite = Pet()
                sprite.load_random()
                tmp_sprites.add(sprite)
            self.sprites_groups += [tmp_sprites]

    def run(self):
        """
            Main function for the screen saver
        """

        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        self.stdscr.clear()
        self.stdscr.refresh()

        self.start_threads()

    def start_threads(self):
        """
            Call the method start from every thread
            It will executes it
        """

        for thread in self.sprites_groups:
            thread.start()

def main(stdscr: object):
    """
        Program main function
    """

    jack_saver = JackSaver(stdscr, args)
    jack_saver.run()

if __name__ == "__main__":
    parser = Parser()
    args = parser.parse_args()

    curses.wrapper(main)
