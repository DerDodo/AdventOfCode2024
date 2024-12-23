from collections import defaultdict

from util.file_util import read_input_file
from util.math_util import Position, Direction
from util.run_util import RunTimer


def parse_input_file() -> list[str]:
    return read_input_file(21)


class Option:
    commands: list[Direction | str]
    hash: int

    def __init__(self, commands: list[Direction | str]):
        self.commands = commands
        self.hash = 0
        for i in reversed(range(len(commands) - 1)):
            self.hash = self.hash * 9 + commands[i].hash_value


class OptionList:
    options: list[Option]
    hash: int

    def __init__(self, options: list[Option]):
        self.options = options
        self.hash = 0
        for i in reversed(range(len(options))):
            self.hash = self.hash * 100000 + options[i].hash


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


def solve_code(code: str, num_robots: int) -> int:
    parts = create_options(list(code), keypad)
    min_len = sum(map(lambda part: solve_codes_directional(part, num_robots), parts))
    return calc_complexity(code, min_len)


solution_cache: dict[int, dict[int, int]] = defaultdict(dict)


def solve_codes_directional(codes: OptionList, num_robots: int) -> int:
    if num_robots == 0:
        return min(map(lambda option: len(option.commands), codes.options))

    if codes.hash in solution_cache[num_robots]:
        return solution_cache[num_robots][codes.hash]

    min_len = 9999999999999999999
    for code in codes.options:
        parts = create_options(code.commands, directional_pad)
        min_parts_len = sum(map(lambda part: solve_codes_directional(part, num_robots - 1), parts))
        min_len = min(min_len, min_parts_len)
    solution_cache[num_robots][codes.hash] = min_len
    return min_len


def create_options(code: list, pad: dict) -> list[OptionList]:
    parts = []
    position = pad["A"]
    for button in code:
        target = pad[button]
        buttons = get_buttons(position, target)
        options = create_options_with_a(position, buttons, pad[ILLEGAL])
        parts.append(options)
        position = target
    return parts


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


def create_options_with_a(start: Position, new_movements: list[tuple[Direction, int]], forbidden_spot: Position) -> OptionList:
    if len(new_movements) == 2:
        options = []

        for a, b in [(0, 1), (1, 0)]:
            if (start.x + new_movements[a][0].x * new_movements[a][1] != forbidden_spot.x or
                    start.y + new_movements[a][0].y * new_movements[a][1] != forbidden_spot.y):
                movements = [new_movements[a][0]] * new_movements[a][1] + [new_movements[b][0]] * new_movements[b][1] + ["A"]
                options.append(Option(movements))

        return OptionList(options)
    elif len(new_movements) == 1:
        movements = [new_movements[0][0]] * new_movements[0][1] + ["A"]
        return OptionList([Option(movements)])
    elif len(new_movements) == 0:
        return OptionList([Option(["A"])])
    else:
        raise ValueError(f"Invalid movements {new_movements}")


def calc_complexity(code: str, min_len: int) -> int:
    return min_len * int(code.replace("A", ""))


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
    # runtime check
    level21(25)
