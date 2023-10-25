import os
from dataclasses import dataclass

from pytest import fixture

from src.models.serializable import Serializable


@dataclass
class MyClass(Serializable):
    a: int
    b: list


class TestSerializable:
    my_class: MyClass

    @fixture(autouse=True)
    def init(self):
        self.my_class = MyClass(1, [1, 2, 3])

    def test_should_serialize_and_deserialize(self):
        serialized = self.my_class.serialize()
        deserialized = MyClass.deserialize(serialized)

        assert deserialized.a == self.my_class.a
        assert deserialized.b == self.my_class.b

    def test_should_serialize_to_file(self):
        PATH = "/tmp/test_serializable"

        self.my_class.save_to_file(PATH)
        deserialized = MyClass.load_from_file(PATH)

        assert deserialized.a == self.my_class.a
        assert deserialized.b == self.my_class.b

        os.remove(PATH)
