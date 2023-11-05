import pickle
from typing import List

from src.models.tour import ComputedTour
from src.services.singleton import Singleton


class TourSavingService(Singleton):
    def save_tours(self, tours: ComputedTour, path: str) -> None:
        pickle.dump(tours, open(path, "wb"))

    def load_tours(self, path: str) -> List[ComputedTour]:
        return pickle.load(open(path, "rb"))
