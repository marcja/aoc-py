import sys
from datetime import timedelta
from pathlib import Path
from time import perf_counter

import numpy as np

TR = str.maketrans(".#", "01")


def parse(path):
    def parse_rec(rec):
        return np.array([tuple(map(int, tuple(row))) for row in rec.split()])

    with open(path) as file:
        text = file.read()
        recs = str.translate(text, TR).split("\n\n")
        pats = [parse_rec(rec) for rec in recs]

    return pats


def find_reflection_h(pattern, exclude=0):
    for i in range(1, pattern.shape[1]):
        if i == exclude:
            continue

        lhs, rhs = np.hsplit(pattern, [i])
        siz = min(lhs.shape[1], rhs.shape[1])
        if (np.fliplr(lhs)[:, :siz] == rhs[:, :siz]).all():
            return i


def find_reflection(pattern, exclude=0):
    r = find_reflection_h(pattern, exclude)
    if r:
        return r

    r = find_reflection_h(np.rot90(pattern), exclude / 100)
    if r:
        return r * 100

    return 0


def solve_part1(data):
    return sum([find_reflection(pattern) for pattern in data])


def solve_part2(data):
    sum = 0
    for id, pattern in enumerate(data):
        mask = np.zeros_like(pattern)
        base = find_reflection(pattern)
        mask[0, 0] = 1
        for i in range(len(pattern.flat)):
            r = find_reflection(pattern ^ np.roll(mask, i), base)
            if r > 0:
                sum += r
                break

    return sum


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
