from operator import mul, add

from util.file_util import read_input_file


def count_digits(n):
    if n < 10:
        return 1
    elif n < 100:
        return 2
    else:
        return 3
    # runtime optimization
    # return math.floor(math.log10(abs(n))) + 1


def concatenate(a: int, b: int) -> int:
    for _ in range(count_digits(b)):
        a *= 10
    return a + b
    # runtime optimization
    # return a * int(math.pow(10, count_digits(b))) + b


class Equation:
    result: int
    numbers: list[int]
    len_numbers: int

    def __init__(self, line: str):
        split = line.split(": ")
        self.result = int(split[0])
        self.numbers = list(map(int, split[1].split(" ")))
        # runtime optimization
        self.len_numbers = len(self.numbers)

    def can_evaluate(self, operations: list) -> bool:
        return self._can_evaluate(operations, self.numbers[0])

    def _can_evaluate(self, operations: list, result: int, i: int = 1) -> bool:
        if i == self.len_numbers:
            return result == self.result

        for operation in operations:
            new_result = operation(result, self.numbers[i])

            if new_result > self.result:
                return False

            if self._can_evaluate(operations, new_result, i + 1):
                return True


def parse_input_file() -> list[Equation]:
    return list(map(Equation, read_input_file(7)))


def level7() -> tuple[int, int]:
    equations = parse_input_file()

    total_calibration_result_1 = sum(map(lambda e: e.result if e.can_evaluate([add, mul]) else 0, equations))
    total_calibration_result_2 = sum(map(lambda e: e.result if e.can_evaluate([add, mul, concatenate]) else 0, equations))

    return total_calibration_result_1, total_calibration_result_2


if __name__ == '__main__':
    print("Total calibration result: " + str(level7()))


def test_level7():
    assert level7() == (3749, 11387)
