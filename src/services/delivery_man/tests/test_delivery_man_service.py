from typing import Dict
from xml.etree.ElementTree import Element

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
        root: Dict[str, DeliveryMan] = {
        "Josué stcyr": DeliveryMan("Josué stcyr", [8, 9, 10, 11]),
        "clem farhat": DeliveryMan("clem farhat", [8, 9, 10, 11]),
        }

        return root

    def test_should_create(self, root):
        length = len(self.delivery_man_service.delivery_men.value)
        delivery_man = self.delivery_man_service.create_delivery_man("Josué stcyr")

        assert delivery_man == root["Josué stcyr"]
        assert len(self.delivery_man_service.delivery_men.value) == length+1