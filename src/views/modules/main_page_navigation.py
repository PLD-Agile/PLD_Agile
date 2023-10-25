from enum import Enum

from src.controllers.navigator import Navigator, Route
from src.views.main_page.DeliveryPage import DeliveryPage


class MainPageNavigationRoutes(Enum):
    CURRENT_TOUR = "current_tour"
    ADD_DELIVERY_ADDRESS = "add_delivery_address"
    CONFIRM_DELIVERY_ADDRESS = "confirm_delivery_address"
    ADD_DELIVERY_TIME_WINDOW = "add_delivery_time_window"
    SELECT_DELIVERY_MAN_PAGE = "select"
    DELIVERY_PAGE= "delivery_page"


main_page_navigation = Navigator[MainPageNavigationRoutes](
    routes=[
        # Route(
        #     name=MainPageNavigationRoutes.CURRENT_TOUR,
        #     widget=CurrentTourPage,
        # ),
        Route(
            name=MainPageNavigationRoutes.DELIVERY_PAGE,
            widget=DeliveryPage,
        ),

        # Route(
        #     name=MainPageNavigationRoutes.ADD_DELIVERY_ADDRESS,
        #     widget=AddDeliveryAddressPage,
        # ),
        # Route(
        #     name=MainPageNavigationRoutes.CONFIRM_DELIVERY_ADDRESS,
        #     widget=ConfirmDeliveryAddressPage,
        # ),
        # Route(
        #     name=MainPageNavigationRoutes.ADD_DELIVERY_TIME_WINDOW,
        #     widget=AddDeliveryTimeWindowPage,
        # ),
        # Route(
        #     name=MainPageNavigationRoutes.SELECT_DELIVERY_MAN_PAGE,
        #     widget=SelectDeliveryManPage,
        # ),
    ],
    default_name=MainPageNavigationRoutes.DELIVERY_PAGE,
)
