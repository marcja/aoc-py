import logging
import sys
from pathlib import Path

import numpy as np
from aoc.utils.timing import timed


def parse(path):
    COLORS = {"red": 0, "green": 1, "blue": 2}
    MAXPLY = 10

    with open(path) as file:
        games = file.read().splitlines()
        cubes = np.zeros((len(games), len(COLORS), MAXPLY), int)
        for g, game in enumerate(games):
            _, plays = game.split(":")
            for p, play in enumerate(plays.split(";")):
                for pair in play.split(","):
                    count, color = pair.split()
                    cubes[g, COLORS[color], p] = count

        return cubes


@timed
def solve_part1(cubes):
    limit = np.array([12, 13, 14])
    valid = np.all(cubes.max(2) <= limit, 1)

    return np.sum(np.argwhere(valid) + 1)


@timed
def solve_part2(cubes):
    return cubes.max(2).prod(1).sum()


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
