from enum import Enum

from src.controllers.navigator import Navigator, Route
from src.views.main_page.main_page import MainPage
from src.views.manage_delivery_man_page.manage_delivery_man_page import (
    ManageDeliveryManPage,
)


class AppNavigationRoutes(Enum):
    MAIN = "main"
    MANAGE_DELIVERY_MAIN = "manage_delivery_main"


app_navigation = Navigator[AppNavigationRoutes](
    routes=[
        Route(name=AppNavigationRoutes.MAIN, widget=MainPage),
        Route(
            name=AppNavigationRoutes.MANAGE_DELIVERY_MAIN,
            widget=ManageDeliveryManPage,
        ),
    ],
    default_name=AppNavigationRoutes.MAIN,
)
