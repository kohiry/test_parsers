"""Модуль сo всеми видами парсеров."""
from parser import (
    download_all_photos,
    SyncParser,
)
from decorator import timer
import asyncio


class SyncApp:
    """Синхронное приложение."""

    def __init__(self):
        """Иницилизация синхронного приложения.

        folder_name: str -- принимает название главной папки с фото
        """
        self.folder_name: str = "data"

    def run(self):
        """Метод запуска приложения."""
        download_all_photos(SyncParser(), self.folder_name)


@timer
def main():
    """Основная функция."""
    SyncApp().run()
    return 200


if __name__ == "__main__":
    print("Start download img.")
    main()
