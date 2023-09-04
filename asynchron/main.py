"""Модуль запуска приложнеия."""
import asyncio
from decorator import timer
from parser import download_all_photos


class App:
    """Класс приложения."""

    def __init__(self):
        self.folder = "data"

    def run(self):
        asyncio.run(download_all_photos(self.folder))


@timer
def main():
    """Основной модуль запуска приложения."""
    App().run()


if __name__ == "__main__":
    main()
