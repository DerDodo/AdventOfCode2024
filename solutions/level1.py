from collections import defaultdict

from util.file_util import read_input_file_id, read_input_file


def process_line(line: str) -> int:
    digits = list(filter(str.isdigit, line))
    return int(digits[0]) * 10 + int(digits[-1])


def process_line_with_text(line: str) -> int:
    digits = []
    for idx, character in enumerate(line):
        if character.isdigit():
            digits.append(int(character))
        else:
            text_number = is_text_number(line, idx)
            if text_number:
                digits.append(text_number)

    return digits[0] * 10 + digits[-1]


def is_text_number(line: str, idx: int) -> int | None:
    search_texts = [
        ["one", 1],
        ["two", 2],
        ["three", 3],
        ["four", 4],
        ["five", 5],
        ["six", 6],
        ["seven", 7],
        ["eight", 8],
        ["nine", 9],
    ]

    for search_text in search_texts:
        if line[idx:idx + len(search_text[0])] == search_text[0]:
            return search_text[1]

    return None


def parse_input_file() -> tuple[list[int], list[int], dict[int, int]]:
    lines = read_input_file(1)
    parts_list = list(map(lambda line: line.split(" "), lines))

    left = list(map(lambda parts: int(parts[0]), parts_list))
    right = list(map(lambda parts: int(parts[-1]), parts_list))

    right_amount = defaultdict(int)
    for item in right:
        right_amount[item] += 1

    left.sort()
    right.sort()

    return left, right, right_amount


def level1() -> tuple[int, int]:
    left, right, right_amount = parse_input_file()
    total_distance = 0
    total_similarity = 0
    for i in range(len(left)):
        total_distance += abs(left[i] - right[i])
        total_similarity += left[i] * right_amount[left[i]]
    return total_distance, total_similarity

if __name__ == '__main__':
    print("Total distance: " + str(level1()))


def test_level1():
    assert (11, 31) == level1()
