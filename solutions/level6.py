from enum import Enum

from util.data_util import convert_string_list
from util.file_util import read_input_file
from util.math_util import Position, Direction, Area
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

    # runtime optimization
    # def set_obstacle(self, position: Position):
    def set_obstacle(self, x: int, y: int):
        self.field[y][x] = Field.Obstacle

    def remove_obstacle(self, x: int, y: int):
        self.field[y][x] = Field.Free


class Guard:
    facility: Facility
    # runtime optimization
    # position: Position
    position_x: int
    position_y: int
    direction: Direction
    left_facility: bool

    def __init__(self, facility: Facility):
        self.facility = facility
        self.position_x = facility.guard_start.x
        self.position_y = facility.guard_start.y
        self.direction = Direction.North
        self.left_facility = False

    def step(self):
        new_position_x = self.position_x + self.direction.x
        new_position_y = self.position_y + self.direction.y
        if not (0 <= new_position_x < self.facility.bounds.x and 0 <= new_position_y < self.facility.bounds.y):
            self.left_facility = True
        elif self.facility.field[new_position_y][new_position_x] == Field.Obstacle:
            self.direction = self.direction.turn_right_90()
        else:
            self.position_x = new_position_x
            self.position_y = new_position_y

    def will_get_stuck(self) -> bool:
        history = set()
        while not self.left_facility:
            hash_value = self.__hash__()
            if hash_value in history:
                return True
            history.add(hash_value)
            self.step()
        return False

    def position_hash(self) -> int:
        return self.position_y * 10000000 + self.position_x

    def __hash__(self) -> int:
        return self.position_hash() * 10 + self.direction.__hash__()


def parse_input_file() -> tuple[Facility, Guard]:
    lines = read_input_file(6)
    facility = Facility(lines)
    guard = Guard(facility)
    return facility, guard


def level6_1() -> int:
    _, guard = parse_input_file()
    positions = set()
    while not guard.left_facility:
        positions.add(guard.position_y * 1000000 + guard.position_x)
        guard.step()
    return len(positions)


def level6_2() -> int:
    original_facility, original_guard = parse_input_file()
    trial_facility = parse_input_file()[0]
    found_obstacles = set()
    tried_obstacles = set()
    while not original_guard.left_facility:
        start_position_x = original_guard.position_x
        start_position_y = original_guard.position_y
        start_direction = original_guard.direction
        original_guard.step()

        if ((original_guard.position_x != original_facility.guard_start.x or
             original_guard.position_y != original_facility.guard_start.y) and
                original_guard.position_hash() not in tried_obstacles):
            trial_guard = Guard(trial_facility)
            trial_facility.set_obstacle(original_guard.position_x, original_guard.position_y)
            tried_obstacles.add(original_guard.position_hash())

            trial_guard.position_x = start_position_x
            trial_guard.position_y = start_position_y
            trial_guard.direction = start_direction

            if trial_guard.will_get_stuck():
                found_obstacles.add(original_guard.position_hash())

            trial_facility.remove_obstacle(original_guard.position_x, original_guard.position_y)

    return len(found_obstacles)


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Num visited fields, num loops: {level6_1()}, {level6_2()}")
    timer.print()


def test_level6():
    assert (level6_1(), level6_2()) == (41, 6)
