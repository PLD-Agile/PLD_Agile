from typing import Optional

from reactivex import Observable
from reactivex.subject import BehaviorSubject

from src.models.errors.no_value_error import NoValueError
from src.models.map.tour import Tour
from src.services.singleton import Singleton


class TourService(Singleton):
    __current_tour: BehaviorSubject[Optional[Tour]]

    def __init__(self) -> None:
        self.__current_tour = BehaviorSubject(None)

    @property
    def current_tour(self) -> Observable[Optional[Tour]]:
        return self.__current_tour

    def set_current_tour(self, tour: Tour) -> None:
        self.__current_tour.on_next(tour)

    def clear_current_tour(self) -> None:
        self.__current_tour.on_next(None)

    def get_current_tour_value(self) -> Tour:
        if not self.__current_tour.value:
            raise NoValueError("No current tour")

        return self.__current_tour.value
