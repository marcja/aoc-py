import operator
import sys
from datetime import timedelta
from functools import reduce
from math import ceil, floor, prod
from pathlib import Path
from time import perf_counter


def parse(path):
    with open(path) as file:
        time, dist = file.readlines()
        times = map(int, time.split()[1:])
        dists = map(int, dist.split()[1:])
        return tuple(zip(times, dists))


def wins_slow(data):
    def dist(term, hold):
        return hold * (term - hold)

    for time, best in data:
        races = (dist(time, hold) for hold in range(time))
        bests = filter(lambda r: r > best, races)
        yield len(tuple(bests))


def wins_fast(data):
    def diff(x, y):
        return ceil(y - 1) - floor(x)

    def quad(time, best):
        term = (time * time - 4.0 * best) ** 0.5
        root = ((time - term) / 2.0, (time + term) / 2.0)
        return diff(*root)

    for time, best in data:
        yield quad(time, best)


def wins(data):
    return wins_fast(data)


def solve_part1(data):
    return prod(wins(data))


def solve_part2(data):
    time = int(reduce(operator.concat, (str(time) for time, _ in data)))
    best = int(reduce(operator.concat, (str(best) for _, best in data)))

    return prod(wins([(time, best)]))


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
