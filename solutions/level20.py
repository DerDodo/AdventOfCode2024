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


cheat_directions = [
    Direction.North * 2,
    Direction.East * 2,
    Direction.South * 2,
    Direction.West * 2,
    Direction.NorthEast,
    Direction.SouthEast,
    Direction.SouthWest,
    Direction.NorthWest
]


cheat_directions_big = [
    Direction.North * 2,
    Direction.North * 3,
    Direction.East * 2,
    Direction.East * 3,
    Direction.South * 2,
    Direction.South * 3,
    Direction.West * 2,
    Direction.West * 3,
    Direction.NorthEast,
    Direction.NorthEast + Direction.East,
    Direction.NorthEast + Direction.North,
    Direction.SouthEast,
    Direction.SouthEast + Direction.East,
    Direction.SouthEast + Direction.South,
    Direction.SouthWest,
    Direction.SouthWest + Direction.West,
    Direction.SouthWest + Direction.South,
    Direction.NorthWest,
    Direction.NorthWest + Direction.West,
    Direction.NorthWest + Direction.North
]


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
            for direction in cheat_directions:
                target = position + direction
                if self.is_in_bounds(target) and self[target] != WALL:
                    cheated_distance = self[target] - self[position] - 2
                    if cheated_distance >= cheat_target:
                        num_cheats += 1

        return num_cheats


def parse_input_file() -> Maze:
    return Maze(read_input_file(20))


def level20(cheat_target: int) -> tuple[int, int]:
    maze = parse_input_file()
    return maze.find_cheats(cheat_target), 0


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Available patterns: {level20(100)}")
    timer.print()


def test_level20():
    assert level20(64) == (1, 0)
    assert level20(38) == (3, 0)
    assert level20(20) == (5, 0)
    assert level20(12) == (8, 0)
    assert level20(10) == (10, 0)
    assert level20(8) == (14, 0)
    assert level20(6) == (16, 0)
    assert level20(4) == (30, 0)
    assert level20(2) == (44, 0)
