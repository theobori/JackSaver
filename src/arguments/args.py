from argparse import ArgumentParser

from sys import stderr, exit

class Parser(ArgumentParser):

    def __init__(self) -> None:
        super().__init__()
        self.init_args()

    def error(self, message):
        """
            Override error from ArgumentParser
            It exit the program and print an error message on stderr
        """

        stderr.write(f"error: {message}\n")
        self.print_help()
        exit(84)

    def init_args(self):
        """

        """

        self.add_argument(
            "-c", "--count",
            type=int, default=5,
            help="Amount of thread"
        )
        self.add_argument(
            "-x", "--sprite_per_thread",
            type=int, default=4,
            help="Amount of sprite managed by a single thread"
        )