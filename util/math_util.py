import math
from enum import Enum


def clamp(n):
    return max(-1, min(1, n))


def transpose(l):
    # https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
    return list(map(list, zip(*l)))


class Direction(Enum):
    North = 0, -1
    NorthEast = 1, -1
    East = 1, 0
    SouthEast = 1, 1
    South = 0, 1
    SouthWest = -1, 1
    West = -1, 0
    NorthWest = -1, -1

    hash_value: int

    def __init__(self, x: int, y: int):
        self.hash_value = (y + 1) * 3 + x + 1

    def turn_right_90(self):
        match self:
            case Direction.North:
                return Direction.East
            case Direction.NorthEast:
                return Direction.SouthEast
            case Direction.East:
                return Direction.South
            case Direction.SouthEast:
                return Direction.SouthWest
            case Direction.South:
                return Direction.West
            case Direction.SouthWest:
                return Direction.NorthWest
            case Direction.West:
                return Direction.North
            case Direction.NorthWest:
                return Direction.NorthEast

    def __mul__(self, other):
        if isinstance(other, int):
            return self.value[0] * other, self.value[1] * other
        raise TypeError(f"{other} is no int")

    def __hash__(self) -> int:
        return self.hash_value


class Position:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x != other.x or self.y != other.y
        return True

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        if isinstance(other, Direction):
            return Position(self.x + other.value[0], self.y + other.value[1])
        if isinstance(other, int):
            return Position(self.x + other, self.y + other)
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            return Position(self.x + other[0], self.y + other[1])
        raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")

    def __iadd__(self, other):
        if isinstance(other, Position):
            self.x += other.x
            self.y += other.y
            return self
        if isinstance(other, Direction):
            self.x += other.value[0]
            self.y += other.value[1]
            return self
        if isinstance(other, int):
            self.x += other
            self.y += other
            return self
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            self.x += other[0]
            self.y += other[1]
            return self
        raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")

    def __sub__(self, other):
        if isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        if isinstance(other, Direction):
            return Position(self.x - other.value[0], self.y - other.value[1])
        if isinstance(other, int):
            return Position(self.x - other, self.y - other)
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            return Position(self.x - other[0], self.y - other[1])
        raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")

    def __isub__(self, other):
        if isinstance(other, Position):
            self.x -= other.x
            self.y -= other.y
            return self
        if isinstance(other, Direction):
            self.x -= other.value[0]
            self.y -= other.value[1]
            return self
        if isinstance(other, int):
            self.x -= other
            self.y -= other
            return self
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            self.x -= other[0]
            self.y -= other[1]
            return self
        raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")

    def __mul__(self, other):
        if isinstance(other, Position):
            return Position(self.x * other.x, self.y * other.y)
        if isinstance(other, Direction):
            return Position(self.x * other.value[0], self.y * other.value[1])
        if isinstance(other, int):
            return Position(self.x * other, self.y * other)
        if isinstance(other, tuple) and isinstance(other[0], int) and isinstance(other[1], int):
            return Position(self.x * other[0], self.y * other[1])
        raise TypeError(f"{other} is no Position, Direction, int, or tuple[int, int]")

    def __hash__(self):
        return self.y * 10000000 + self.x

    def is_in_bounds(self, bounds) -> bool:
        if isinstance(bounds, Position):
            return 0 <= self.x < bounds.x and 0 <= self.y < bounds.y
        elif isinstance(bounds, list) and (isinstance(bounds[0], str) or isinstance(bounds[0], list)):
            return 0 <= self.x < len(bounds[0]) and 0 <= self.y < len(bounds)
        raise TypeError(f"{bounds} is no Position, list[list], or list[str]")

    def __str__(self):
        return f"Position({self.x}, {self.y})"

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError(f"Invalid index {index}")

    def __setitem__(self, index: int, value: int):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError(f"Invalid index {index}")


class Area:
    field: list
    bounds: Position

    def __init__(self, field: list):
        self.field = field
        self.bounds = Position(len(field[0]), len(field))

    def __getitem__(self, position: Position):
        return self.field[position.y][position.x]

    def __setitem__(self, position: Position, value):
        self.field[position.y][position.x] = value

    def safe_check(self, position: Position, value):
        return position.is_in_bounds(self.bounds) and self[position] == value

    def __iter__(self):
        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                yield Position(x, y)

    def is_in_bounds(self, position: Position) -> bool:
        return position.is_in_bounds(self.bounds)
