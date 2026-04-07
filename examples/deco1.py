from typing import Callable

def deco(func: Callable):
    def wrapper():
        res = func()
        return res
    return wrapper

