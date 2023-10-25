from src.models.map.tour import Tour
from src.services.singleton import Singleton
from src.services.tour.tour_service import TourService


class TourSavingService(Singleton):
    def save_current_tour_from_index(self, index: int, path: str) -> None:
        TourService.instance().get_current_tour_from_index(index).save_to_file(path)

    def load_tour(self, path: str) -> None:
        TourService.instance().add_tour(Tour.load_from_file(path))
