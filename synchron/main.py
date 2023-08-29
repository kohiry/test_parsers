from parser import download_all_photos, SynchronPhotoDownloader
from decorator import timer


class App:
    def __init__(self):
        self.folder_name: str = "data"

    def run(self):
        download_all_photos(SynchronPhotoDownloader(), self.folder_name)


@timer
def main():
    App().run()


if __name__ == "__main__":
    main()
