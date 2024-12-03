import sys


def read_input_file(level_id: int, strip: bool = True) -> list[str]:
    file_id = 1
    if "pytest" in sys.modules:
        file_id = 0

    return read_input_file_id(level_id, file_id, strip)


def read_input_file_id(level_id: int, file_id: int, strip: bool = True) -> list[str]:
    input_file = open(f"../input-files/level{level_id}-{file_id}.txt", "r")
    lines = input_file.readlines()
    if strip:
        lines = [line.strip() for line in lines]
    return lines
