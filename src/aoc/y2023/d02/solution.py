import operator
import re
import sys
from datetime import timedelta
from functools import reduce
from pathlib import Path
from time import perf_counter


def parse(path):
    with open(path) as f:
        games = {}
        for line in f:
            head, tail = line.split(":")
            game = re.search(r"Game (\d+)", head).group(1)
            games[game] = {}

            for set, sets in enumerate(tail.split(";")):
                counts = {}
                for pairs in re.finditer(r"(\d+) (\w+)", sets):
                    count, color = pairs.groups()
                    counts[color] = counts.get(color, 0) + int(count)
                games[game][set] = counts
        return games


def solve_part1(data):
    sum = 0
    for game, sets in data.items():
        violations = 0
        for counts in sets.values():
            match counts:
                case {"red": int() as count} if count > 12:
                    violations += 1
                case {"green": int() as count} if count > 13:
                    violations += 1
                case {"blue": int() as count} if count > 14:
                    violations += 1
        if violations == 0:
            sum += int(game)
    return sum


def solve_part2(data):
    def minimum_set(lhs, rhs):
        result = {}
        for color in ["red", "green", "blue"]:
            result[color] = max(lhs.get(color, 0), rhs.get(color, 0))
        return result

    sum = 0
    for game, sets in data.items():
        result = reduce(minimum_set, sets.values())
        power = reduce(operator.mul, result.values())
        sum += power
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
