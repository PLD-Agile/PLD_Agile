from enum import Enum

from src.controllers.navigator import Navigator, Route
from src.views.manage_delivery_man_page.add_delivery_man_form_view import \
    AddDeliveryManFormView
from src.views.manage_delivery_man_page.delete_delivery_man_form_view import \
    DeleteDeliveryManFormView
from src.views.manage_delivery_man_page.menu_view import MenuView
from src.views.manage_delivery_man_page.modify_delivery_man_form_view import \
    ModifyDeliveryManFormView


class ManageDeliveryManNavigationRoutes(Enum):
    MENU = "menu"
    ADD_DELIVERY_MAN_FORM = "add_delivery_man_form"
    MODIFY_DELIVERY_MAN_FORM = "modify_delivery_man_form"
    DELETE_DELIVERY_MAN_FORM = "delete_delivery_man_form"


manage_delivery_man_navigation = Navigator[ManageDeliveryManNavigationRoutes](
    routes=[
        Route(name=ManageDeliveryManNavigationRoutes.MENU, widget=MenuView),
        Route(
            name=ManageDeliveryManNavigationRoutes.ADD_DELIVERY_MAN_FORM,
            widget=AddDeliveryManFormView,
        ),
        Route(
            name=ManageDeliveryManNavigationRoutes.MODIFY_DELIVERY_MAN_FORM,
            widget=ModifyDeliveryManFormView,
        ),
        Route(
            name=ManageDeliveryManNavigationRoutes.DELETE_DELIVERY_MAN_FORM,
            widget=DeleteDeliveryManFormView,
        ),
    ],
    default_name=ManageDeliveryManNavigationRoutes.MENU,
)
