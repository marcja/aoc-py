import re
import sys
from datetime import timedelta
from itertools import chain, repeat
from math import lcm
from pathlib import Path
from time import perf_counter


def parse(path):
    NODEX = re.compile(r"([0-9A-Z]{3})")
    with open(path) as file:
        lines = file.readlines()
        turns = lines[0].strip()
        nodes = {}
        for line in lines[2:]:
            start, left, right = NODEX.findall(line)
            nodes[start] = (left, right)

        return turns, nodes


def move(nodes, place, turns):
    for i, turn in enumerate(chain.from_iterable(repeat(list(turns)))):
        if place.endswith("Z"):
            return i
        if turn == "L":
            place = nodes[place][0]
        else:
            place = nodes[place][1]


def solve_part1(data):
    turns, nodes = data
    return move(nodes, "AAA", turns)


def solve_part2(data):
    turns, nodes = data
    dists = [move(nodes, p, turns) for p in nodes.keys() if p.endswith("A")]
    return lcm(*dists)


def main():
    path = Path(sys.argv[1])
    data = parse(path)

    time0 = perf_counter()
    part1 = solve_part1(data)
    time1 = perf_counter()
    part2 = solve_part2(data)
    time2 = perf_counter()

    print()
    print(f"part1 | {timedelta(seconds=time1 - time0)} | {part1:>20} |")
    print(f"part2 | {timedelta(seconds=time2 - time1)} | {part2:>20} |")

    return 0


if __name__ == "__main__":
    sys.exit(main())
