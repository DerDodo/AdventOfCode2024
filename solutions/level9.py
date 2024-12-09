from util.file_util import read_input_file

FREE = -1


def parse_input_file() -> list[int]:
    blocks = read_input_file(9)[0]
    disc = []
    read_file = True
    file_id = 0
    for i in range(len(blocks)):
        disc.extend([file_id if read_file else FREE] * int(blocks[i]))
        if read_file:
            file_id += 1
        read_file = not read_file
    return disc

def find_next_free_space(disc: list[int]) -> int:
    for i in range(find_next_free_space.start, len(disc)):
        if disc[i] == FREE:
            find_next_free_space.start = i + 1
            return i
find_next_free_space.start = 0

def rearrange_disc_blocks(disc: list[int]):
    for i in range(len(disc) - 1, -1, -1):
        if disc[i] == FREE:
            continue

        next_free_space = find_next_free_space(disc)
        if next_free_space > i:
            return

        disc[next_free_space] = disc[i]
        disc[i] = FREE

type FreeSpaceMap = list[tuple[int, int]]

def map_free_space(disc:list[int]) -> FreeSpaceMap:
    free_spaces: FreeSpaceMap = []
    i = 0
    while i < len(disc):
        if disc[i] == FREE:
            free_space = 0
            while disc[i] == FREE and i < len(disc):
                free_space += 1
                i += 1
            free_spaces.append((i - free_space, free_space))
        else:
            i += 1
    return free_spaces

def find_first_free_space_for_file(free_spaces: FreeSpaceMap, file_size: int) -> int | None:
    for i in range(len(free_spaces)):
        if free_spaces[i][1] >= file_size:
            return i
    return None

def update_free_space_map(free_spaces: FreeSpaceMap, used_space_index: int, file_size: int):
    if free_spaces[used_space_index][1] == file_size:
        free_spaces.pop(used_space_index)
    else:
        free_spaces[used_space_index] = (free_spaces[used_space_index][0] + file_size, free_spaces[used_space_index][1] - file_size)

def rearrange_disc_files(disc: list[int]):
    free_spaces = map_free_space(disc)

    i = len(disc) - 1
    while i >= 0:
        if disc[i] == FREE:
            i -= 1
            continue

        # calc file size
        file_size = 0
        file_id = disc[i]
        while disc[i] == file_id and i >= 0:
            file_size += 1
            i -= 1

        # find free space
        free_space_i = find_first_free_space_for_file(free_spaces, file_size)
        if free_space_i is None:
            continue
        if free_spaces[free_space_i][0] > i:
            continue

        # move file
        for j in range(file_size):
            disc[free_spaces[free_space_i][0] + j] = file_id
            disc[i + j + 1] = FREE

        update_free_space_map(free_spaces, free_space_i, file_size)


def calc_checksum(disc: list[int]) -> int:
    checksum = 0
    for i in range(len(disc)):
        if disc[i] == FREE:
            continue
        checksum += disc[i] * i
    return checksum


def level9_1() -> int:
    disc = parse_input_file()
    rearrange_disc_blocks(disc)
    checksum = calc_checksum(disc)
    return checksum


def level9_2() -> int:
    disc = parse_input_file()
    rearrange_disc_files(disc)
    checksum = calc_checksum(disc)
    return checksum


def level9() -> tuple[int, int]:
    return level9_1(), level9_2()


if __name__ == '__main__':
    print(f"Checksum: {level9()}")


def test_level9():
    assert level9() == (1928, 2858)
