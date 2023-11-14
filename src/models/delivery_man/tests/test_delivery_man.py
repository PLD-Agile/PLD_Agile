import unittest
from src.models.delivery_man.delivery_man import DeliveryMan

class TestDeliveryMan(unittest.TestCase):
    def test_should_create(self):
        assert DeliveryMan("", []) is not None
        
    def test_should_not_create(self):
         with self.assertRaises(TypeError):
            DeliveryMan()