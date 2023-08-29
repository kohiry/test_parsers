from parser import (
    download_all_photos,
    SynchronPhotoDownloader,
    AsynchronPhotoDownloader,
)
from decorator import timer
from abc import ABC, abstractmethod
import asyncio


class App(ABC):
    @abstractmethod
    def run(self) -> None:
        pass


class SynchronApp(App):
    def __init__(self):
        self.folder_name: str = "data"

    def run(self):
        download_all_photos(SynchronPhotoDownloader(), self.folder_name)


class AsynchronApp(App):
    def __init__(self):
        self.folder_name: str = "data"

    async def run(self):
        download_all_photos(AsynchronPhotoDownloader(), self.folder_name)


@timer
def main(task: str):
    if not task.isalnum():
        print("Bad value.")
    task = int(task)
    if task == 1:
        SynchronApp().run()
    elif task == 2:
        asyncion.run(AsynchronApp().run())


if __name__ == "__main__":
    task = """
        1. synchron
        2. asynchron
    """

    main(input(task))
