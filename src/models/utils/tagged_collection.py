from typing import Dict, Generic, List, TypeVar

Tag = TypeVar("Tag")
Value = TypeVar("Value")


class TaggedCollection(Generic[Tag, Value]):
    __collection: Dict[Tag, List[Value]] = {}

    def get(self, tag: Tag) -> List[Value]:
        return self.__collection.get(tag, [])

    def append(self, tag: Tag, value: Value) -> None:
        self.__collection[tag] = self.get(tag) + [value]

    def clear(self, tag: Tag) -> None:
        self.__collection[tag] = []

    def get_all(self) -> List[Value]:
        return [value for values in self.__collection.values() for value in values]

    def clear_all(self) -> None:
        self.__collection = {}
