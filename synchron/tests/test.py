import main
import dto


def test_album():
    data = main.SyncParser().get_albums()
    assert type(data[0]) is type(dto.AlbumDTO(id=1, title="123"))
    assert type(data[0].id) is type(dto.AlbumDTO(id=1, title="123").id)
    assert type(data[0].title) is type(dto.AlbumDTO(id=1, title="123").title)


def test_photo():
    data = main.SyncParser().get_albums()
    album_dto = dto.AlbumDTO(id=1, title="123")
    photo_dto = dto.PhotoDTO(id=1, title="123", url="123")
    for album, photo in main.SyncParser().get_photo(data[:10]):
        assert type(album) is type(album_dto)
        assert type(album.id) is type(album_dto.id)
        assert type(album.title) is type(album_dto.title)
        assert type(photo) is type(photo_dto)
        assert type(photo.title) is type(photo_dto.title)
        assert type(photo.url) is type(photo_dto.url)
