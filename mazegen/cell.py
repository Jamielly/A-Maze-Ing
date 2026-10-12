"""Module responsible for representing individual maze cells and their wall configurations."""


class Cell:
    """Represents a single cell within the maze grid with coordinates, walls, and state flags."""

    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8

    def __init__(self, x: int, y: int) -> None:
        """Initializes a maze cell with coordinates and default walls (all closed).

        Args:
            x: The column coordinate of the cell.
            y: The row coordinate of the cell.
        """
        self.x: int = x
        self.y: int = y
        self.walls: int = 15
        self.visited: bool = False
        self.is_pattern_42: bool = False

    def has_wall(self, direction_bit: int) -> bool:
        """Check if a specific wall is closed.

        Args:
            direction_bit: Bitmask integer representing the direction (1, 2, 4, or 8).

        Returns:
            True if the wall is closed, False otherwise.
        """
        return bool(self.walls & direction_bit)

    def set_wall(self, direction_bit: int, closed: bool) -> None:
        """Sets a specific wall to be closed or open.

        Args:
            direction_bit: Bitmask integer representing the direction (1, 2, 4, or 8).
            closed: Boolean indicating whether to close (True) or open (False) the wall.
        """
        if closed:
            self.walls |= direction_bit
        else:
            self.walls &= ~direction_bit

    def to_hex(self) -> str:
        """Converts the cell's wall bitmask integer into a hexadecimal character string.

        Returns:
            A lowercase hexadecimal character representing the wall configuration.
        """
        return format(self.walls, "x")