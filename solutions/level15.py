from collections import defaultdict
from enum import Enum

from util.file_util import read_input_file_id
from util.math_util import Position, Area, Direction
from util.run_util import RunTimer


class Field(Enum):
    Free = "."
    Wall = "#"
    Box = "O"
    Robot = "@"
    WideBoxLeft = "["
    WideBoxRight = "]"


class Warehouse(Area):
    movements: list[Direction]
    robot: Position

    def __init__(self, area_lines: list[str], movements: list[str]):
        super().__init__(list(map(lambda line: list(map(Field, line)), area_lines)))
        self.movements = list(map(Direction.from_arrow, "".join(movements)))
        self.robot = self.find_first(Field.Robot)

    def move_robot(self, direction: Direction):
        if direction == Direction.East or direction == Direction.West:
            self.move_robot_horizontal(direction)
        elif direction == Direction.North or direction == Direction.South:
            self.move_robot_vertical(direction)
        else:
            raise ValueError(f"Invalid movement direction {direction}")

    def move_robot_horizontal(self, direction: Direction):
        check_position = self.robot.copy() + direction

        while self[check_position] == Field.WideBoxLeft or self[check_position] == Field.WideBoxRight or self[check_position] == Field.Box:
            check_position += direction

        if self[check_position] == Field.Free:
            while self[check_position] != Field.Robot:
                self[check_position] = self[check_position - direction]
                check_position = check_position - direction
            self[check_position] = Field.Free
            self.robot += direction
        elif self[check_position] == Field.Wall:
            return
        else:
            raise ValueError(f"Invalid field {check_position} = '{self[check_position]}'")

    def move_robot_vertical(self, direction: Direction):
        move_tiles = defaultdict(set)
        start_y = self.robot.y
        y = self.robot.y
        move_tiles[self.robot.y].add(self.robot.x)
        while move_tiles[y]:
            move_tile_set = move_tiles[y]
            y += direction.y

            for move_tile_x in move_tile_set:
                if self.field[y][move_tile_x] == Field.WideBoxLeft:
                    move_tiles[y].add(move_tile_x)
                    move_tiles[y].add(move_tile_x + 1)
                elif self.field[y][move_tile_x] == Field.WideBoxRight:
                    move_tiles[y].add(move_tile_x)
                    move_tiles[y].add(move_tile_x - 1)
                elif self.field[y][move_tile_x] == Field.Box:
                    move_tiles[y].add(move_tile_x)
                elif self.field[y][move_tile_x] == Field.Wall:
                    return
                elif self.field[y][move_tile_x] != Field.Free:
                    raise ValueError(f"Invalid field {move_tile_x}/{y} = '{self.field[y][move_tile_x]}'")

        for move_to_y in range(y, start_y - direction.y, -direction.y):
            move_from_y = move_to_y - direction.y
            for x in move_tiles[move_from_y]:
                self.field[move_to_y][x] = self.field[move_from_y][x]
                self.field[move_from_y][x] = Field.Free

        self.robot += direction

    def calc_gps_sum(self) -> int:
        sum_gps = 0
        for position in self:
            if self[position] == Field.WideBoxLeft or self[position] == Field.Box:
                sum_gps += position.y * 100 + position.x
        return sum_gps


def make_wide_warehouse(lines: list[str]) -> list[str]:
    new_lines = []
    for line in lines:
        new_line = ""
        for char in line:
            if char == Field.Wall.value or char == Field.Free.value:
                new_line += char * 2
            elif char == Field.Box.value:
                new_line += Field.WideBoxLeft.value + Field.WideBoxRight.value
            elif char == Field.Robot.value:
                new_line += Field.Robot.value + Field.Free.value
            else:
                raise ValueError(f"Invalid character '{char}'")
        new_lines.append(new_line)

    return new_lines


def parse_input_file(file_id: int, wide_map: bool) -> Warehouse:
    lines = read_input_file_id(15, file_id)
    split = lines.index("")
    if wide_map:
        return Warehouse(make_wide_warehouse(lines[0:split]), lines[split+1:])
    else:
        return Warehouse(lines[0:split], lines[split+1:])


def level15(file_id: int, wide_map: bool) -> int:
    warehouse = parse_input_file(file_id, wide_map)
    for movement in warehouse.movements:
        warehouse.move_robot(movement)
    return warehouse.calc_gps_sum()


if __name__ == '__main__':
    timer = RunTimer()
    print(f"GPS sum: {level15(2, False)}")
    print(f"GPS sum (wide): {level15(2, True)}")
    timer.print()


def test_level15():
    assert level15(0, False) == 2028
    assert level15(1, False) == 10092
    assert level15(1, True) == 9021
