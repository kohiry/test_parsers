"""Модуль с основной логикой парсеров."""
from typing import List, Tuple
import os
from dto import PhotoDTO, AlbumDTO
import requests


class SyncParser:
    """Класс синхронного парсера."""

    def __init__(self):
        """Инициализация парсера.

        url: str -- аргумент с сылкой на парсируемый сайт
        """
        self.url: str = "https://jsonplaceholder.typicode.com/"

    def get_albums(self) -> List[AlbumDTO]:
        """Метод получения списка альбомов."""
        response = requests.get(self.url + "albums")
        if response.status_code == 200:
            return [
                AlbumDTO(id=album["id"], title=album["title"])
                for album in response.json()
            ]
        return []

    def get_photo(self, albums: List[AlbumDTO]) -> Tuple[AlbumDTO, PhotoDTO]:
        """Метод получения генератора возвращающего альбом и фото."""
        for album in albums:
            # print(album.id)
            response = requests.get(self.url + f"photos?albumId={album.id}")
            if response.status_code != 200:
                print("Failed connect.")
                break
            photos_data = response.json()
            # print(photos_data)
            for photo in photos_data:
                response_photo_solo = requests.get(photo["url"])

                yield (
                    album,
                    PhotoDTO(
                        id=photo["id"],
                        title=photo["title"],
                        url=photo["url"],
                        content=response_photo_solo.content,
                    ),
                )


class SavePhotoAlbum:
    """Класс для сохранения фотографий и алюбомов полученный в DTO формате."""

    def __init__(self, save_folder: str):
        """Инициализация.

        save_folder: str -- аргумент с указанием куда сохранять альбомы, ниже
                            проверека есть ли такая папка.
        """
        # check main folder created or not
        self.save_folder: str = save_folder
        SavePhotoAlbum.is_folder_here(save_folder)

    @staticmethod
    def is_folder_here(save_folder: str) -> None:
        """Проверка наличия папки."""
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

    def save(self, album: AlbumDTO, photo: PhotoDTO):
        """Основная логика сохранения DTO объектов."""
        photo_extension = os.path.splitext(photo.url)[1]

        # check folder
        SavePhotoAlbum.is_folder_here(self.save_folder + "/" + album.title)

        photo_path = os.path.join(
            self.save_folder + "/" + album.title,
            f"{photo.id}_{photo.title}{photo_extension}",
        )
        # print(type(photo_response.content))

        with open(photo_path, "wb") as photo_file:
            photo_file.write(photo.content)
            # print(f"Сохранено: {photo_path}")


def download_all_photos(downloader: SyncParser, folder_path: str):
    """Метод для реализации парсинга и сохранения объектов."""
    albums: List[AlbumDTO] = downloader.get_albums()
    for album, photo in downloader.get_photo(albums):
        SavePhotoAlbum(folder_path).save(album, photo)
