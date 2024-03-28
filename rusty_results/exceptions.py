from functools import wraps


class UnwrapException(Exception):
    ...


class EarlyReturnException[T](ValueError):
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
