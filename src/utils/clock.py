"""clock module"""

import time

class Clock:
    """
        This class will be used as a timer
    """

    def __init__(self, delay: float= 1):
        self.clock = time.time()
        self.delay = delay

    def check(self) -> bool:
        """
            Return if the delay has been passed
        """

        current_time = time.time()

        if (current_time - self.clock < self.delay):
            return (False)
        self.clock = current_time
        return (True)
