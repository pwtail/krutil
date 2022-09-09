import inspect
from contextlib import contextmanager
from contextvars import ContextVar


is_vinyl = ContextVar('is_vinyl', default=False)


def hi_there():
    """
    After the transpiling to the sync version this becomes a regular function.
    """
    pass


def is_async():
    return inspect.iscoroutinefunction(hi_there)


@contextmanager
def use_vinyl():
    try:
        token = is_vinyl.set(True)
        yield
    finally:
        is_vinyl.reset(token)