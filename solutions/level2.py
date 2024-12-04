from util.file_util import read_input_file


def is_valid_recursive(report: list[int], num_allowed_errors: int, is_ascending: bool) -> bool:
    if num_allowed_errors < 0:
        return False
    elif len(report) == 1:
        return True
    elif not report:
        return False

    distance = report[0] - report[1]
    if ((is_ascending and (distance < -3 or distance > -1)) or
            (not is_ascending and (distance < 1 or distance > 3))):
        return is_valid_recursive([report[0]] + report[2:], num_allowed_errors - 1, is_ascending)
    else:
        return is_valid_recursive(report[1:], num_allowed_errors, is_ascending)


def is_ascending(report: list[int]) -> bool:
    ascending_nums = 0
    descending_nums = 0
    for i in range(len(report) - 1):
        if report[i] < report[i + 1]:
            ascending_nums += 1
        elif report[i] > report[i + 1]:
            descending_nums += 1
    return ascending_nums > descending_nums


def is_valid(report: list[int], use_dampener: bool) -> bool:
    if len(report) == 1:
        return True
    elif not report:
        return False

    _is_ascending = is_ascending(report)

    if use_dampener:
        return (is_valid_recursive(report, 1, _is_ascending) or
                is_valid_recursive(report[1:], 0, _is_ascending))
    else:
        return is_valid_recursive(report, 0, _is_ascending)


def parse_input_file() -> list[list[int]]:
    lines = read_input_file(2)
    return list(map(lambda line: list(map(int, line.split(" "))), lines))


def level2() -> tuple[int, int]:
    reports = parse_input_file()
    num_valid_reports = sum(map(lambda report: is_valid(report, False), reports))
    num_valid_dampened_reports = sum(map(lambda report: is_valid(report, True), reports))
    return num_valid_reports, num_valid_dampened_reports


if __name__ == '__main__':
    print("Num safe reports: " + str(level2()))


def test_level2():
    assert (2, 4) == level2()
