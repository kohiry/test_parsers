from typing import List, Tuple
import os
import requests
from multiprocessing import Process, Queue
from dto import AlbumDTO, PhotoDTO


class MultiprocParser:
    """Класс мультипроцессорного парсера."""

    def __init__(self):
        """Инициализация парсера.

        url: str -- аргумент с сылкой на парсируемый сайт
        """
        self.url: str = "https://jsonplaceholder.typicode.com/"

    def get_albums(self, queue: Queue):
        """Метод получения списка альбомов."""
        response = requests.get(self.url + "albums")
        if response.status_code == 200:
            for album in response.json():
                queue.put(AlbumDTO(id=album["id"], title=album["title"]))
        queue.put(None)

    def get_photo(self, queue: Queue, queue_album: Queue) -> Tuple[AlbumDTO, PhotoDTO]:
        """Метод получения генератора возвращающего альбом и фото."""
        while True:
            if queue_album.empty():
                # print(3)
                continue
            album = queue_album.get()
            # print(album)
            if album is None:
                break

            # print(album.id)
            response = requests.get(self.url + f"photos?albumId={album.id}")
            if response.status_code != 200:
                print("Failed connect.")
                break
            photos_data = response.json()
            # print(photos_data)
            for photo in photos_data:
                response_photo_solo = requests.get(photo["url"])

                queue.put(
                    (
                        album,
                        PhotoDTO(
                            id=photo["id"],
                            title=photo["title"],
                            url=photo["url"],
                            content=response_photo_solo.content,
                        ),
                    )
                )
        queue.put(None)


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

    def save(self, queue: Queue):
        """Основная логика сохранения DTO объектов."""
        while True:
            if queue.empty():
                continue

            item = queue.get()
            # print(item)
            if item is None:
                break
            album, photo = item
            photo_extension = os.path.splitext(photo.url)[1]

            # check folder
            SavePhotoAlbum.is_folder_here(self.save_folder + "/" + album.title)

            photo_path = os.path.join(
                self.save_folder + "/" + album.title,
                f"{photo.id}_{photo.title}{photo_extension}",
            )

            with open(photo_path, "wb") as photo_file:
                photo_file.write(photo.content)
                # print(f"Сохранено: {photo_path}")


def download_all_photos(folder_path: str):
    queue1 = Queue()
    queue2 = Queue()
    p1 = Process(target=MultiprocParser().get_albums, args=(queue1,))
    p2 = Process(target=MultiprocParser().get_photo, args=(queue2, queue1))
    p3 = Process(target=SavePhotoAlbum(folder_path).save, args=(queue2,))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
