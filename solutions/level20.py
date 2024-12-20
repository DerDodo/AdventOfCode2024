from util.file_util import read_input_file
from util.math_util import Area, NEWSDirections, Direction, Position
from util.run_util import RunTimer


WALL = -2
UNDEFINED = -1


maze_dict = {
    "#": WALL,
    ".": UNDEFINED,
    "S": 0,
    "E": UNDEFINED
}


def create_cheat_matrix(seconds: int) -> set[Position]:
    cheat_locations = set()
    last_locations = {Position(0, 0)}
    for _ in range(seconds):
        new_locations = set()
        for location in last_locations:
            for direction in NEWSDirections:
                new_locations += location + direction
        cheat_locations.update(new_locations)
        last_locations = new_locations
    cheat_locations.remove(Position(0, 0))
    for direction in NEWSDirections:
        cheat_locations.remove(Position(direction.x, direction.y))
    return cheat_locations


class Maze(Area):
    start: Position
    end: Position

    def __init__(self, lines: list[str]):
        super().__init__(list(map(lambda l: list(map(lambda v: maze_dict[v], l)), lines)))
        string_field = Area(lines)
        self.start = string_field.find_first("S")
        self.end = string_field.find_first("E")
        self.init_track()

    def init_track(self):
        position = self.start
        steps = 0

        while position != self.end:
            self[position] = steps
            steps += 1
            for direction in NEWSDirections:
                if self[position + direction] == UNDEFINED:
                    position += direction
                    break
        self[self.end] = steps

    def find_cheats(self, cheat_target: int) -> int:
        num_cheats = 0
        for position in self:
            num_cheats += self.get_num_cheats(position, cheat_target)
        return num_cheats

    def get_num_cheats(self, position: Position, cheat_target: int) -> int:
        num_cheats = 0
        if self[position] != WALL:
            for direction in :
                target = position + direction
                if self.is_in_bounds(target) and self[target] != WALL:
                    cheated_distance = self[target] - self[position] - 2
                    if cheated_distance >= cheat_target:
                        num_cheats += 1

        return num_cheats


def parse_input_file() -> Maze:
    return Maze(read_input_file(20))


def level20(cheat_target: int, cheat_duration: int) -> int:
    maze = parse_input_file()
    cheat_matrix_1 = create_cheat_matrix(cheat_duration)
    return maze.find_cheats(cheat_target)


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Available patterns: {level20(100, create_cheat_matrix(2))}")
    timer.print()


def test_level20():
    assert level20(64, 2) == 1
    assert level20(38, 2) == 3
    assert level20(20, 2) == 5
    assert level20(12, 2) == 8
    assert level20(10, 2) == 10
    assert level20(8, 2) == 14
    assert level20(6, 2) == 16
    assert level20(4, 2) == 30
    assert level20(2, 2) == 44
