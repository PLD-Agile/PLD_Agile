import pickle
from typing import Type, TypeVar

T = TypeVar("T", bound="Serializable")


class Serializable:
    def serialize(self) -> bytes:
        return pickle.dumps(self)

    def save_to_file(self, path: str) -> None:
        pickle.dump(self, open(path, "wb"))

    @classmethod
    def deserialize(cls: Type[T], data: bytes) -> T:
        return pickle.loads(data)

    @classmethod
    def load_from_file(cls: Type[T], path: str) -> T:
        return pickle.load(open(path, "rb"))
