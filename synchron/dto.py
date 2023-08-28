class PhotoDTO:
    def __init__(self, id, title, url):
        self.id = id
        self.title = title
        self.url = url

    def __str__(self):
        return f"photo id: {self.id} | title: {self.title} | url: {self.url}"


class AlbumDTO:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __str__(self):
        return f"album id: {self.id} | title: {self.title}"

