from src.services.singleton import Singleton
from src.models.tour import ComputedTour
from typing import List
import pickle


class TourSavingService(Singleton):
    def save_tours(self, tours: ComputedTour, path: str) -> None:
        pickle.dump(tours, open(path, "wb"))
        
    def load_tours(self, path: str) -> List[ComputedTour]:
        return pickle.load(open(path, "rb"))