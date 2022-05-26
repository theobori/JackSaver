"""rotate tools"""

from typing import List

MIRRORS_SYMBOLS = {
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
                line[i] = MIRRORS_SYMBOLS[char]
            except KeyError:
                continue

        line = "".join(line)
        line = " " * spaces + line
        ret.append(line)

    return ret
