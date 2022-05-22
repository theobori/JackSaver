"""rotate module"""

from typing import List

mirrors_symbols = {
    "\\":"/",
    "/":"\\",
    "(":")",
    ")":"(",
    "{":"}",
    "}":"{",
    "<":">",
    ">":"<",
    "'":"`",
    "`":"'"
}

def horizontal_symetry(content: List[str]) -> List[str]:
    """
        Rotate a sprite horizontaly (ascii art)
    """

    ret = []
    max_size = len(max(content, key=len))

    for line in content:
        line = list(line[::-1])
        spaces = max_size - len(line)

        for i, char in enumerate(line):
            try:
                line[i] = mirrors_symbols[char]
            except KeyError:
                continue

        line = "".join(line)
        line = " " * spaces + line
        ret += [line]

    return ret
