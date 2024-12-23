from collections import defaultdict

from util.file_util import read_input_file
from util.math_util import Area, Direction
from util.run_util import RunTimer


def parse_input_file(file_id: int) -> Area:
    original_area = Area(read_input_file(12, file_id))
    area = Area(read_input_file(12, file_id))
    next_area_id = 0
    for position in original_area:
        if area[position] == original_area[position]:
            area.flood_fill(position, next_area_id)
            next_area_id += 1
    return area


def calc_area_fences(area: Area, value: int) -> tuple[int, dict[int, dict[Direction, list[int]]]]:
    fences: dict[int, dict[Direction, list[int]]] = defaultdict(lambda: defaultdict(list))
    sum_area = 0

    # runtime optimization
    for y in range(area.bounds.y):
        for x in range(area.bounds.x):
            if area.field[y][x] == value:
                sum_area += 1
                if not area.fast_safe_check(x + Direction.North.x, y + Direction.North.y, value):
                    fences[y][Direction.North].append(x)
                if not area.fast_safe_check(x + Direction.East.x, y + Direction.East.y, value):
                    fences[x][Direction.East].append(y)
                if not area.fast_safe_check(x + Direction.South.x, y + Direction.South.y, value):
                    fences[y][Direction.South].append(x)
                if not area.fast_safe_check(x + Direction.West.x, y + Direction.West.y, value):
                    fences[x][Direction.West].append(y)

    return sum_area, fences


def calc_fence_without_discount(fences: dict[int, dict[Direction, list[int]]]) -> int:
    return sum(map(lambda dim1: sum(map(lambda d: len(fences[dim1][d]), fences[dim1])), fences))


def calc_fence_with_discount(fences: dict[int, dict[Direction, list[int]]]) -> int:
    sides = 0
    for dimension_1 in fences:
        for direction in fences[dimension_1]:
            last_fence = -10000
            for dimension_2 in fences[dimension_1][direction]:
                if dimension_2 != last_fence + 1:
                    sides += 1
                last_fence = dimension_2
    return sides


def calc_fence_cost(area: Area, value: int, bulk_discount: bool) -> int:
    sum_area, fences = calc_area_fences(area, value)

    if bulk_discount:
        return sum_area * calc_fence_with_discount(fences)
    else:
        return sum_area * calc_fence_without_discount(fences)


def level12(file_id: int, bulk_discount: bool) -> int:
    area = parse_input_file(file_id)
    total_cost = 0
    for value in area.get_value_set():
        total_cost += calc_fence_cost(area, value, bulk_discount)
    return total_cost


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Price of fence: {level12(0, False)}, {level12(0, True)}")
    timer.print()


def test_level12():
    assert level12(0, False) == 140
    assert level12(1, False) == 772
    assert level12(2, False) == 1930
    assert level12(0, True) == 80
    assert level12(2, True) == 1206
    assert level12(3, True) == 236
    assert level12(4, True) == 368
