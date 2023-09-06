"""Декоратор timer.

Замеряет быстродействие функции.
"""

import time


def timer(func):
    """Декоратор принимает func."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Время исполнения функции {func.__name__}:"
            + f"{end_time - start_time} секунд"
        )
        return result

    return wrapper
