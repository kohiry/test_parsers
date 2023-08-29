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
    @abstractmethod
    def run(self) -> None:
        pass


@save_app
class SyncApp(App):
    def __init__(self):
        self.folder_name: str = "data"

    def run(self):
        download_all_photos(SyncParser(), self.folder_name)


@save_app
class AsynApp(App):
    def __init__(self):
        self.folder_name: str = "data"

    async def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_photos(AsyncParser(), self.folder_name))


@timer
def main(task: str):
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
