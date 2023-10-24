from src.models.map.map_size import MapSize
from src.models.map.position import Position


class TestMapSize:
    def test_should_create(self):
        assert MapSize(Position(0, 0), Position(0, 0)) is not None

    def test_should_create_inverse_max_size(self):
        assert MapSize.inverse_max_size() is not None

    def test_should_calculate_area(self):
        assert MapSize(Position(0, 0), Position(1, 1)).area == 1
        assert MapSize(Position(0, 0), Position(2, 2)).area == 4
        assert MapSize(Position(0, 0), Position(3, 3)).area == 9

    def test_should_get_min(self):
        assert MapSize(Position(0, 0), Position(1, 1)).min == Position(0, 0)

    def test_should_set_min(self):
        map_size = MapSize(Position(0, 0), Position(1, 1))
        map_size.min = Position(1, 1)

        assert map_size.min == Position(1, 1)

    def test_should_get_max(self):
        assert MapSize(Position(0, 0), Position(1, 1)).max == Position(1, 1)

    def test_should_set_max(self):
        map_size = MapSize(Position(0, 0), Position(1, 1))
        map_size.max = Position(0, 0)

        assert map_size.max == Position(0, 0)

    def test_should_get_width(self):
        assert MapSize(Position(0, 0), Position(1, 1)).width == 1
        assert MapSize(Position(0, 0), Position(2, 2)).width == 2
        assert MapSize(Position(0, 0), Position(3, 3)).width == 3

    def test_should_get_height(self):
        assert MapSize(Position(0, 0), Position(1, 1)).height == 1
        assert MapSize(Position(0, 0), Position(2, 2)).height == 2
        assert MapSize(Position(0, 0), Position(3, 3)).height == 3
