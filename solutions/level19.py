from util.file_util import read_input_file
from util.run_util import RunTimer

def parse_input_file() -> tuple[list[str], list[str]]:
    lines = read_input_file(19)
    towels = lines[0].split(", ")
    return towels, lines[2:]


def calc_num_patterns(pattern: str, i: int, towels: list[str], result_cache: dict[int, int]) -> int:
    if i in result_cache:
        return result_cache[i]

    num_combinations = 0
    for towel in towels:
        new_i = i + len(towel)
        if pattern[i:new_i] == towel:
            if new_i == len(pattern):
                num_combinations += 1
            else:
                num_combinations += calc_num_patterns(pattern, new_i, towels, result_cache)
    result_cache[i] = num_combinations
    return num_combinations


def level19() -> tuple[int, int]:
    towels, patterns = parse_input_file()
    num_possible_patterns = 0
    num_total_combinations = 0
    for pattern in patterns:
        num_combinations = calc_num_patterns(pattern, 0, towels, dict())
        num_total_combinations += num_combinations
        if num_combinations > 0:
            num_possible_patterns += 1
    return num_possible_patterns, num_total_combinations


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Available patterns: {level19()}")
    timer.print()


def test_level19():
    assert level19() == (6, 16)
