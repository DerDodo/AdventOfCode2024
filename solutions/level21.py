from collections import defaultdict

from util.file_util import read_input_file
from util.math_util import Position, Direction
from util.run_util import RunTimer


def parse_input_file() -> list[str]:
    return read_input_file(21)


Option = list[Direction | str]


ILLEGAL = "!"


keypad = {
    "7": Position(0, 0),
    "8": Position(1, 0),
    "9": Position(2, 0),
    "4": Position(0, 1),
    "5": Position(1, 1),
    "6": Position(2, 1),
    "1": Position(0, 2),
    "2": Position(1, 2),
    "3": Position(2, 2),
    ILLEGAL: Position(0, 3),
    "0": Position(1, 3),
    "A": Position(2, 3)
}


directional_pad = {
    ILLEGAL: Position(0, 0),
    Direction.North: Position(1, 0),
    "A": Position(2, 0),
    Direction.West: Position(0, 1),
    Direction.South: Position(1, 1),
    Direction.East: Position(2, 1)
}


def get_buttons(start: Position, end: Position) -> list[tuple[Direction, int]]:
    result = []
    if end.y > start.y:
        result.append((Direction.South, end.y - start.y))
    elif end.y < start.y:
        result.append((Direction.North, start.y - end.y))
    if end.x > start.x:
        result.append((Direction.East, end.x - start.x))
    elif end.x < start.x:
        result.append((Direction.West, start.x - end.x))
    return result


A_B = [(0, 1), (1, 0)]


def create_options_with_a(start: Position, new_movements: list[tuple[Direction, int]], forbidden_spot: Position) -> list[Option]:
    if len(new_movements) == 2:
        options = []

        for a, b in A_B:
            if (start.x + new_movements[a][0].x * new_movements[a][1] != forbidden_spot.x or
                    start.y + new_movements[a][0].y * new_movements[a][1] != forbidden_spot.y):
                movements = [new_movements[a][0]] * new_movements[a][1] + [new_movements[b][0]] * new_movements[b][1] + ["A"]
                options.append(movements)

        return options
    elif len(new_movements) == 1:
        movements = [new_movements[0][0]] * new_movements[0][1] + ["A"]
        return [movements]
    elif len(new_movements) == 0:
        return [["A"]]
    else:
        raise ValueError(f"Invalid movements {new_movements}")


class Cache:
    values: dict[Direction | str, dict[Direction | str, list[Option]]]

    def __init__(self, pad: dict):
        self.values = defaultdict(dict)
        for x in pad:
            start = pad[x]
            for y in pad:
                end = pad[y]
                buttons = get_buttons(start, end)
                options = create_options_with_a(start, buttons, pad[ILLEGAL])
                self.values[start][end] = options


keypad_cache = Cache(keypad)
directional_cache = Cache(directional_pad)


def solve_code(code: str, num_robots: int) -> int:
    parts = create_options(list(code), keypad, keypad_cache)
    min_len = sum(map(lambda part: solve_codes_directional(part, num_robots), parts))
    return calc_complexity(code, min_len)


def solve_codes_directional(codes: list[Option], num_robots: int) -> int:
    if num_robots == 0:
        return min(map(len, codes))

    min_len = 9999999999999999999
    for code in codes:
        parts = create_options(code, directional_pad, directional_cache)
        min_parts_len = sum(map(lambda part: solve_codes_directional(part, num_robots - 1), parts))
        min_len = min(min_len, min_parts_len)
    return min_len


def create_options(code: Option, pad: dict, cache: Cache) -> list[list[Option]]:
    parts = []
    position = pad["A"]
    for button in code:
        target = pad[button]
        parts.append(cache.values[position][target])
        position = target
    return parts


def calc_complexity(code: str, min_len: int) -> int:
    print(f"{min_len} * {int(code.replace('A', ''))} = {min_len * int(code.replace('A', ''))}")
    return min_len * int(code.replace("A", ""))


def calc_complexity_old(code: str, patterns: list[Option]) -> int:
    pattern_len = min(map(lambda p: len(p.movements), patterns))
    print(f"{pattern_len} * {int(code.replace('A', ''))} = {pattern_len * int(code.replace('A', ''))}")
    return pattern_len * int(code.replace("A", ""))


def level21(num_robots: int) -> int:
    codes = parse_input_file()
    results = map(lambda c: solve_code(c, num_robots), codes)
    return sum(results)


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Complexity sum: { level21(2) }, { level21(25) }")
    timer.print()


def test_level21():
    assert level21(2) == 126384
    level21(11)
