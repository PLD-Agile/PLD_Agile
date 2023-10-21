from dataclasses import dataclass


@dataclass
class NavigatorConfig:
    allow_push_same_route: bool = False
    allow_replace_same_route: bool = False
