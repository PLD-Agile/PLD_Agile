from src.services.singleton import Singleton
from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.delivery_man.errors import DeliveryManError

class DeliveryManService(Singleton):
    def create_delivery_man(self, delivery_man_info) -> DeliveryMan:
        """Creates a Delivery Man and pass it back.
        
        Args:
            delivery_man_info: A dictionary containing the name,
            availabilities and speed (optional) of the deliveryman 
            to be created.
        
        Returns:
            DeliveryMan: DeliveryMan instance
        """

        name = delivery_man_info.get('name')
        availabilities = delivery_man_info.get('availabilities')
        speed = delivery_man_info.get('speed')
        
        if (name is not None) and (availabilities is not None):
            if (speed is not None):
                deliveryman = DeliveryMan(name, availabilities, speed)
            else:
                deliveryman = DeliveryMan(name, availabilities)
        
        else:
            raise DeliveryManError("No name or availabilities provided")

        return deliveryman
    
    def modify_delivery_man(self, delivery_man: DeliveryMan, delivery_man_info) -> DeliveryMan:
        """Updates a Delivery Man and pass it back.
        
        Args:
            delivery_man: A DeliveryMan instance to be updated
            delivery_man_info: A dictionary containing the new state
            of the DeliveryMan instance to be update
        
        Returns:
            DeliveryMan: DeliveryMan instance
        """
        name = delivery_man_info.get('name')
        availabilities = delivery_man_info.get('availabilities')
        speed = delivery_man_info.get('speed')
        
        if (name is not None):
            delivery_man.name = name
            
        if (availabilities is not None): 
            delivery_man.availabilities = availabilities
        
        if (speed is not None):
            delivery_man.speed = speed
        
        return delivery_man
        
    def remove_delivery_man(self, delivery_man: DeliveryMan) -> None:
        """Deletes a Delivery Man.
        
        Args:
            delivery_man: A DeliveryMan instance to be deleted
        """
        
        del(delivery_man)
        
        return
        
