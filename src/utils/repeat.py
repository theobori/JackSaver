"""repeat module"""

import threading
from typing import Callable

class RepeatFunc:
    """
        Optimized object that will call a function every n seconds
    """

    def __init__(self, n: float, callback: Callable, *args: list, **kwargs: dict):
        self._timer = None
        self.n = n
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.callback(*self.args, **self.kwargs)
        self.is_running = False

        self.start()

    def _run(self):
        """
            Call the function
        """

        self.is_running = False
        self.start()
        self.callback(*self.args, **self.kwargs)

    def start(self):
        """
            Start the reapeater
        """

        self._timer = threading.Timer(self.n, self._run)
        self._timer.start()
        self.is_running = True

    def stop(self):
        """
            Cancel the thread, then it stops the "loop"
        """

        self._timer.cancel()
