import sys
from datetime import timedelta
from functools import cache
from pathlib import Path
from time import perf_counter


def parse(path):
    data = []
    with open(path) as file:
        for line in file:
            row, dat = line.split()
            rec = tuple(map(int, dat.split(",")))
            data.append((row, rec))

    return data


@cache
def count(row, rec):
    if row == "":
        return 1 if rec == () else 0

    if rec == ():
        return 0 if "#" in row else 1

    res = 0

    if row[0] in ".?":
        res += count(row[1:], rec)

    if row[0] in "#?":
        if (
            rec[0] <= len(row)
            and "." not in row[: rec[0]]
            and (rec[0] == len(row) or row[rec[0]] != "#")
        ):
            res += count(row[rec[0] + 1 :], rec[1:])

    return res


def solve_part1(data):
    sum = 0
    for each in data:
        row, rec = each
        sum += count(row, rec)
    return sum


def solve_part2(data):
    sum = 0
    for each in data:
        row, rec = each

        row = "?".join([row] * 5)
        rec = rec * 5

        sum += count(row, rec)
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
