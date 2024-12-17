import queue
from enum import Enum

from util.data_util import create_2d_list, convert_string_list
from util.file_util import read_input_file
from util.math_util import Position, Area, Direction, NEWSDirections
from util.run_util import RunTimer


class Field(Enum):
    Free = "."
    Wall = "#"
    Start = "S"
    End = "E"

NOT_FOUND = 1000000
ROTATION_COST = 1000
WALKING_COST = 1


class Maze(Area):
    paths: list[list[set[int]]]

    def __init__(self, lines: list[str]):
        super().__init__(convert_string_list(lines, Field))
        self.paths = create_2d_list(len(self.field[0]), len(self.field), set)
        self._a_star()

    def _a_star(self):
        path_score = NOT_FOUND
        paths_to_follow = self._a_star_init_paths()

        while not paths_to_follow.empty():
            score, position, direction = paths_to_follow.get()
            if self[position] == Field.End:
                path_score = min(path_score, score)
                self.paths[position.y][position.x].add(score)
                continue

            self.paths[position.y][position.x].add(score)

            for step in self._a_star_calc_next_steps(score, position, direction, path_score):
                paths_to_follow.put(step)

    def _a_star_init_paths(self) -> queue.PriorityQueue[tuple[int, Position, Direction]]:
        reindeer_start = self.find_first(Field.Start)
        self.paths[reindeer_start.y][reindeer_start.x].add(0)
        paths_to_follow = queue.PriorityQueue()
        if self[reindeer_start + Direction.East] != Field.Wall:
            paths_to_follow.put((WALKING_COST, reindeer_start + Direction.East, Direction.East))
        if self[reindeer_start + Direction.North] != Field.Wall:
            paths_to_follow.put((ROTATION_COST + WALKING_COST, reindeer_start + Direction.North, Direction.North))
        return paths_to_follow

    def _a_star_calc_next_steps(self, score: int, position: Position, direction: Direction, path_score: int) -> set[tuple[int, Position, Direction]]:
        next_steps = set()
        for d in filter(lambda newsd: newsd != -direction, NEWSDirections):
            new_score = score + WALKING_COST + (ROTATION_COST if d != direction else 0)
            new_position = position + d
            if self._a_star_can_continue(new_position, new_score, path_score):
                next_steps.add((new_score, position, d))
        return next_steps

    def _a_star_can_continue(self, position: Position, score: int, path_score: int):
        if self[position] != Field.Wall and score <= path_score:
            found_higher_score = False
            for s in self.paths[position.y][position.x]:
                if score < s + 1001:
                    found_higher_score = True
                    break
            return not self.paths[position.y][position.x] or found_higher_score
        return False

    def get_path_score(self) -> int:
        start_position = self.find_first(Field.End)
        return min(self.paths[start_position.y][start_position.x])

    def a_num_good_seats(self) -> int:
        start_position = self.find_first(Field.End)
        path_score = min(self.paths[start_position.y][start_position.x])

        positions = set()
        to_follow = {(start_position, path_score)}

        while to_follow:
            position, score = to_follow.pop()
            positions.add(position)
            for d in NEWSDirections:
                check_position = position + d
                for p in self.paths[check_position.y][check_position.x]:
                    if p == score - 1001 or p == score - 1:
                        to_follow.add((check_position, p))

        return len(positions)

    def print(self, path_positions: set[Position]):
        for y in range(len(self.field)):
            line = ""
            for x in range(len(self.field[y])):
                if self.field[y][x] == Field.Wall:
                    line += "#"
                elif self.field[y][x] == Field.Start:
                    line += "S"
                elif self.field[y][x] == Field.End:
                    line += "E"
                elif Position(x, y) in path_positions:
                    line += "O"
                else:
                    line += "."
            print(line)


def parse_input_file(file_id: int) -> Maze:
    lines = read_input_file(16, file_id)
    return Maze(lines)


def level16(file_id: int = 0) -> tuple[int, int]:
    maze = parse_input_file(file_id)
    return maze.get_path_score(), maze.a_num_good_seats()


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Num tokens: {level16()}")
    timer.print()


def test_level16():
    assert level16() == (7036, 45)
    assert level16(1) == (11048, 64)
