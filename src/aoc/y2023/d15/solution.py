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
    boxes = defaultdict(list)

    for item in data:
        oper = item.rstrip("-").split("=")
        match oper:
            case [lens]:
                bid = hash_item(lens)
                box = boxes[bid]
                lid = -1
                for i in range(len(box)):
                    if box[i][0] == lens:
                        lid = i
                        break
                if lid >= 0:
                    del box[lid]
            case [lens, foca]:
                bid = hash_item(lens)
                box = boxes[bid]
                lid = -1
                for i in range(len(box)):
                    if box[i][0] == lens:
                        lid = i
                        break
                if lid >= 0:
                    del box[lid]
                    box.insert(lid, [lens, int(foca)])
                else:
                    box.append([lens, int(foca)])

    res = 0
    for bid in range(256):
        box = boxes[bid]
        for i, [lens, foca] in enumerate(box):
            res += (bid + 1) * (i + 1) * foca

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
