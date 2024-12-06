from enum import Enum

from util.file_util import read_input_file


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

    def copy(self):
        return Position(self.x, self.y)

    def get_hash(self) -> int:
        return self.y * 1000 + self.x

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False


class Field(Enum):
    Unvisited = "."
    Visited = "x"
    Obstacle = "#"
    GuardStart = "^"


class Facility:
    _field: list[list[Field]]
    _guard_start: Position

    def __init__(self, lines: list[str]):
        self._field = []
        for line in lines:
            self._field.append(list(map(Field, line)))
        self.init_guard_start()

    def init_guard_start(self):
        for y in range(0, len(self._field)):
            for x in range(0, len(self._field[0])):
                if self._field[y][x] == Field.GuardStart:
                    self._guard_start = Position(x, y)
                    self._field[y][x] = Field.Visited
                    return

    def is_out_of_bounds(self, position: Position) -> bool:
        return position.x < 0 or position.y < 0 or position.x >= len(self._field[0]) or position.y >= len(self._field)

    def get(self, position: Position) -> Field:
        return self._field[position.y][position.x]

    def visit(self, position: Position):
        self._field[position.y][position.x] = Field.Visited

    def get_guard_start(self) -> Position:
        return self._guard_start.copy()

    def get_num_visited(self) -> int:
        return sum(map(lambda line: sum(map(lambda x: 1 if x == Field.Visited else 0, line)), self._field))

    def get_size(self) -> int:
        return len(self._field) * len(self._field[0])

    def print(self):
        for line in self._field:
            print("".join(list(map(lambda x: x.value, line))))

    def set_obstacle(self, position: Position):
        self._field[position.y][position.x] = Field.Obstacle


class Guard:
    _facility: Facility
    _position: Position
    _direction: Direction
    _left_facility: bool

    def __init__(self, facility: Facility):
        self._facility = facility
        self._position = facility.get_guard_start()
        self._direction = Direction.North
        self._left_facility = False

    def walk(self):
        new_position = self._position.copy()
        new_position.move(self._direction)
        if self._facility.is_out_of_bounds(new_position):
            self._left_facility = True
        elif self._facility.get(new_position) == Field.Obstacle:
            self._direction = self._direction.turn_right()
        else:
            self._facility.visit(new_position)
            self._position = new_position

    def has_left_facility(self) -> bool:
        return self._left_facility

    def get_position(self) -> Position:
        return self._position.copy()

    def will_get_stuck(self) -> bool:
        history = set()
        while not self.has_left_facility():
            if self.get_history_hash() in history:
                return True
            history.add(self.get_history_hash())
            self.walk()
        return False

    def get_history_hash(self) -> int:
        return self._position.get_hash() * 10 + self._direction.value


def parse_input_file() -> tuple[Facility, Guard]:
    lines = read_input_file(6)
    facility = Facility(lines)
    guard = Guard(facility)
    return facility, guard


def level6_1() -> int:
    facility, guard = parse_input_file()
    while not guard.has_left_facility():
        guard.walk()
    return facility.get_num_visited()


def level6_2() -> int:
    original_facility, original_guard = parse_input_file()
    found_obstacles = set()
    tried_obstacles = set()
    while not original_guard.has_left_facility():
        original_guard.walk()
        position_hash = original_guard.get_position().get_hash()
        if original_guard.get_position() != original_facility.get_guard_start() and position_hash not in tried_obstacles:
            trial_facility, trial_guard = parse_input_file()
            trial_facility.set_obstacle(original_guard.get_position())
            tried_obstacles.add(position_hash)
            if trial_guard.will_get_stuck():
                found_obstacles.add(position_hash)
    return len(found_obstacles)


def level6() -> tuple[int, int]:
    return level6_1(), level6_2()


if __name__ == '__main__':
    print("Num visited fields, num loops: " + str(level6()))


def test_level6():
    assert (41, 6) == level6()
