"""Модуль сo всеми видами парсеров."""
from parser import (
    download_all_photos,
    SyncParser,
    AsyncParser,
)
from decorator import timer, save_app, AppList
from abc import ABC, abstractmethod
import asyncio


class App(ABC):
    """Абстрактный класс приложения."""

    @abstractmethod
    def run(self) -> None:
        """Метод запуска приложения."""
        pass


@save_app
class SyncApp(App):
    """Синхронное приложение."""

    def __init__(self):
        """Иницилизация синхронного приложения.

        folder_name: str -- принимает название главной папки с фото
        """
        self.folder_name: str = "data"

    def run(self):
        """Метод запуска приложения."""
        download_all_photos(SyncParser(), self.folder_name)


@save_app
class AsynApp(App):
    """Асинхронное приложение."""

    def __init__(self):
        """Иницилизация синхронного приложения.

        folder_name: str -- принимает название главной папки с фото
        """
        self.folder_name: str = "data2"

    async def run(self):
        """Метод запуска приложения."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_photos(AsyncParser(), self.folder_name))


@timer
def main(task: str):
    """Основная функция.

    Юзер выбирает какой парсер запустить.
    """
    if not task.isalnum():
        print("Bad value.")
        return 400
    task = int(task)
    if len(AppList.apps) < task:
        print("Not a option.")
        return 404
    i = 0
    for app in AppList.apps:
        if i + 1 == task:
            print("Ok.")
            app().run()
            return 200
        i += 1


if __name__ == "__main__":
    task = """
        1. synchron
        2. asynchron
    """

    main(input(task))
