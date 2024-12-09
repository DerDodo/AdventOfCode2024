from collections import defaultdict

from util.file_util import read_input_file
from util.math_util import Position, Area
from util.run_util import RunTimer


def parse_input_file() -> tuple[Position, dict[str, list[Position]]]:
    field = Area(read_input_file(8))
    antennas = defaultdict(list)
    for position in field:
        if not field.safe_check(position, "."):
            antennas[field[position]].append(position)
    return field.bounds, antennas


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
    timer = RunTimer()
    print("Num anti nodes: " + str(level8()))
    timer.print()


def test_level8():
    assert level8() == (14, 34)
