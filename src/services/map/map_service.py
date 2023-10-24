from src.services.singleton import Singleton
from reactivex import Observable
from reactivex.subject import BehaviorSubject
from reactivex.operators import map
from src.models.map import Map
from typing import Optional


class MapService(Singleton):
    __map: BehaviorSubject[Optional[Map]] = BehaviorSubject(None)
    
    @property
    def map(self) -> Observable[Optional[Map]]:
        return self.__map
    
    @property
    def is_loaded(self) -> Observable[bool]:
        return self.__map.pipe(map(lambda map: map is not None))
    
    def set_map(self, map: Optional[Map]) -> None:
        self.__map.on_next(map)