import sys
from datetime import timedelta
from itertools import batched
from pathlib import Path
from time import perf_counter


def parse(path):
    data = path.read_text()
    head, *body = data.split("\n\n")
    seeds = list(map(int, head.split()[1:]))
    parts = []
    for sect in body:
        part = []
        for line in sect.splitlines()[1:]:
            dst, src, len = map(int, line.split())
            part.append((src, src + len, dst - src))
        part.sort()
        parts.append(part)

    return seeds, parts


def transform(part, packs):
    for x, y in packs:
        for a, b, s in part:
            yield (x, min(y, a))
            yield (max(x, a) + s, min(y, b) + s)
            x = max(x, min(y, b))
        yield (x, y)


def calculate(parts, packs):
    packs = list(packs)
    for part in parts:
        packs = [(x, y) for x, y in transform(part, packs) if x < y]

    return min(x for x, _ in packs)


def solve_part1(data):
    seeds, parts = data
    packs = ((x, x + 1) for x in seeds)

    return calculate(parts, packs)


def solve_part2(data):
    seeds, parts = data
    packs = ((x, x + y) for x, y in batched(seeds, 2))

    return calculate(parts, packs)


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
