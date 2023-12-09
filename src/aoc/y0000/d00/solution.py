import sys
from datetime import timedelta
from pathlib import Path
from time import perf_counter

from tqdm import tqdm


def parse(path):
    return ...


def solve_part1(data):
    for each in tqdm(data):
        pass
    return ...


def solve_part2(data):
    for each in tqdm(data):
        pass
    return ...


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
