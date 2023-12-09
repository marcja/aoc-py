import re
import sys
from datetime import timedelta
from pathlib import Path
from time import perf_counter


def parse(path):
    with open(path) as f:
        return f.readlines()


def solve_part1(data):
    sum = 0
    for line in data:
        line = re.sub(r"\D", "", line)
        pair = line[0] + line[-1]
        sum += int(pair)
    return sum


def solve_part2(data):
    NUMBERS = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def expn(match):
        number = match.group(1)
        return f"{number[0]}{NUMBERS[number]}{number[-1]}"

    sum = 0
    for line in data:
        line = re.sub(r"(?=(one|two|three|four|five|six|seven|eight|nine))", expn, line)
        line = re.sub(r"\D", "", line)
        pair = line[0] + line[-1]
        sum += int(pair)
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
