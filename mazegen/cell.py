class Cell:

    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls: int = 15
        self.visited: bool = False
        self.is_pattern_42: bool = False

    def has_wall(self, direction_bit: int) -> bool:
        return bool(self.walls & direction_bit)

    def set_wall(self, direction_bit: int, closed: bool) -> None:
        if closed:
            self.walls |= direction_bit
        else:
            self.walls &= ~direction_bit

    def to_hex(self) -> str:
        return format(self.walls, "x")
