"""JackSaver module"""

import curses
import threading
from sys import stderr
from src.sprite.pet import Pet, Pets

from src.sprite.sprite import Sprites
from src.arguments.args import Parser
from src.exceptions.exception import JackError

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

        for amount in range(0, self.args.count, self.args.sprite_per_thread):
            tmp_pets = Pets(self.stdscr)

            if (self.args.count - amount > self.args.sprite_per_thread):
                _max = self.args.sprite_per_thread
            else:
                _max = self.args.count - amount

            for _ in range(_max):
                pet = Pet()
                pet.load_random()
                tmp_pets.add(pet)
            self.sprites_groups += [tmp_pets]

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

        while 1:
            pass

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
    try:
        jack_saver = JackSaver(stdscr, args)
        jack_saver.run()
    except JackError as error:
        print(error, file=stderr)


if __name__ == "__main__":
    parser = Parser()
    args = parser.parse_args()

    curses.wrapper(main)
