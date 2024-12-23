from collections import defaultdict

from util.file_util import read_input_file
from util.run_util import RunTimer


def parse_input_file(file_id: int) -> list[int]:
    return list(map(int, read_input_file(22, file_id)))


def calc_next_numbers(n: int, numbers: int) -> tuple[int, list[int]]:
    one_digits = [n % 10]
    for _ in range(numbers):
        n = ((n << 6) ^ n) % 16777216
        n = ((n >> 5) ^ n) % 16777216
        n = ((n << 11) ^ n) % 16777216
        one_digits.append(n % 10)
    return n, one_digits


def calc_price_diffs(prices: list[int]) -> list[int]:
    price_diffs = []
    for i in range(len(prices) - 1):
        price_diffs.append(prices[i + 1] - prices[i])
    return price_diffs


StopCommand = tuple[int, int]


def calc_stop_commands(prices: list[int], price_diffs: list[int]) -> list[StopCommand]:
    stop_commands = []
    for i in range(len(price_diffs) - 3):
        hash_value = (price_diffs[i] + 10) * 8000 + (price_diffs[i+1] + 10) * 400 + (price_diffs[i+2] + 10) * 20 + (price_diffs[i+3] + 10)
        stop_commands.append((prices[i + 4], hash_value))
    return stop_commands


def level22(file_id: int = 0) -> tuple[int, int]:
    numbers = parse_input_file(file_id)
    results = list(map(lambda n: calc_next_numbers(n, 2000), numbers))
    all_price_diffs = list(map(lambda r: calc_price_diffs(r[1]), results))
    all_stop_commands = list(map(lambda i: calc_stop_commands(results[i][1], all_price_diffs[i]), range(len(all_price_diffs))))

    prices = defaultdict(int)
    for stop_commands in all_stop_commands:
        used = set()
        for stop_command in stop_commands:
            if stop_command[1] not in used:
                prices[stop_command[1]] += stop_command[0]
                used.add(stop_command[1])

    return sum(map(lambda r: r[0], results)), max(prices.values())


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Secret number sum, bananas: { level22() }")
    timer.print()


def test_level22():
    assert level22(0)[0] == 37327623
    assert level22(1)[1] == 23
