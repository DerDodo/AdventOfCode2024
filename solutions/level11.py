import math
from collections import defaultdict

from util.file_util import read_input_file
from util.math_util import count_digits
from util.run_util import RunTimer


def parse_input_file() -> list[int]:
    line = read_input_file(11)[0]
    return list(map(int, line.split(" ")))


def blink_for_stone(stone: int, blinks_left: int) -> int:
    if blinks_left == 0:
        return 1

    if blinks_left in blink_for_stone.blink_dict[stone]:
        return blink_for_stone.blink_dict[stone][blinks_left]

    num_digits = count_digits(stone)
    if stone == 0:
        num_stones = blink_for_stone(1, blinks_left - 1)
    elif num_digits % 2 == 0:
        split = int(math.pow(10, num_digits // 2))
        left = stone // split
        right = stone % split
        num_stones = blink_for_stone(left, blinks_left - 1) + blink_for_stone(right, blinks_left - 1)
    else:
        num_stones = blink_for_stone(stone * 2024, blinks_left - 1)

    blink_for_stone.blink_dict[stone][blinks_left] = num_stones
    return num_stones
blink_for_stone.blink_dict = defaultdict(dict)


def level11(num_blinks: int) -> int:
    stones = parse_input_file()
    return sum(map(lambda stone: blink_for_stone(stone, num_blinks), stones))


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Num stones after 25 blinks: {level11(25)}")
    print(f"Num stones after 75 blinks: {level11(75)}")
    timer.print()


def test_level11():
    assert level11(6) == 22
    assert level11(25) == 55312
