import math
from enum import Enum

from util.file_util import read_input_file


def count_digits(n):
    return math.floor(math.log10(abs(n))) + 1


class Operation(Enum):
    Add = 0
    Multiply = 1
    Concatenate = 2


class Evaluation:
    result: int
    numbers: list[int]
    operations: list[Operation]

    def __init__(self, result: int, numbers: list[int], operations: list[Operation]):
        self.result = result
        self.numbers = numbers
        self.operations = operations

    def is_correct_with_incorrect_math(self):
        result = 0
        i = 0

        while i < len(self.numbers):
            operation = Operation.Add if i == 0 else self.operations[i - 1]
            if operation == Operation.Add:
                result += self.numbers[i]
            elif operation == Operation.Multiply:
                result *= self.numbers[i]
            elif operation == Operation.Concatenate:
                result *= int(math.pow(10, count_digits(self.numbers[i])))
                result += self.numbers[i]
            if result > self.result:
                return False
            i += 1
        return result == self.result

    def is_correct_with_correct_math(self):
        result = 0
        i = 0
        while i < len(self.numbers):
            temp_result = self.numbers[i]
            while i < len(self.operations) and self.operations[i] == Operation.Multiply:
                i += 1
                temp_result *= self.numbers[i]
            result += temp_result
            i += 1
        return result == self.result


class Equation:
    result: int
    numbers: list[int]

    def __init__(self, input: str):
        split = input.split(": ")
        self.result = int(split[0])
        self.numbers = list(map(int, split[1].split(" ")))

    def can_evaluate(self, operations: list[Operation]) -> bool:
        permutations = self.create_permutations(operations)
        for permutation in permutations:
            evaluation = Evaluation(self.result, self.numbers, permutation)
            if evaluation.is_correct_with_incorrect_math():
                return True
        return False

    def create_permutations(self, operations: list[Operation]) -> list[list[Operation]]:
        permutations = []
        for operation in operations:
            permutations.append([operation])
        while len(permutations[0]) != len(self.numbers) - 1:
            new_permutations = []
            for permutation in permutations:
                for operation in operations:
                    new_permutations.append([*permutation, operation])
            permutations = new_permutations
        return permutations

    def can_evaluate_recursive(self, operations: list[Operation]) -> bool:
        return self._can_evaluate_recursive(operations, self.numbers[0])

    def _can_evaluate_recursive(self, operations: list[Operation], result: int, i: int = 1) -> bool:
        if result > self.result:
            return False
        if i == len(self.numbers):
            return result == self.result
        for operation in operations:
            if operation == Operation.Add:
                new_result = result + self.numbers[i]
                if self._can_evaluate_recursive(operations, new_result, i + 1):
                    return True
            elif operation == Operation.Multiply:
                new_result = result * self.numbers[i]
                if self._can_evaluate_recursive(operations, new_result, i + 1):
                    return True
            elif operation == Operation.Concatenate:
                new_result = result * int(math.pow(10, count_digits(self.numbers[i]))) + self.numbers[i]
                if self._can_evaluate_recursive(operations, new_result, i + 1):
                    return True


def parse_input_file() -> list[Equation]:
    return list(map(Equation, read_input_file(7)))


def level7() -> tuple[int, int]:
    equations = parse_input_file()

    total_calibration_result_1 = 0
    total_calibration_result_2 = 0
    for equation in equations:
        if equation.can_evaluate_recursive([Operation.Add, Operation.Multiply]):
            total_calibration_result_1 += equation.result
        if equation.can_evaluate_recursive([Operation.Add, Operation.Multiply, Operation.Concatenate]):
            total_calibration_result_2 += equation.result

    return total_calibration_result_1, total_calibration_result_2


if __name__ == '__main__':
    print("Total calibration result: " + str(level7()))


def test_level7():
    assert level7() == (3749, 11387)
