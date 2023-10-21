from enum import Enum

from src.controllers.navigator import Navigator, Route
from src.views.main_page.main_page import MainPage
from src.views.manage_delivery_man_page.manage_delivery_man_page import \
    ManageDeliveryManPage


class MainNavigationRoutes(Enum):
    MAIN = "main"
    MANAGE_DELIVERY_MAIN = "manage_delivery_main"


main_navigation = Navigator[MainNavigationRoutes](
    routes=[
        Route(name=MainNavigationRoutes.MAIN, widget=MainPage),
        Route(
            name=MainNavigationRoutes.MANAGE_DELIVERY_MAIN,
            widget=ManageDeliveryManPage,
        ),
    ],
    default_name=MainNavigationRoutes.MAIN,
)
