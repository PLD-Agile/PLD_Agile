from src.models.map.tour import Tour
from src.services.singleton import Singleton
from src.services.tour.tour_service import TourService


class TourSavingService(Singleton):
    def save_current_tour(self, path: str) -> None:
        TourService.instance().save_to_file(path)

    def load_tour(self, path: str) -> None:
        TourService.instance().set_current_tour(Tour.load_from_file(path))
