import re

from util.file_util import read_input_file
from util.run_util import RunTimer


class Multiplication:
    left: int
    right: int

    def __init__(self, command: str):
        numbers = command[4:-1]
        self.left, self.right = map(int, numbers.split(","))

    def get_result(self) -> int:
        return self.left * self.right


def parse_input_file_with_no_conditionals() -> list[Multiplication]:
    lines = read_input_file(3)
    commands = []
    for line in lines:
        commands += re.findall("mul\\(\\d{1,3},\\d{1,3}\\)", line)

    return list(map(Multiplication, commands))


def parse_input_file_with_conditionals() -> list[Multiplication]:
    lines = read_input_file(3)
    commands = []
    for line in lines:
        commands += re.findall("mul\\(\\d{1,3},\\d{1,3}\\)|do\\(\\)|don't\\(\\)", line)

    multiplications = []
    do = True
    for command in commands:
        if command == "do()":
            do = True
        elif command == "don't()":
            do = False
        elif do:
            multiplications.append(Multiplication(command))

    return multiplications


def level3_1() -> int:
    commands = parse_input_file_with_no_conditionals()
    return sum(map(lambda command: command.get_result(), commands))


def level3_2() -> int:
    commands = parse_input_file_with_conditionals()
    return sum(map(lambda command: command.get_result(), commands))


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Calculation result: {level3_1()}, {level3_2()}")
    timer.print()


def test_level3():
    assert (level3_1(), level3_2()) == (161, 48)
