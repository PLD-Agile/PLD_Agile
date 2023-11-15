import copy
from typing import Dict
from xml.etree.ElementTree import Element
from uuid import UUID

from pytest import fixture

from src.models.delivery_man.delivery_man import DeliveryMan
from src.services.delivery_man.delivery_man_service import DeliveryManService


class TestDeliveryManService:
    delivery_man_service: DeliveryManService

    @fixture(autouse=True)
    def setup_method(self):
        self.delivery_man_service = DeliveryManService.instance()

        yield

        DeliveryManService.reset()

    @fixture
    def root(self):
        self.n1 = DeliveryMan("Josué stcyr", [8, 9, 10, 11])
        self.n2 = DeliveryMan("clem farhat", [8, 9, 10, 11])

        root: Dict[UUID, DeliveryMan] = {
            self.n1.id: self.n1,
            self.n2.id: self.n2,
        }

        return root

    def test_should_create(self, root):
        length = len(self.delivery_man_service.delivery_men.value)
        delivery_man = self.delivery_man_service.create_delivery_man("test")

        assert delivery_man is not None or delivery_man == root[self.n1.id] or delivery_man == root[self.n2.id]
        assert isinstance(delivery_man, DeliveryMan)
        assert len(self.delivery_man_service.delivery_men.value) == length + 1

    def test_should_modify(self, root):
        delivery_man = list(self.delivery_man_service.delivery_men.value.values())[0]
        pre_name = delivery_man.name
        pre_availabilities = delivery_man.availabilities

        delivery_man_info = {"name": "name", "availabilities": [11]}
        delivery_man_modified = self.delivery_man_service.modify_delivery_man(delivery_man, delivery_man_info)

        assert delivery_man_modified is not None
        assert isinstance(delivery_man, DeliveryMan)
        assert delivery_man.name != pre_name
        assert delivery_man.availabilities != pre_availabilities
        assert delivery_man.id == delivery_man_modified.id

    def test_should_remove(self):
        length = len(self.delivery_man_service.delivery_men.value)
        delivery_man = list(self.delivery_man_service.delivery_men.value.values())[0]

        self.delivery_man_service.remove_delivery_man(delivery_man)

        assert len(self.delivery_man_service.delivery_men.value) == length - 1
        assert self.delivery_man_service.delivery_men.value.get(delivery_man.id) is None