import sys
from collections import defaultdict
from pathlib import Path

from aoc.utils.reporting import report


def parse(path):
    with open(path) as file:
        return [item for line in file for item in line.strip().split(",")]


def hash_item(item):
    res = 0
    for c in item:
        res += ord(c)
        res *= 17
        res %= 256

    return res


@report
def solve_part1(data):
    return sum([hash_item(item) for item in data])


@report
def solve_part2(data):
    boxes = defaultdict(dict)

    for item in data:
        oper = item.rstrip("-").split("=")
        match oper:
            case [lens]:
                boxes[hash_item(lens)].pop(lens, None)
            case [lens, f]:
                boxes[hash_item(lens)][lens] = int(f)

    res = 0
    for box, lenses in boxes.items():
        for i, f in enumerate(lenses.values(), 1):
            res += (box + 1) * i * f

    return res


def main():
    path = Path(sys.argv[1])
    data = parse(path)

    part1 = solve_part1(data)
    print(f"> solve_part1 | {part1:>20} |")

    part2 = solve_part2(data)
    print(f"> solve_part2 | {part2:>20} |")

    return 0


if __name__ == "__main__":
    sys.exit(main())
