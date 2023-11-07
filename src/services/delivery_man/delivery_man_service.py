from typing import Dict, List
from reactivex import Observable

from reactivex.subject import BehaviorSubject

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.delivery_man.errors import DeliveryManError
from src.services.singleton import Singleton


class DeliveryManService(Singleton):
    __delivery_men : BehaviorSubject[Dict[str, DeliveryMan]] = BehaviorSubject({
        "Josué stcyr": DeliveryMan("Josué stcyr", [8, 9, 10, 11]),
        "clem farhat": DeliveryMan("clem farhat", [8, 9, 10, 11]),
    })

    @property
    def delivery_men(self) -> Observable[Dict[str, DeliveryMan]]:
        """Returns every Delivery Men.

        Args:
           No args.

        Returns:
            Observable[Dict[DeliveryMan]]: DeliveryMen dictionnary observable instance
        """

        return self.__delivery_men

    def create_delivery_man(self, name: str) -> None:
        """Creates a Delivery Man and pass it back.

        Args:
            name: a string that represents the name of the delivery name that'll be created

        Returns:
            None
        """

        availabilities = [8, 9, 10, 11]

        if (name is None):
            raise DeliveryManError("No name or availabilities provided")

        deliveryman = DeliveryMan(name, availabilities)
        
        self.__delivery_men.value[deliveryman.name] = deliveryman
        self.__delivery_men.on_next(self.__delivery_men.value)

        return deliveryman

    def modify_delivery_man(
        self, delivery_man: DeliveryMan, delivery_man_info
    ) -> DeliveryMan:
        """Updates a Delivery Man and pass it back.

        Args:
            delivery_man: A DeliveryMan instance to be updated
            delivery_man_info: A dictionary containing the new state
            of the DeliveryMan instance to be update

        Returns:
            DeliveryMan: DeliveryMan instance
        """
        
        delivery_man = self.__delivery_men.value[delivery_man.name]

        name = delivery_man_info.get("name")
        availabilities = delivery_man_info.get("availabilities")
        speed = delivery_man_info.get("speed")

        if name is not None:
            delivery_man.name = name

        if availabilities is not None:
            delivery_man.availabilities = availabilities

        self.__delivery_men.on_next(self.__delivery_men.value)

        return delivery_man

    def remove_delivery_man(self, delivery_man: DeliveryMan) -> None:
        """Deletes a Delivery Man.

        Args:
            delivery_man: A DeliveryMan instance to be deleted
        """

        del self.__delivery_men.value[delivery_man.name]
        self.__delivery_men.on_next(self.__delivery_men.value)
        
        return
