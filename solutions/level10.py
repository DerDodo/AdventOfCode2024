from util.data_util import convert_string_list
from util.file_util import read_input_file
from util.math_util import Area, Position, Direction
from util.run_util import RunTimer


def parse_input_file() -> Area:
    lines = read_input_file(10)
    field = convert_string_list(lines, int)
    return Area(field)


def get_trails(area: Area, position: Position) -> set[Position]:
    if area[position] == 9:
        return {position}

    next_value = area[position] + 1
    found_trails = set()
    if area.safe_check(position + Direction.North, next_value):
        found_trails.update(get_trails(area, position + Direction.North))
    if area.safe_check(position + Direction.East, next_value):
        found_trails.update(get_trails(area, position + Direction.East))
    if area.safe_check(position + Direction.South, next_value):
        found_trails.update(get_trails(area, position + Direction.South))
    if area.safe_check(position + Direction.West, next_value):
        found_trails.update(get_trails(area, position + Direction.West))

    return found_trails


def get_trails_all(area: Area, position: Position) -> int:
    if area[position] == 9:
        return 1

    next_value = area[position] + 1
    found_trails = 0
    if area.safe_check(position + Direction.North, next_value):
        found_trails += get_trails_all(area, position + Direction.North)
    if area.safe_check(position + Direction.East, next_value):
        found_trails += get_trails_all(area, position + Direction.East)
    if area.safe_check(position + Direction.South, next_value):
        found_trails += get_trails_all(area, position + Direction.South)
    if area.safe_check(position + Direction.West, next_value):
        found_trails += get_trails_all(area, position + Direction.West)

    return found_trails


def calc_trail_score(area: Area, position: Position, all_distinct: bool) -> int:
    if area[position] != 0:
        return 0
    elif all_distinct:
        return get_trails_all(area, position)
    else:
        return len(get_trails(area, position))


def level10() -> tuple[int, int]:
    area = parse_input_file()
    sum_trail_scores_1 = sum(map(lambda position: calc_trail_score(area, position, False), area))
    sum_trail_scores_2 = sum(map(lambda position: calc_trail_score(area, position, True), area))
    return sum_trail_scores_1, sum_trail_scores_2


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Sum trail scores: {level10()}")
    timer.print()


def test_level10():
    assert level10() == (36, 81)
