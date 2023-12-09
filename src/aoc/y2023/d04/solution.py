import sys
from datetime import timedelta
from pathlib import Path
from time import perf_counter

from tqdm import tqdm


def parse(path):
    with open(path) as file:
        data = []
        for line in file:
            elem = line.split()
            vbar = elem.index("|")
            card = elem[1].rstrip(":")
            have = set(elem[2:vbar])
            want = set(elem[vbar + 1 :])
            data.append((card, len(have & want)))
        return data


def solve_part1(data):
    return sum([1 << wins >> 1 for _, wins in data])


def solve_part2(data):
    score = [1] * len(data)
    for c, (_, wins) in enumerate(data):
        i, j = c + 1, c + 1 + wins
        score[i:j] = [x + score[c] for x in score[i:j]]
    return sum(score)


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
