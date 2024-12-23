from collections import defaultdict

from util.file_util import read_input_file
from util.run_util import RunTimer


def parse_input_file() -> dict[str, set[str]]:
    pairs = list(map(lambda line: line.split("-"), read_input_file(23)))
    connections = defaultdict(set)

    for pair in pairs:
        connections[pair[0]].add(pair[1])
        connections[pair[1]].add(pair[0])

    return connections


def create_id(partners: list[str]) -> str:
    return ",".join(sorted(partners))


def create_initial_groups(connections: dict[str, set[str]]) -> list[list[str]]:
    new_groups: set[str] = set()

    for key in connections:
        for partner in connections[key]:
            new_groups.add(create_id([key, partner]))

    return list(map(lambda text: text.split(","), new_groups))


def calc_new_groups(groups: list[list[str]], connections: dict[str, set[str]]) -> list[list[str]]:
    new_groups: set[str] = set()
    len_group = len(groups[0])

    for group in groups:
        new_partners = defaultdict(int)

        for device in group:
            for new_partner in connections[device]:
                new_partners[new_partner] += 1

        for new_partner, value in new_partners.items():
            if value == len_group:
                new_groups.add(create_id([*group, new_partner]))

    return list(map(lambda text: text.split(","), new_groups))


def level23() -> tuple[int, str]:
    connections = parse_input_file()

    groups = create_initial_groups(connections)
    num_threesomes = 0

    for _ in range(len(connections)):
        groups = calc_new_groups(groups, connections)

        if len(groups) == 1:
            return num_threesomes, create_id(groups[0])

        if len(groups[0]) == 3:
            num_threesomes = len(list(filter(lambda group: group[0][0] == "t" or group[1][0] == "t" or group[2][0] == "t", groups)))

    raise ValueError("Didn't find password")


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Potential networks, Wi-Fi password: { level23() }")
    timer.print()


def test_level23():
    assert level23() == (7, "co,de,ka,ta")
