import re
import sys
from datetime import timedelta
from functools import partial
from itertools import groupby
from math import prod
from pathlib import Path
from time import perf_counter


def first(value: tuple) -> any:
    return value[0]


def second(value: tuple) -> any:
    return value[1]


def kernel(cols, i):
    return [
        i - cols - 1,
        i - cols,
        i - cols + 1,
        i - 1,
        i,
        i + 1,
        i + cols - 1,
        i + cols,
        i + cols + 1,
    ]


def mask_part(data, cols, i):
    def is_part(s):
        return not (s == "." or s.isdigit() or s.isspace())

    parts = [k for k in kernel(cols, i) if k in range(len(data)) and is_part(data[k])]
    return len(parts)


def parse(path):
    return path.read_text() + "\n"


def solve_part1(data):
    def is_partnum(m):
        return sum([mask[i] for i in range(m.start(), m.end())]) > 0

    cols = data.index("\n") + 1
    mask = list(map(partial(mask_part, data, cols), range(len(data))))

    parts = [int(m.group()) for m in re.finditer(r"\d+", data) if is_partnum(m)]
    return sum(parts)


def solve_part2(data):
    cols = data.index("\n") + 1
    size = len(data)

    # create a lookup table from index into part number
    codes = {}
    for m in re.finditer(r"\d+", data):
        for i in range(m.start(), m.end()):
            codes[i] = (m.start(), int(m.group()))

    # create a mapping from (part_id, part_number) to gear_id
    teeth = {}
    for gear in re.finditer(r"\*", data):
        for i in kernel(cols, gear.start()):
            if i in range(0, size) and data[i].isdigit():
                teeth[codes[i]] = gear.start()

    pairs = [(v, k[1]) for k, v in teeth.items()]
    parts = [(k, list(map(second, g))) for k, g in groupby(pairs, first)]
    gears = [part for part in parts if len(part[1]) == 2]

    ratios = dict(map(lambda v: (v[0], prod(v[1])), gears))
    totals = sum(ratios.values())

    return totals


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
