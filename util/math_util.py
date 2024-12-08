from enum import Enum


def clamp(n):
    return max(-1, min(1, n))


def transpose(l):
    # https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
    return list(map(list, zip(*l)))


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

    def get_next(self) -> tuple[int, int]:
        match self:
            case Direction.North:
                return 0, -1
            case Direction.East:
                return 1, 0
            case Direction.South:
                return 0, 1
            case Direction.West:
                return -1, 0

    def turn_right(self):
        match self:
            case Direction.North:
                return Direction.East
            case Direction.East:
                return Direction.South
            case Direction.South:
                return Direction.West
            case Direction.West:
                return Direction.North


class Position:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, direction: Direction):
        delta = direction.get_next()
        self.x += delta[0]
        self.y += delta[1]

    def get_hash(self) -> int:
        return self.y * 1000 + self.x

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        raise TypeError(f"{other} is no Position")

    def __sub__(self, other):
        if isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        raise TypeError(f"{other} is no Position")

    def __hash__(self):
        return hash(self.y * 10000000 + self.x)

    def is_in_bounds(self, bounds) -> bool:
        return 0 <= self.x < bounds.x and 0 <= self.y < bounds.y
