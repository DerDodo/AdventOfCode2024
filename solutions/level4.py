from util.file_util import read_input_file
from util.math_util import Position, Direction, Area


def parse_input_file() -> Area:
    return Area(read_input_file(4))


def is_mas(riddle: Area, position: Position, direction: Direction) -> bool:
    return (riddle.safe_check(position, "M") and
            riddle.safe_check(position + direction, "A") and
            riddle.safe_check(position + direction * 2, "S"))


def count_xmas(riddle: Area) -> int:
    num_xmas = 0
    for position in riddle:
        if riddle.safe_check(position, "X"):
            num_xmas += sum(is_mas(riddle, position + direction, direction) for direction in Direction)
    return num_xmas


def is_x_mas(riddle: Area, pos: Position):
    return (riddle.safe_check(pos, "A") and
            ((riddle.safe_check(pos + Direction.NorthWest, "M") and riddle.safe_check(pos + Direction.SouthEast, "S")) or
             (riddle.safe_check(pos + Direction.SouthEast, "M") and riddle.safe_check(pos + Direction.NorthWest, "S"))) and
            ((riddle.safe_check(pos + Direction.NorthEast, "M") and riddle.safe_check(pos + Direction.SouthWest, "S")) or
             (riddle.safe_check(pos + Direction.SouthWest, "M") and riddle.safe_check(pos + Direction.NorthEast, "S"))))


def count_x_mas(riddle: Area) -> int:
    num_x_mas = 0
    for position in riddle:
        if is_x_mas(riddle, position):
            num_x_mas += 1
    return num_x_mas


def level4() -> tuple[int, int]:
    riddle = parse_input_file()
    return count_xmas(riddle), count_x_mas(riddle)


if __name__ == '__main__':
    print("Num XMAS: " + str(level4()))


def test_level4():
    assert level4() == (18, 9)
