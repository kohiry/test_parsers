"""Декоратор timer.

Замеряет быстродействие функции.
"""

import time


class AppList:
    """Класс, для формирования списка приложений."""

    apps = []

    @classmethod
    def add_class(cls, klass):  # have bug with App, Import Error. klass : App
        """Метод для добавления приложения в список."""
        cls.apps.append(klass)


def save_app(klass):
    """Декоратор для формирования списка приложений."""
    AppList.add_class(klass)
    return klass


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
