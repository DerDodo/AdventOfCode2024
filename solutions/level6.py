from enum import Enum

from util.data_util import convert_string_list
from util.file_util import read_input_file
from util.math_util import Position, Direction, Area, position_and_direction_hash
from util.run_util import RunTimer


class Field(Enum):
    Free = "."
    Obstacle = "#"
    GuardStart = "^"


class Facility(Area):
    guard_start: Position

    def __init__(self, lines: list[str]):
        super().__init__(convert_string_list(lines, Field))
        self.guard_start = self.find_first(Field.GuardStart)

    def set_obstacle(self, position: Position):
        self[position] = Field.Obstacle

    def remove_obstacle(self, position: Position):
        self[position] = Field.Free


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
        new_position = Position(self.position.x + self.direction.x, self.position.y + self.direction.y)
        if not self.facility.is_in_bounds(new_position):
            self.left_facility = True
        elif self.facility[new_position] == Field.Obstacle:
            self.direction = self.direction.turn_right_90()
        else:
            self.position = new_position

    def will_get_stuck(self) -> bool:
        history = set()
        while not self.left_facility:
            if self in history:
                return True
            history.add(self)
            self.step()
        return False

    def __hash__(self) -> int:
        return position_and_direction_hash(self.position, self.direction)


def parse_input_file() -> tuple[Facility, Guard]:
    lines = read_input_file(6)
    facility = Facility(lines)
    guard = Guard(facility)
    return facility, guard


def level6_1() -> int:
    _, guard = parse_input_file()
    positions = set()
    while not guard.left_facility:
        positions.add(guard.position)
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

        if original_guard.position != original_facility.guard_start and original_guard.position not in tried_obstacles:
            trial_guard = Guard(trial_facility)
            trial_facility.set_obstacle(original_guard.position)
            tried_obstacles.add(original_guard.position)

            trial_guard.position = start_position
            trial_guard.direction = start_direction

            if trial_guard.will_get_stuck():
                found_obstacles.add(original_guard.position)

            trial_facility.remove_obstacle(original_guard.position)

    return len(found_obstacles)


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Num visited fields, num loops: {level6_1()}, {level6_2()}")
    timer.print()


def test_level6():
    assert (level6_1(), level6_2()) == (41, 6)
