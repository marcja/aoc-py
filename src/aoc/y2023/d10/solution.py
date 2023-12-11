import sys
from datetime import timedelta
from pathlib import Path
from time import perf_counter

import numpy as np

TR = str.maketrans("SF-7|JL.", "⍟┏━┓┃┛┗·")


def print_tiles(tiles):
    print()
    for line in tiles:
        disp = "".join(line).translate(TR)
        print(disp)


def find_start(tiles):
    return list(zip(*np.where(tiles == "S")))[0]


def find_route(tiles, coord):
    y, x = coord
    t = tiles[coord]

    if t in "SJ-7":
        # try left
        coord = y, x - 1
        if tiles[coord] in "F-L":
            yield coord
    if t in "SF|7":
        # try down
        coord = y + 1, x
        if tiles[coord] in "J|L":
            yield coord
    if t in "SF-L":
        # try right
        coord = y, x + 1
        if tiles[coord] in "J-7":
            yield coord
    if t in "SJ|L":
        # try up
        coord = y - 1, x
        if tiles[coord] in "7|F":
            yield coord


def find_cycle(tiles, start):
    cycle = []
    while start not in cycle:
        cycle.append(start)
        route = [c for c in find_route(tiles, start) if c not in cycle]
        if len(route) > 0:
            start = route[0]
    return cycle


def parse(path):
    with open(path) as file:
        tiles = np.array([list(line.strip()) for line in file], dtype=np.str_)

    start = find_start(tiles)
    cycle = find_cycle(tiles, start)

    for coord, x in np.ndenumerate(tiles):
        if coord not in cycle:
            tiles[coord] = "."

    print_tiles(tiles)

    return tiles, cycle, start


def solve_part1(data):
    _, cycle, _ = data
    return len(cycle) // 2 + len(cycle) % 2


def solve_part2(data):
    _, cycle, _ = data

    x, y = zip(*cycle)
    dets = [x[i] * y[i - 1] - x[i - 1] * y[i] for i in range(len(cycle))]
    area = 0.5 * abs(sum(dets))

    count = int(area - 0.5 * len(cycle) + 1)

    return count


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
