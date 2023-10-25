from typing import List

from reactivex import Observable
from reactivex.subject import BehaviorSubject

from src.models.errors.no_value_error import NoValueError
from src.models.map.tour import Tour
from src.services.singleton import Singleton


class TourService(Singleton):
    __current_tours: BehaviorSubject[List[Tour]]

    def __init__(self) -> None:
        self.__current_tours = BehaviorSubject([])

    @property
    def current_tours(self) -> Observable[List[Tour]]:
        return self.__current_tours

    def add_tour(self, tour: Tour) -> None:
        self.__current_tours.on_next(self.__current_tours + [tour])
        
    def remove_tour_from_index(self, index: int) -> None:
        self.__current_tours.on_next(self.__current_tours.value[:index] + self.__current_tours.value[index + 1:])

    def clear_current_tours(self) -> None:
        self.__current_tours.on_next([])

    def get_current_tours(self) -> List[Tour]:
        return self.__current_tours.value
    
    def get_current_tour_from_index(self, index: int) -> Tour:
        tour = self.__current_tours.value[index]
        
        if not tour:
            raise NoValueError("No tour found at index " + str(index))
        
        return tour