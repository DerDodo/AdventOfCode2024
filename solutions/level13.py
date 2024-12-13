from util.file_util import read_input_file
from util.math_util import Position
from util.run_util import RunTimer

class ClawMachine:
    button_a: Position
    button_b: Position
    price: Position

    def __init__(self, lines: list[str]):
        self.button_a = self.parse_input(lines[0], "+")
        self.button_b = self.parse_input(lines[1], "+")
        self.price = self.parse_input(lines[2], "=")

    def parse_input(self, line: str, delimiter: str) -> Position:
        parts = line.split(",")
        x = int(parts[0][parts[0].find(delimiter)+1:])
        y = int(parts[1][parts[1].find(delimiter)+1:])
        return Position(x, y)

    def calc_min_tokens(self, offset: int = 0) -> int:
        # Add the two vectors to each other, simplify the formula and restructure. Fortunately it returned the minimum result already.
        target_x = self.price.x + offset
        target_y = self.price.y + offset
        num_a = (target_y * self.button_b.x - self.button_b.y * target_x) / (self.button_a.y * self.button_b.x - self.button_b.y * self.button_a.x)
        if num_a == int(num_a):
            num_b = (target_x - self.button_a.x * num_a) / self.button_b.x
            return int(num_a) * 3 + int(num_b)
        else:
            return 0


def parse_input_file() -> list[ClawMachine]:
    lines = read_input_file(13)
    claw_machines = []
    for i in range(0, len(lines), 4):
        claw_machines.append(ClawMachine(lines[i:i+3]))
    return claw_machines


def level13() -> tuple[int, int]:
    claw_machines = parse_input_file()
    sum_direct = sum(map(lambda c: c.calc_min_tokens(), claw_machines))
    sum_with_offset = sum(map(lambda c: c.calc_min_tokens(10000000000000), claw_machines))
    return sum_direct, sum_with_offset


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Num tokens: {level13()}")
    timer.print()


def test_level13():
    assert level13() == (480, 875318608908)
