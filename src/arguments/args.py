"""args parsing"""

from argparse import ArgumentParser
from sys import stderr, exit
import re

SCHEME_REGEX = re.compile(r"(^[^\(]+)\(([\d+^\)]+)\)")

class Parser(ArgumentParser):
    """
        This class manages the command line argument
    """

    def __init__(self) -> None:
        super().__init__()
        self.init_args()

    def error(self, message):
        """
            Override error from ArgumentParser
            It exit the program and print an error message on stderr
        """

        print(f"error: {message}\n", file=stderr)
        self.print_help()
        exit(84)

    def init_args(self):
        """
            Add needed arguments to ArgumentParser
        """

        self.add_argument(
            "-c", "--count",
            type=int, default=5,
            help="Amount of pet"
        )
        self.add_argument(
            "-x", "--sprite_per_thread",
            type=int, default=4,
            help="Amount of sprite managed by a single thread"
        )
        self.add_argument(
            "-s", "--schema",
            type=str, default="",
            help="Schema that describe which pet will spawn"
        )


def parse_cli_scheme(data: str) -> dict:
    """
        Parse the command line argument
        and generate a dict
    """

    schemes = data.split(" ")
    ret = {}

    for scheme in schemes:
        scheme = SCHEME_REGEX.findall(scheme)

        if not scheme:
            continue

        name, amount = scheme[0]
        amount = int(amount)

        if not name in ret.keys():
            ret[name] = amount
        else:
            ret[name] += amount

    return ret
