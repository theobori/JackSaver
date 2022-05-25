"""binds manager"""

import curses
from typing import Union, Any, Callable

class Bind:
    """
        Describing combination (hotkey -- callback)
    """

    def __init__(self, key: Any, callback: Callable, *args: list, **kwargs: dict):
        self.key = key
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
    
    def try_call(self) -> bool:
        """
            Tries to call the stored function
        """

        ret = True

        try:
            self.callback(*self.args, **self.kwargs)
        except:
            ret = False
        
        return (ret)

class Binds:
    """
        Storing Jack Saver bind
        hotkey --> function
    """

    def __init__(self):
        self.key_binding = {}

    def __getitem__(self, key: Any) -> Union[Bind, None]:
        if not key in self.key_binding.keys():
            return (None)

        return (self.key_binding[key])
    
    def add_bind(self, key: Any, function: callable, *args: list, **kwargs: dict):
        """
            Add a Bind to the dictionnary
        """
        
        bind = Bind(key, function, *args, **kwargs)

        self.key_binding[key] = bind

    def try_call_from_bind(self, key: Any) -> bool:
        """
            If the dictionnary key is found, 
            then it tries to call the associated function
        """

        bind = self[key]

        if not bind:
            return (False)
        
        return bind.try_call()
    

def hello(a: str):
    print("hello " + a)
