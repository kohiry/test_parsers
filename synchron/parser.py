from typing import List, Tuple
import os
from dto import PhotoDTO, AlbumDTO
import requests
from abc import ABC, abstractmethod
from pprint import pprint


class PhotoDownloader(ABC):
    @abstractmethod
    def get_albums(self) -> List[dict]:
        pass

    @abstractmethod
    def get_photo(self, albums: List[AlbumDTO]) -> Tuple[AlbumDTO, PhotoDTO]:
        pass


class SynchronPhotoDownloader(PhotoDownloader):
    def __init__(self):
        self.url: str = "https://jsonplaceholder.typicode.com/"

    def get_albums(self):
        response = requests.get(self.url + "albums")
        if response.status_code == 200:
            return [
                AlbumDTO(id=album["id"], title=album["title"])
                for album in response.json()
            ]
        return []

    def get_photo(self, albums: List[AlbumDTO]) -> Tuple[AlbumDTO, PhotoDTO]:
        for album in albums:
            # print(album.id)
            response = requests.get(self.url + f"photos?albumId={album.id}")
            if response.status_code != 200:
                print("Failed connect.")
                break
            photos_data = response.json()
            # print(photos_data)
            photos = [
                PhotoDTO(photo["id"], photo["title"], photo["url"])
                for photo in photos_data
            ]

            for photo in photos:
                yield (album, photo)


class SavePhotoAlbum:
    def __init__(self, save_folder: str):
        # check main folder created or not
        self.save_folder: str = save_folder
        SavePhotoAlbum.is_folder_here(save_folder)

    @staticmethod
    def is_folder_here(save_folder: str) -> None:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

    def save(self, album: AlbumDTO, photo: PhotoDTO):
        photo_extension = os.path.splitext(photo.url)[1]

        # check folder
        SavePhotoAlbum.is_folder_here(self.save_folder + "/" + album.title)

        photo_path = os.path.join(
            self.save_folder + "/" + album.title,
            f"{photo.id}_{photo.title}{photo_extension}",
        )
        photo_response = requests.get(photo.url)

        with open(photo_path, "wb") as photo_file:
            photo_file.write(photo_response.content)
            # print(f"Сохранено: {photo_path}")


def download_all_photos(downloader: PhotoDownloader, folder_path: str):
    albums: List[AlbumDTO] = downloader.get_albums()
    for album, photo in downloader.get_photo(albums):
        SavePhotoAlbum(folder_path).save(album, photo)


# download_all_photos(SynchronPhotoDownloader(), "data")
