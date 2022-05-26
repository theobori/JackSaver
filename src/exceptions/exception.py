"""exceptions system"""

class JackError(Exception):
    """
        Exception raised for errors for the sprites
    """

    def __init__(self, message: str = ""):
        self.message = message

        super().__init__(self.message)

    def __str__(self):
        return self.message
