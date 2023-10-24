from src.controllers.navigator import Route
from src.views.main_page.add_delivery_address_page import AddDeliveryAddressPage
from src.views.main_page.add_delivery_time_window_page import AddDeliveryTimeWindowPage
from src.views.main_page.confirm_delivery_address_page import ConfirmDeliveryAddressPage
from src.views.main_page.current_tour_page import CurrentTourPage
from src.views.main_page.load_map_page import LoadMapPage
from src.views.main_page.select_delivery_man_page import SelectDeliveryManPage
from src.views.modules.main_page_navigator.navigator import get_main_page_navigator
from src.views.modules.main_page_navigator.routes import MainPageNavigationRoutes


def init_main_page_navigator():
    get_main_page_navigator().init(
        routes=[
            Route(
                name=MainPageNavigationRoutes.LOAD_MAP,
                widget=LoadMapPage,
            ),
            Route(
                name=MainPageNavigationRoutes.CURRENT_TOUR,
                widget=CurrentTourPage,
            ),
            Route(
                name=MainPageNavigationRoutes.ADD_DELIVERY_ADDRESS,
                widget=AddDeliveryAddressPage,
            ),
            Route(
                name=MainPageNavigationRoutes.CONFIRM_DELIVERY_ADDRESS,
                widget=ConfirmDeliveryAddressPage,
            ),
            Route(
                name=MainPageNavigationRoutes.ADD_DELIVERY_TIME_WINDOW,
                widget=AddDeliveryTimeWindowPage,
            ),
            Route(
                name=MainPageNavigationRoutes.SELECT_DELIVERY_MAN_PAGE,
                widget=SelectDeliveryManPage,
            ),
        ],
        default_name=MainPageNavigationRoutes.LOAD_MAP,
    )
