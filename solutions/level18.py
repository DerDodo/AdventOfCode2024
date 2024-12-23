from collections import deque
from enum import Enum

from util.data_util import create_2d_list
from util.file_util import read_input_file
from util.math_util import Position, Area, NEWSDirections
from util.run_util import RunTimer


class Field(Enum):
    Free = "."
    Corrupted = "#"


NOT_FOUND = -1


class Memory(Area):
    def __init__(self, corrupted_positions: list[Position], size: int):
        super().__init__(create_2d_list(size, size, Field.Free))

        for corrupted_position in corrupted_positions:
            self[corrupted_position] = Field.Corrupted

    def a_star(self) -> int:
        size = self.bounds.x
        paths = Area(create_2d_list(size, size, size * size * size))
        end = self.bounds - 1
        paths_to_follow = deque()
        paths_to_follow.append((0, Position(0, 0)))
        while paths_to_follow:
            score, position = paths_to_follow.popleft()
            if score < paths[position]:
                paths[position] = score

                if position == end:
                    return score

                paths_to_follow.extend(self._a_star_calc_next_steps(paths, score, position))
        return NOT_FOUND

    def _a_star_calc_next_steps(self, paths: Area, score: int, position: Position) -> set[tuple[int, Position]]:
        next_steps = set()
        for direction in NEWSDirections:
            new_score = score + 1
            new_position = position + direction
            if self.safe_check(new_position, Field.Free) and paths[new_position] > new_score:
                next_steps.add((new_score, new_position))
        return next_steps


def parse_input_file() -> list[Position]:
    return list(map(lambda line: Position(*map(int, line.split(","))), read_input_file(18)))


def level18_1(size: int, num_bytes_to_push: int) -> int:
    corrupted_positions = parse_input_file()[0:num_bytes_to_push]
    memory = Memory(corrupted_positions, size)
    return memory.a_star()


def level18_2(size: int) -> str:
    corrupted_positions = parse_input_file()
    lower_bound = 0
    upper_bound = len(corrupted_positions) - 1
    while upper_bound - lower_bound > 1:
        half_way = lower_bound + (upper_bound - lower_bound) // 2

        memory = Memory(corrupted_positions[0:half_way], size)
        result = memory.a_star()

        if result == NOT_FOUND:
            upper_bound = half_way
        else:
            lower_bound = half_way

    blocking_byte = corrupted_positions[upper_bound - 1]
    return f"{blocking_byte.x},{blocking_byte.y}"


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Shortest path: {level18_1(71, 1024)}")
    print(f"Blocking byte: {level18_2(71)}")
    timer.print()


def test_level18():
    assert level18_1(7, 12) == 22
    assert level18_2(7) == "6,1"
