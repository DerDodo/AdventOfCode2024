from collections import defaultdict

from util.file_util import read_input_file
from util.math_util import Position, Direction
from util.run_util import RunTimer


def parse_input_file() -> list[int]:
    return list(map(int, read_input_file(22)))


def calc_next_numbers(n: int, numbers: int) -> tuple[int, list[int]]:
    one_digits = [n % 10]
    for _ in range(numbers):
        n = ((n * 64) ^ n) % 16777216
        n = ((n // 32) ^ n) % 16777216
        n = ((n * 2048) ^ n) % 16777216
        one_digits.append(n % 10)
    return n, one_digits


def calc_price_diffs(prices: list[int]) -> list[int]:
    price_diffs = []
    for i in range(len(prices) - 1):
        price_diffs.append(prices[i + 1] - prices[i])
    return price_diffs


def calc_price_dicts(prices: list[int], price_diffs: list[int]) -> dict[int, list[list[int]]]:
    return dict()



def level22() -> int:
    numbers = parse_input_file()
    results = list(map(lambda n: calc_next_numbers(n, 2000), numbers))
    price_diffs = list(map(lambda r: calc_price_diffs(r[1]), results))
    price_dicts = list(map(lambda i: calc_price_dicts(results[i][1], price_diffs[i]), range(len(price_diffs[0]))))
    return sum(map(lambda r: r[0], results))


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Complexity sum: { level22() }")
    timer.print()


def test_level22():
    assert level22() == 37327623
