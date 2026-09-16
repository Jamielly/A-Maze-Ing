"""Cell module representing an individual grid cell with bitmask walls."""


class Cell:
    """Represents a single cell in the maze with wall state bitmask."""

    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8

    def __init__(self, x: int, y: int) -> None:
        """Initialize a cell with coordinates and all four walls closed."""
        self.x: int = x
        self.y: int = y
        self.walls: int = 15
        self.visited: bool = False
        self.is_pattern_42: bool = False

    def has_wall(self, direction_bit: int) -> bool:
        """Check if a specific wall is closed."""
        return bool(self.walls & direction_bit)

    def set_wall(self, direction_bit: int, closed: bool) -> None:
        """Open or close a specific wall."""
        if closed:
            self.walls |= direction_bit
        else:
            self.walls &= ~direction_bit

    def to_hex(self) -> str:
        """Convert wall bitmask to a single hexadecimal character."""
        return format(self.walls, "x")
