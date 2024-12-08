import math
from enum import Enum

from util.file_util import read_input_file


def count_digits(n):
    return math.floor(math.log10(abs(n))) + 1


class Operation(Enum):
    Add = 0
    Multiply = 1
    Concatenate = 2


class Equation:
    result: int
    numbers: list[int]

    def __init__(self, input: str):
        split = input.split(": ")
        self.result = int(split[0])
        self.numbers = list(map(int, split[1].split(" ")))

    def can_evaluate(self, operations: list[Operation]) -> bool:
        return self._can_evaluate(operations, self.numbers[0])

    def _can_evaluate(self, operations: list[Operation], result: int, i: int = 1) -> bool:
        if result > self.result:
            return False
        if i == len(self.numbers):
            return result == self.result
        for operation in operations:
            if operation == Operation.Add:
                new_result = result + self.numbers[i]
                if self._can_evaluate(operations, new_result, i + 1):
                    return True
            elif operation == Operation.Multiply:
                new_result = result * self.numbers[i]
                if self._can_evaluate(operations, new_result, i + 1):
                    return True
            elif operation == Operation.Concatenate:
                new_result = result * int(math.pow(10, count_digits(self.numbers[i]))) + self.numbers[i]
                if self._can_evaluate(operations, new_result, i + 1):
                    return True


def parse_input_file() -> list[Equation]:
    return list(map(Equation, read_input_file(7)))


def level7() -> tuple[int, int]:
    equations = parse_input_file()

    total_calibration_result_1 = 0
    total_calibration_result_2 = 0
    for equation in equations:
        if equation.can_evaluate([Operation.Add, Operation.Multiply]):
            total_calibration_result_1 += equation.result
        if equation.can_evaluate([Operation.Add, Operation.Multiply, Operation.Concatenate]):
            total_calibration_result_2 += equation.result

    return total_calibration_result_1, total_calibration_result_2


if __name__ == '__main__':
    print("Total calibration result: " + str(level7()))


def test_level7():
    assert level7() == (3749, 11387)
