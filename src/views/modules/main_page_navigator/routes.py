from enum import Enum


class MainPageNavigationRoutes(Enum):
    LOAD_MAP = "load_map"
    CURRENT_TOUR = "current_tour"
    ADD_DELIVERY_ADDRESS = "add_delivery_address"
    CONFIRM_DELIVERY_ADDRESS = "confirm_delivery_address"
    ADD_DELIVERY_TIME_WINDOW = "add_delivery_time_window"
    SELECT_DELIVERY_MAN_PAGE = "select"
