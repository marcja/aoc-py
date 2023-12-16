import sys
from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from time import perf_counter


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


def solve_part1(data):
    return sum([hash_item(item) for item in data])


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
