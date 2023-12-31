import sys
from datetime import timedelta
from itertools import count
from pathlib import Path
from time import perf_counter

import numpy as np


def parse(path):
    TR = {"O": -1, ".": 0, "#": 1}

    with open(path) as file:
        return np.array([[TR[cell] for cell in line.strip()] for line in file])


def tilt(data):
    data = np.rot90(data)
    data = np.row_stack(
        [
            np.concatenate([np.sort(s) for s in np.hsplit(r, np.where(r == 1)[0] + 1)])
            for r in data
        ]
    )
    data = np.rot90(data, -1)
    return data


def spin(data):
    for _ in range(4):
        data = tilt(data)
        data = np.rot90(data, -1)

    return data


def loop(data):
    hist = {}
    recs = []

    for i in count(1):
        data = spin(data)
        key = hash(tuple(data.flat))
        if key in hist:
            return (hist[key], i, recs)
        else:
            hist[key] = i
            recs.append(load(data))


def load(data):
    rocks = np.count_nonzero(data == -1, 1)
    score = np.arange(rocks.shape[0], 0, -1)

    return np.sum(rocks * score)


def solve_part1(data):
    return load(tilt(data))


def solve_part2(data, times=1000000000):
    beg, end, recs = loop(data)
    stop = beg + (times - beg) % (end - beg)
    stop = min(times, stop) - 1

    return recs[stop]


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
