import sys
from datetime import timedelta
from pathlib import Path
from time import perf_counter

import numpy as np

TR = str.maketrans(".#", "·⍟")


def print_image(data):
    for line in data:
        disp = "".join(line).translate(TR)
        print(disp)


def parse(path):
    with open(path) as file:
        data = np.array([list(line.strip()) for line in file])

    return data


def solve(data, mult=1):
    mult = max(1, mult - 1)

    dots = data == "."
    rows = np.cumsum(np.all(dots, axis=1).astype(int) * mult)
    cols = np.cumsum(np.all(dots, axis=0).astype(int) * mult)

    rowd = np.arange(len(rows)) + rows
    cold = np.arange(len(cols)) + cols

    bity, bitx = np.where(data == "#")
    outy = np.abs(rowd[bity] - rowd[bity][:, np.newaxis])
    outx = np.abs(cold[bitx] - cold[bitx][:, np.newaxis])

    return np.triu(outy + outx).sum()


def solve_part1(data):
    return solve(data)


def solve_part2(data, mult=1000000):
    return solve(data, mult)


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
