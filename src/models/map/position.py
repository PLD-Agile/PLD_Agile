from dataclasses import dataclass
from typing import List


@dataclass
class Position:
    longitude: float
    """Longitude of the position.
    """
    latitude: float
    """Latitude of the position.
    """

    @property
    def x(self) -> float:
        """Get the value of the X axis. Equivalent the longitude of the position."""
        return self.longitude

    @x.setter
    def x(self, value: float) -> None:
        """Set the value of the X axis. Equivalent the longitude of the position."""
        self.longitude = value

    @property
    def y(self) -> float:
        """Get the value of the Y axis. Equivalent the latitude of the position."""
        return self.latitude

    @y.setter
    def y(self, value: float) -> None:
        """Set the value of the Y axis. Equivalent the latitude of the position."""
        self.latitude = value

    def max(self, p: "Position", *args: List["Position"]) -> "Position":
        """Get the maximum position between the current position and the given position.

        Args:
            p (Position): Other position to compare.

        Returns:
            Position: New position instance with the maximum values.
        """
        return Position(
            max(self.longitude, p.longitude, *map(lambda p: p.longitude, args)),
            max(self.latitude, p.latitude, *map(lambda p: p.latitude, args)),
        )

    def min(self, p: "Position", *args: List["Position"]) -> "Position":
        """Get the minimum position between the current position and the given position.

        Args:
            p (Position): Other position to compare.

        Returns:
            Position: New position instance with the minimum values.
        """
        return Position(
            min(self.longitude, p.longitude, *map(lambda p: p.longitude, args)),
            min(self.latitude, p.latitude, *map(lambda p: p.latitude, args)),
        )
