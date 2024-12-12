from collections import defaultdict

from util.file_util import read_input_file_id
from util.math_util import Area, Direction, position_and_direction_hash, Position
from util.run_util import RunTimer


def parse_input_file(file_id: int) -> Area:
    original_area = Area(read_input_file_id(12, file_id))
    area = Area(read_input_file_id(12, file_id))
    next_area_id = 0
    for position in original_area:
        if area[position] == original_area[position]:
            area.flood_fill(position, next_area_id)
            next_area_id += 1
    return area


def calc_area_fences(area: Area, value: int) -> tuple[int, dict[int, dict[Direction, list[int]]]]:
    fences: dict[int, dict[Direction, list[int]]] = defaultdict(lambda: defaultdict(list))
    sum_area = 0

    for position in area:
        if area[position] == value:
            sum_area += 1
            if not area.safe_check(position + Direction.North, value):
                fences[position.y][Direction.North].append(position.x)
            if not area.safe_check(position + Direction.East, value):
                fences[position.x][Direction.East].append(position.y)
            if not area.safe_check(position + Direction.South, value):
                fences[position.y][Direction.South].append(position.x)
            if not area.safe_check(position + Direction.West, value):
                fences[position.x][Direction.West].append(position.y)

    return sum_area, fences


def calc_fence_cost(area: Area, value: int, bulk_discount: bool) -> int:
    sum_area, fences = calc_area_fences(area, value)

    if bulk_discount:
        sides = 0
        for dimension_1 in fences:
            for direction in fences[dimension_1]:
                last_fence = -10000
                for dimension_2 in fences[dimension_1][direction]:
                    if dimension_2 != last_fence + 1:
                        sides += 1
                    last_fence = dimension_2
        return sum_area * sides
    else:
        return sum_area * sum(map(lambda dim1: sum(map(lambda d: len(fences[dim1][d]), fences[dim1])), fences))

def level12(file_id: int, bulk_discount: bool) -> int:
    area = parse_input_file(file_id)
    total_cost = 0
    for value in area.get_value_set():
        total_cost += calc_fence_cost(area, value, bulk_discount)
    return total_cost


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Price of fence: {level12(5, False)}, {level12(5, True)}")
    timer.print()


def test_level12():
    assert level12(0, False) == 140
    assert level12(1, False) == 772
    assert level12(2, False) == 1930
    assert level12(0, True) == 80
    assert level12(2, True) == 1206
    assert level12(3, True) == 236
    assert level12(4, True) == 368
