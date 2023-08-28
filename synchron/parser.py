from types import List
from abc import ABC, abstractmethod


class PhotoDownloader(ABC):
    @abstractmethod
    def get_albums(self) -> List[dict]:
        pass

    @abstractmethod
    def save_all_photos(self):
        pass

    @abstractmethod
        def download_photos(self, ):
        pass
