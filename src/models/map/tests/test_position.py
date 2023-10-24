from src.models.map.position import Position


class TestPosition:
    def test_should_create(self):
        assert Position(0, 0) is not None

    def test_should_get_longitude_equals_x(self):
        LONGITUDE = 420

        assert Position(LONGITUDE, 0).longitude == LONGITUDE
        assert Position(LONGITUDE, 0).x == LONGITUDE

    def test_should_get_latitude_equals_y(self):
        LATITUDE = 69

        assert Position(0, LATITUDE).latitude == LATITUDE
        assert Position(0, LATITUDE).y == LATITUDE

    def test_should_get_max(self):
        assert Position(1, 1).max(Position(2, 2)) == Position(2, 2)
        assert Position(1, 1).max(Position(2, 2), Position(3, 3)) == Position(3, 3)

    def test_should_get_min(self):
        assert Position(1, 1).min(Position(2, 2)) == Position(1, 1)
        assert Position(1, 1).min(Position(2, 2), Position(3, 3)) == Position(1, 1)
