from functools import wraps
from typing import TypeVar


class UnwrapException(Exception):
    ...


T = TypeVar("T")


class EarlyReturnException(ValueError):
    def __init__(self, value: T):
        self.value = value
        super().__init__(self.value)


def early_return(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except EarlyReturnException as e:
            return e.value
    return wrapper
