from datetime import datetime, timedelta


class Config:
    INITIAL_DEPART_TIME = datetime(year=1, month=1, day=1, hour=8)
    """Time when the delivery driver starts his tour from the warehouse.
    """

    TIME_WINDOW_SIZE = timedelta(hours=1)
    """Time window size.
    """

    TRAVELING_SPEED = 15
    """Speed at which the delivery driver travels between two points in km/h.
    """

    DELIVERY_TIME = timedelta(minutes=5)
    """Time it takes to deliver a package.
    """

    KMH_TO_MS = 3.6
    """Conversion factor from km/h to m/s.
    """
