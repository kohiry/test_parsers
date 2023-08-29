class PhotoDTO:
    def __init__(self, id, title, url):
        self.id: int = id
        self.title: str = title
        self.url: str = url

    def __str__(self):
        return f"photo id: {self.id} | title: {self.title} | url: {self.url}"


class AlbumDTO:
    def __init__(self, id, title):
        self.id: int = id
        self.title: str = title

    def __str__(self):
        return f"album id: {self.id} | title: {self.title}"
