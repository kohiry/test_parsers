import asyncio
import os
from typing import List, Tuple
from aiohttp import ClientSession
from dto import AlbumDTO, PhotoDTO
from aiohttp.streams import StreamReader
import aiofiles

client_session = {}


async def read_stream(reader: StreamReader) -> bytes:
    """Чтение данных из потока и преобразование к типу bytes."""
    buffer_size = 1024
    data = b""
    while True:
        chunk = await reader.read(buffer_size)
        if not chunk:
            break
        data += chunk
    return data


class AsyncParser:
    """Класс асинхронного парсера."""

    def __init__(self):
        """Инициализация парсера.

        url: str -- аргумент с сылкой на парсируемый сайт
        """
        self.url: str = "https://jsonplaceholder.typicode.com/"

    @staticmethod
    async def __get_album_from_list(data: List[dict]):
        for d in data:
            yield d

    async def get_album(self):
        """Метод получения списка альбомов."""
        async with client_session["session"].get(self.url + "albums") as response:
            if response.status == 200:
                albums_data = await response.json()
                async for album in self.__get_album_from_list(albums_data):
                    yield AlbumDTO(id=album["id"], title=album["title"])

    #             return []

    async def get_photo(self) -> Tuple[AlbumDTO, PhotoDTO]:
        """Метод получения генератора возвращающего альбом и фото."""
        async for album in self.get_album():
            async with client_session["session"].get(
                self.url + f"photos?albumId={album.id}"
            ) as response:
                if response.status != 200:
                    print("Failed connect.")
                    break
                photos_data = await response.json()
                # print(photos_data)
                async for photo in self.__get_album_from_list(photos_data):
                    async with client_session["session"].get(
                        photo["url"]
                    ) as photo_solo:
                        # print(type(photo_solo.content))
                        yield (
                            album,
                            PhotoDTO(
                                id=photo["id"],
                                title=photo["title"],
                                url=photo["url"],
                                content=await read_stream(photo_solo.content),
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

    @staticmethod
    def is_folder_here(save_folder: str) -> None:
        """Проверка наличия папки."""
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

    async def save(self, album: AlbumDTO, photo: PhotoDTO):
        """Основная логика сохранения DTO объектов."""
        SavePhotoAlbum.is_folder_here(self.save_folder)
        photo_extension = os.path.splitext(photo.url)[1]

        # check folder
        SavePhotoAlbum.is_folder_here(self.save_folder + "/" + album.title)

        photo_path = os.path.join(
            self.save_folder + "/" + album.title,
            f"{photo.id}_{photo.title}{photo_extension}",
        )

        async with aiofiles.open(photo_path, "wb") as photo_file:
            await photo_file.write(photo.content)
            # print(f"Сохранено: {photo_path}")


async def download_all_photos(folder_path: str):
    """Метод для реализации парсинга и сохранения объектов."""
    client_session["session"] = ClientSession()
    async with client_session["session"]:
        async for album, photo in AsyncParser().get_photo():
            await SavePhotoAlbum(folder_path).save(album, photo)
