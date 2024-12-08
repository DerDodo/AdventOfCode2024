from enum import Enum

from util.file_util import read_input_file
from util.math_util import Position, Direction


class Field(Enum):
    Free = "."
    Obstacle = "#"
    GuardStart = "^"


class Facility:
    field: list[list[Field]]
    bounds: Position
    guard_start: Position

    def __init__(self, lines: list[str]):
        self.field = [list(map(Field, line)) for line in lines]
        self.bounds = Position(len(lines[0]), len(lines))

        for y in range(0, len(self.field)):
            for x in range(0, len(self.field[0])):
                if self.field[y][x] == Field.GuardStart:
                    self.guard_start = Position(x, y)
                    return

    def get(self, position: Position) -> Field:
        return self.field[position.y][position.x]

    def set_obstacle(self, position: Position):
        self.field[position.y][position.x] = Field.Obstacle

    def remove_obstacle(self, position: Position):
        self.field[position.y][position.x] = Field.Free


class Guard:
    facility: Facility
    position: Position
    direction: Direction
    left_facility: bool

    def __init__(self, facility: Facility):
        self.facility = facility
        self.position = facility.guard_start
        self.direction = Direction.North
        self.left_facility = False

    def step(self):
        new_position = Position(self.position.x, self.position.y)
        new_position.move(self.direction)
        if not new_position.is_in_bounds(self.facility.bounds):
            self.left_facility = True
        elif self.facility.get(new_position) == Field.Obstacle:
            self.direction = self.direction.turn_right()
        else:
            self.position = new_position

    def will_get_stuck(self) -> bool:
        history = set()
        while not self.left_facility:
            if self.get_history_hash() in history:
                return True
            history.add(self.get_history_hash())
            self.step()
        return False

    def get_history_hash(self) -> int:
        return self.position.get_hash() * 10 + self.direction.value


def parse_input_file() -> tuple[Facility, Guard]:
    lines = read_input_file(6)
    facility = Facility(lines)
    guard = Guard(facility)
    return facility, guard


def level6_1() -> int:
    _, guard = parse_input_file()
    positions = set()
    while not guard.left_facility:
        positions.add(guard.position.get_hash())
        guard.step()
    return len(positions)


def level6_2() -> int:
    original_facility, original_guard = parse_input_file()
    trial_facility = parse_input_file()[0]
    found_obstacles = set()
    tried_obstacles = set()
    while not original_guard.left_facility:
        start_position = original_guard.position
        start_direction = original_guard.direction
        original_guard.step()

        position_hash = original_guard.position.get_hash()
        if original_guard.position != original_facility.guard_start and position_hash not in tried_obstacles:
            trial_guard = Guard(trial_facility)
            trial_facility.set_obstacle(original_guard.position)
            tried_obstacles.add(position_hash)

            trial_guard.position = start_position
            trial_guard.direction = start_direction

            if trial_guard.will_get_stuck():
                found_obstacles.add(position_hash)

            trial_facility.remove_obstacle(original_guard.position)

    return len(found_obstacles)


if __name__ == '__main__':
    print(f"Num visited fields, num loops: {level6_1()}, {level6_2()}")


def test_level6():
    assert (41, 6) == (level6_1(), level6_2())
