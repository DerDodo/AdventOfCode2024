import math
from collections.abc import Callable

from util.file_util import read_input_file
from util.run_util import RunTimer


class Computer:
    A: int
    B: int
    C: int
    instruction_pointer: int
    operations = list[int]
    output = list[int]
    operation_lookup: list[Callable]

    def __init__(self, lines: list[str]):
        self.A = int(lines[0].split(" ")[-1])
        self.B = int(lines[1].split(" ")[-1])
        self.C = int(lines[2].split(" ")[-1])

        self.instruction_pointer = 0
        self.operations = list(map(int, lines[4].split(" ")[-1].split(",")))
        self.output = []

        self.operation_lookup = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv
        ]

    def get_output(self) -> str:
        return ",".join(map(str, self.output))

    def boot(self):
        while self.instruction_pointer < len(self.operations):
            instruction = self.operation_lookup[self.operations[self.instruction_pointer]]
            operand = self.operations[self.instruction_pointer + 1]
            if instruction(operand):
                self.instruction_pointer += 2

    def adv(self, operand: int) -> bool:
        denominator = math.pow(2, self.get_combo_operand(operand))
        self.A = int(self.A / denominator)
        return True

    def bxl(self, operand: int) -> bool:
        self.B = self.B ^ operand
        return True

    def bst(self, operand: int) -> bool:
        self.B = self.get_combo_operand(operand) % 8
        return True

    def jnz(self, operand: int) -> bool:
        if self.A != 0:
            self.instruction_pointer = operand
            return False
        return True

    def bxc(self, operand: int) -> bool:
        self.B = self.B ^ self.C
        return True

    def out(self, operand: int) -> bool:
        combo = self.get_combo_operand(operand)
        self.output.append(combo % 8)
        return True

    def bdv(self, operand: int) -> bool:
        denominator = math.pow(2, self.get_combo_operand(operand))
        self.B = int(self.A / denominator)
        return True

    def cdv(self, operand: int) -> bool:
        denominator = math.pow(2, self.get_combo_operand(operand))
        self.C = int(self.A / denominator)
        return True

    def get_combo_operand(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case _:
                raise ValueError(f"Invalid combo operand {operand}")


def parse_input_file() -> Computer:
    return Computer(read_input_file(17))


def level17_1() -> str:
    computer = parse_input_file()
    computer.boot()
    return computer.get_output()


def level17_2() -> int:
    # A initializes B and C every cycle from scratch. Reformulate the program to a formula taking only A as a
    # parameter. The cast to integer after the division forces us to check all 8 potential possibilities for
    # the potential A params. At least one of them will output your program.
    computer = parse_input_file()
    end_as = [0]
    for i in reversed(range(len(computer.operations))):
        out = computer.operations[i]
        new_end_as = []
        for end_a in end_as:
            for A in range(end_a * 8, (end_a + 1) * 8, 1):
                # Take a sheet of paper and transform your program to a formula
                # that calculates the output for a single variable A.
                test_out = ((((A % 8) ^ 1) ^ int(A / (math.pow(2, (A % 8) ^ 1)))) ^ 4) % 8
                if test_out == out:
                    new_end_as.append(A)
        end_as = new_end_as

    return end_as[0]


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Output: {level17_1()}")
    print(f"Initial value for A: {level17_2()}")
    timer.print()


def test_level17():
    assert level17_1() == "4,6,3,5,6,3,5,2,1,0"
    # No test for part 2 since the code is too specific
