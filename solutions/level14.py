import math
from collections import defaultdict

from util.file_util import read_input_file
from util.math_util import Position
from util.run_util import RunTimer


class Robot:
    # runtime optimization
    # position: Position
    x: int
    y: int
    velocity: Position

    def __init__(self, line: str):
        parts = line.split(" ")
        position_parts = parts[0][2:].split(",")
        velocity_parts = parts[1][2:].split(",")
        self.x = int(position_parts[0])
        self.y = int(position_parts[1])
        self.velocity = Position(int(velocity_parts[0]), int(velocity_parts[1]))

    def __str__(self) -> str:
        return f"Robot({self.x}/{self.y}, {self.velocity})"


def parse_input_file() -> list[Robot]:
    lines = read_input_file(14)
    return list(map(Robot, lines))


def calc_safety_factor(robots: list[Robot], bounds: Position):
    quadrants = [0, 0, 0, 0]
    bounds //= 2

    for robot in robots:
        if robot.x == bounds.x or robot.y == bounds.y:
            continue
        x = 0 if robot.x < bounds.x else 1
        y = 0 if robot.y < bounds.y else 1
        quadrants[y * 2 + x] += 1

    return math.prod(quadrants)


def level14_1(bounds: Position) -> int:
    robots = parse_input_file()
    for robot in robots:
        robot.x = (robot.x + robot.velocity.x * 100) % bounds.x
        robot.y = (robot.y + robot.velocity.y * 100) % bounds.y
    return calc_safety_factor(robots, bounds)


def did_form_tree(robots: list[Robot]) -> bool:
    robot_dict = defaultdict(set)
    for robot in robots:
        robot_dict[robot.y].add(robot.x)

    neighbours = 0
    for robot in robots:
        x = robot.x
        y = robot.y
        if x in robot_dict[y - 1]:
            neighbours += 1
        if x in robot_dict[y + 1]:
            neighbours += 1
        if x + 1 in robot_dict[y]:
            neighbours += 1
        if x - 1 in robot_dict[y]:
            neighbours += 1
    return neighbours > len(robots) * 2


def level14_2(bounds: Position) -> int:
    robots = parse_input_file()
    for i in range(1, bounds.x * bounds.y + 1):
        robot_set = set()
        for robot in robots:
            robot.x = (robot.x + robot.velocity.x) % bounds.x
            robot.y = (robot.y + robot.velocity.y) % bounds.y
            robot_set.add(robot.y * 100000 + robot.x)

        if len(robot_set) == len(robots) and did_form_tree(robots):
            return i
    raise RuntimeError("Couldn't find solution")


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Safety factor: {level14_1(Position(101, 103))}")
    print(f"Seconds to christmas tree: {level14_2(Position(101, 103))}")
    timer.print()


def test_level14():
    assert level14_1(Position(11, 7)) == 12
    # No test for part 2 since it will not finish
