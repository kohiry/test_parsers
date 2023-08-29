"""DTO файл.

Описаны 2 класса. PhotoDTO, AlbumDTO.
"""


class PhotoDTO:
    """DTO класс PhotoDTO.

    Нужен для представления данных о фотографиях из парсера.
    """

    def __init__(self, id, title, url):
        """Инициализация DTO класса.

        Принимает:
            id: int
            title: str
            url: str
        """
        self.id: int = id
        self.title: str = title
        self.url: str = url

    def __str__(self):
        """Магический метод для отображения PhotoDTO экземпляров."""
        return f"photo id: {self.id} | title: {self.title} | url: {self.url}"


class AlbumDTO:
    """DTO класс AlbumDTO.

    Нужен для представления данных о альбомах из парсера.
    """

    def __init__(self, id, title):
        """Инициализация DTO класса.

        Принимает:
            id: int
            title: str
        """
        self.id: int = id
        self.title: str = title

    def __str__(self):
        """Магический метод для отображения AlbumDTO экземпляров."""
        return f"album id: {self.id} | title: {self.title}"
