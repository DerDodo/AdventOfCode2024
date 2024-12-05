from util.file_util import read_input_file


def parse_input_file() -> list[str]:
    return read_input_file(4)


directions = [
    [-1, -1],
    [0, -1],
    [1, -1],
    [-1, 0],
    [1, 0],
    [-1, 1],
    [0, 1],
    [1, 1],
]


def is_s(riddle: list[str], x: int, y: int) -> bool:
    if x < 0 or y < 0 or x >= len(riddle[0]) or y >= len(riddle):
        return False

    return riddle[y][x] == "S"


def is_as(riddle: list[str], x: int, y: int, dir_x: int, dir_y: int) -> bool:
    if x < 0 or y < 0 or x >= len(riddle[0]) or y >= len(riddle) or riddle[y][x] != "A":
        return False

    return is_s(riddle, x + dir_x, y + dir_y)


def is_mas(riddle: list[str], x: int, y: int, dir_x: int, dir_y: int) -> bool:
    if x < 0 or y < 0 or x >= len(riddle[0]) or y >= len(riddle) or riddle[y][x] != "M":
        return False

    return is_as(riddle, x + dir_x, y + dir_y, dir_x, dir_y)


def count_xmas(riddle: list[str]) -> int:
    num_xmas = 0
    for y in range(0, len(riddle)):
        for x in range(0, len(riddle[0])):
            if riddle[y][x] == "X":
                for direction in directions:
                    num_xmas += 1 if is_mas(riddle, x + direction[0], y + direction[1], direction[0], direction[1]) else 0
    return num_xmas


class Riddle:
    text: list[str]

    def __init__(self, text: list[str]):
        self.text = text

    def check(self, x: int, y: int, letter: str):
        if x < 0 or y < 0 or x >= len(self.text[0]) or y >= len(self.text):
            return False

        return self.text[y][x] == letter


def count_x_mas(riddle_str: list[str]) -> int:
    riddle = Riddle(riddle_str)
    num_x_mas = 0
    for y in range(1, len(riddle.text) - 1):
        for x in range(1, len(riddle.text[0]) - 1):
            if riddle.check(x, y, "A"):
                if (((riddle.check(x - 1, y - 1, "M") and riddle.check(x + 1, y + 1, "S")) or
                        (riddle.check(x + 1, y + 1, "M") and riddle.check(x - 1, y - 1, "S"))) and
                        ((riddle.check(x + 1, y - 1, "M") and riddle.check(x - 1, y + 1, "S")) or
                        (riddle.check(x - 1, y + 1, "M") and riddle.check(x + 1, y - 1, "S")))):
                    num_x_mas += 1
    return num_x_mas


def level4() -> tuple[int, int]:
    riddle = parse_input_file()
    return count_xmas(riddle), count_x_mas(riddle)


if __name__ == '__main__':
    print("Num XMAS: " + str(level4()))


def test_level4():
    assert (18, 9) == level4()
