"""text box module"""

from curses.textpad import rectangle
from sys import stderr
from typing import Union, Any

from src.sprite.sprite import Position, Size, MinimalObject

class Box(MinimalObject):
    """
        This object represents a curses box that can contains text
        It can be selected, hidden and you can even move it
    """

    def __init__(
            self,
            name: str,
            stdscr: object,
            pos: Position,
            size: Size,
            content: list = []
        ):
        super().__init__(pos.x, pos.y, size.w, size.h)

        self.name = name
        self.stdscr = stdscr
 
        self.hidden = False
        self.selected = False

        if not content:
            self.content = content
        else:
            self.setContent(content)

    def switch(self):
        """
            Switch hidden status
        """

        self.hidden ^= True
    
    def select(self):
        """
            Select the box
        """

        self.selected = True
    
    def unselect(self):
        """
            Unselect the box
        """

        self.selected = False

    def move(self, stdscr: object, x: int, y: int):
        """
            Move the box and it content
        """

        rows, cols = stdscr.getmaxyx()
        new_x = self.pos.x + x
        new_y = self.pos.y + y

        if new_x < 0 or new_x + self.size.w >= cols:
            return
        if new_y < 0 or new_y + self.size.h >= rows:
            return

        self.pos.x = new_x
        self.pos.y = new_y

    def setContent(self, content: str):
        """
            Update values
        """

        self.content = []

        for row in range(0, (self.size.w - 1) * (self.size.h - 1), self.size.w - 1):
            line = content[row:row + self.size.w - 1]
            self.content.append(line)

    def run(self):
        """
            Draw rectangle with his content inside to the screen
        """

        if self.hidden:
            return

        rectangle(
            self.stdscr,
            self.pos.y, self.pos.x,
            self.pos.y + self.size.h, self.pos.x + self.size.w
        )
        for y, line in enumerate(self.content):
            self.stdscr.addstr(self.pos.y + y + 1 , self.pos.x + 1, line)
        
        if not self.selected:
            return

        self.stdscr.addstr(self.pos.y, self.pos.x, "S")

class Boxes:
    """
        This class manages multiple Box
    """

    def __init__(self):
        self.boxes = {}
        self.selected = None
    
    def __getitem__(self, key: Any) -> Union[Box, None]:
        if not key in self.boxes.keys():
            return None

        return self.boxes[key]
    
    def add(self, box: Box):
        """
            Append a box to the dict
        """

        if not self.selected:
            box.select()
            self.selected = box

        self.boxes[box.name] = box

    def run(self):
        """
            Drawing every box at the screen
        """

        for _, box in self.boxes.items():
            try:
                box.run()
            except:
                continue

    def move_selected(self, stdscr: object, x: int, y: int):
        """
            Move the selected box
        """

        if not self.selected:
            return
        
        self.selected.move(stdscr, x, y)
        
    def switch_selected(self):
        """
            Hide / Show the selected box
        """

        if not self.selected:
            return
        
        self.selected.switch()

    def select(self, key: Any):
        """
            Select a box
        """

        box = self[key]

        if not box:
            return
        
        if self.selected:
            self.selected.unselect()

        box.select()
        self.selected = box

    def select_next(self):
        """
            Select the box next to the selected one
        """

        boxes_values = list(self.boxes.values())

        try:
            index = boxes_values.index(self.selected)
        except ValueError as error:
            print(error, file=stderr)
            return
        
        next_box_index = (index + 1) % len(boxes_values)
        new_box = boxes_values[next_box_index]
        self.select(new_box.name)
