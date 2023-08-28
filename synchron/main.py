from parser import PhotoDownloader, JsonPlaceholderPhotoDownloader
from decorator import timer


class PhotoDownloaderApp:
    def __init__(self, photo_downloader: PhotoDownloader):
        self.photo_downloader = photo_downloader

    def run(self, album_id, save_folder):
        self.photo_downloader.download_photos(album_id, save_folder)


@timer
def main():
    target_album_id = 1  # Идентификатор альбома
    output_folder = "downloaded_photos"  # Папка для сохранения фотографий

    PhotoDownloaderApp(JsonPlaceholderPhotoDownloader()).run(
        target_album_id, output_folder
    )


if __name__ == "__main__":
    main()
