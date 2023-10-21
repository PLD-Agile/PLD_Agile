from enum import Enum
from typing import List, Tuple

import pytest
from PyQt6.QtWidgets import QWidget

from src.controllers.navigator.navigator import Navigator
from src.controllers.navigator.route import Route


class TestWidget1(QWidget):
    pass


class TestWidget2(QWidget):
    pass


class TestWidget3(QWidget):
    pass


class NotFoundWidget(QWidget):
    pass


class TestRoutes(Enum):
    route1 = "route1"
    route2 = "route2"
    route3 = "route3"


DEFAULT_ROUTE_NAME = TestRoutes.route2

ROUTES: List[Route[TestRoutes]] = [
    Route(name=TestRoutes.route1, widget=TestWidget1),
    Route(name=TestRoutes.route2, widget=TestWidget2),
    Route(name=TestRoutes.route3, widget=TestWidget3),
]


class TestNavigator:
    navigator: Navigator[TestRoutes]

    @pytest.fixture(autouse=True)
    def init_navigator(self) -> Navigator[TestRoutes]:
        self.navigator = Navigator[TestRoutes](
            routes=ROUTES,
            default_name=DEFAULT_ROUTE_NAME,
            not_found_widget=NotFoundWidget,
        )

    def test_should_create(self):
        assert self.navigator is not None

    def test_should_show_default_route(self):
        def on_next(route_name):
            assert route_name == DEFAULT_ROUTE_NAME

        self.navigator.current_route_name.subscribe(on_next)

    def test_should_add_to_history_on_push(self):
        self.navigator.push(TestRoutes.route1)

        def on_next(history_stack):
            assert history_stack == [DEFAULT_ROUTE_NAME, TestRoutes.route1]

        self.navigator.history_stack.subscribe(on_next)

    def test_should_replace_history_on_replace(self):
        self.navigator.push(TestRoutes.route3)
        self.navigator.replace(TestRoutes.route1)

        def on_next(history_stack):
            assert history_stack == [DEFAULT_ROUTE_NAME, TestRoutes.route1]

        self.navigator.history_stack.subscribe(on_next)

    def test_should_pop_history_on_pop(self):
        self.navigator.push(TestRoutes.route1)
        self.navigator.pop()

        def on_next(history_stack):
            assert history_stack == [DEFAULT_ROUTE_NAME]

        self.navigator.history_stack.subscribe(on_next)

    def test_should_raise_error_on_pop_when_only_one_route(self):
        with pytest.raises(IndexError):
            self.navigator.pop()

    def test_should_not_push_same_route(self):
        self.navigator.push(TestRoutes.route1)
        self.navigator.push(TestRoutes.route1)

        def on_next(history_stack):
            assert history_stack == [DEFAULT_ROUTE_NAME, TestRoutes.route1]

        self.navigator.history_stack.subscribe(on_next)

    def test_should_resolve(self):
        def on_next(res: Tuple[int, Route]):
            assert res[1].widget == TestWidget2

        self.navigator.current_route.subscribe(on_next)

    def test_should_resolve_on_change(self):
        self.navigator.push(TestRoutes.route1)

        def on_next(res: Tuple[int, Route]):
            assert res[1].widget == TestWidget1

        self.navigator.current_route.subscribe(on_next)
