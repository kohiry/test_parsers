"""Этот модуль содержит класс App, который представляет собой приложение.

Класс App предоставляет методы для запуска приложения.
"""
from parser import download_all_photos
from decorator import timer


class App:
    """App.

    Представляет приложение.
    """

    def __init__(self):
        """Метод инициализации с главной папкой."""
        self.folder_name = "data"

    def run(self):
        """Функция run.

        Запускает приложение.
        """
        download_all_photos(self.folder_name)


@timer
def main():
    """Основная функция для запуска приложения."""
    print("Start app :)")
    App().run()


if __name__ == "__main__":
    main()
