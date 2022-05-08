from typing import *

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
    ret = []
    max_size = len(max(content, key=len))

    for line in content:
        line = list(line[::-1])
        spaces = max_size - len(line)

        for i, c in enumerate(line):
            if (c in mirrors_symbols.keys()):
                line[i] = mirrors_symbols[c]

        line = "".join(line)
        line = " " * spaces + line
        ret += [line]
    
    return (ret)
