from collections import defaultdict

from util.file_util import read_input_file
from util.math_util import Position


def parse_input_file() -> tuple[Position, dict[str, list[Position]]]:
    lines = read_input_file(8)
    bounds = Position(len(lines[0]), len(lines))
    antennas = defaultdict(list)
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] != ".":
                antennas[lines[y][x]].append(Position(x, y))
    return bounds, antennas


def level8() -> tuple[int, int]:
    bounds, antenna_dict = parse_input_file()

    anti_nodes = set()
    resonant_anti_nodes = set()
    for antenna_type, antennas in antenna_dict.items():
        for i in range(len(antennas) - 1):
            for j in range(i + 1, len(antennas)):
                diff = antennas[j] - antennas[i]
                anti_nodes.add(antennas[i] - diff)
                anti_nodes.add(antennas[j] + diff)

                anti_node = antennas[i]
                while anti_node.is_in_bounds(bounds):
                    resonant_anti_nodes.add(anti_node)
                    anti_node = anti_node - diff

                anti_node = antennas[j]
                while anti_node.is_in_bounds(bounds):
                    resonant_anti_nodes.add(anti_node)
                    anti_node = anti_node + diff

    num_valid_anti_nodes = sum(a.is_in_bounds(bounds) for a in anti_nodes)

    return num_valid_anti_nodes, len(resonant_anti_nodes)


if __name__ == '__main__':
    print("Num anti nodes: " + str(level8()))


def test_level8():
    assert level8() == (14, 34)
