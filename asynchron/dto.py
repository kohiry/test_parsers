"""DTO файл.

Описаны 2 класса. PhotoDTO, AlbumDTO.
"""
from pydantic import BaseModel


class PhotoDTO(BaseModel):
    """DTO класс PhotoDTO.

    Нужен для представления данных о фотографиях из парсера.
    """

    id: int
    title: str
    url: str
    content: bytes


class AlbumDTO(BaseModel):
    """DTO класс AlbumDTO.

    Нужен для представления данных о альбомах из парсера.
    """

    id: int
    title: str
