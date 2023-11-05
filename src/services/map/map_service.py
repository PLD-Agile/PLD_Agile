from typing import List, Optional

from reactivex import Observable
from reactivex.operators import map
from reactivex.subject import BehaviorSubject

from src.models.map import Map
from src.services.singleton import Singleton
from src.services.tour.tour_service import TourService


class MapService(Singleton):
    __map: BehaviorSubject[Optional[Map]]

    def __init__(self) -> None:
        self.__map = BehaviorSubject(None)

    @property
    def map(self) -> Observable[Optional[Map]]:
        return self.__map

    @property
    def is_loaded(self) -> Observable[bool]:
        return self.__map.pipe(map(lambda map: map is not None))

    def set_map(self, map: Map) -> None:
        self.__map.on_next(map)

    def clear_map(self) -> None:
        self.__map.on_next(None)
        TourService.instance().clear_tour_requests()
        TourService.instance().clear_computed_tours()
