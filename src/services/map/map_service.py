from typing import List, Optional

from reactivex import Observable
from reactivex.operators import map
from reactivex.subject import BehaviorSubject

from src.models.map import Map, Marker
from src.services.singleton import Singleton


class MapService(Singleton):
    __map: BehaviorSubject[Optional[Map]] = BehaviorSubject(None)
    __markers: BehaviorSubject[List[Marker]] = BehaviorSubject([])

    @property
    def map(self) -> Observable[Optional[Map]]:
        return self.__map

    @property
    def is_loaded(self) -> Observable[bool]:
        return self.__map.pipe(map(lambda map: map is not None))

    def markers(self) -> Observable[List[Marker]]:
        return self.__markers

    def set_map(self, map: Optional[Map]) -> None:
        self.__map.on_next(map)

    def add_marker(self, marker: Marker) -> None:
        self.__markers.on_next(self.__markers.value + [marker])
