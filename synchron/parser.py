import requests
from dto import PhotoDTO
import os
from abc import ABC, abstractmethod


class PhotoDownloader(ABC):
    @abstractmethod
    def download_photos(self, album_id, save_folder):
        pass


class JsonPlaceholderPhotoDownloader(PhotoDownloader):
    def download_photos(self, album_id, save_folder):
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/photos?albumId={album_id}"
        )

        if response.status_code != 200:
            print("Ошибка при получении данных")
            return
        photos_data = response.json()
        photos = [
            PhotoDTO(photo["id"], photo["title"], photo["url"]) for photo in photos_data
        ]

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        for photo in photos:
            photo_extension = os.path.splitext(photo.url)[1]
            photo_path = os.path.join(
                save_folder, f"{photo.id}_{photo.title}{photo_extension}"
            )
            photo_response = requests.get(photo.url)

            with open(photo_path, "wb") as photo_file:
                photo_file.write(photo_response.content)
                # print(f"Сохранено: {photo_path}")
        print("Данные сохранены.")
