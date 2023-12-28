import logging
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from pprint import pprint
from typing import Iterable, Optional, override

import numpy as np
from aoc.utils.reporting import report
from numpy.polynomial import polynomial as npp
from tqdm import trange


@dataclass(frozen=True, order=True)
class Vec2d:
    """Represents a 2D vector (or coordinate) in row-major (y, x) format."""

    y: int = 0
    x: int = 0

    def __add__(self, other: "Vec2d") -> "Vec2d":
        return Vec2d(self.y + other.y, self.x + other.x)

    def __mod__(self, other: "Vec2d") -> "Vec2d":
        return Vec2d(self.y % other.y, self.x % other.x)

    def __mul__(self, scalar: int) -> "Vec2d":
        return Vec2d(self.y * scalar, self.x * scalar)

    def __neg__(self) -> "Vec2d":
        return Vec2d(-self.y, -self.x)


class Heading(Vec2d, Enum):
    N = (-1, 0)
    E = (0, 1)
    W = (0, -1)
    S = (1, 0)


@dataclass
class GardenStep(set[Vec2d]):
    """Represents the plots reachable at step N as a set."""

    step: int = 0


@dataclass
class Garden(dict[Vec2d, str]):
    """Represents the garden as a grid with all of its plots, rocks, and relationships."""

    def __init__(
        self, input: Optional[Iterable[tuple[Vec2d, str]]] = None, /, infinite=False
    ):
        """Return a new Garden, possibly initialized with input and a flag to indiciate if infinite."""

        super().__init__()

        """The starting position of the elf in the garden."""
        self.start: Optional[Vec2d] = None

        """The set of all rocks in the garden."""
        self.rocks: set[Vec2d] = set()

        """The flag to indicate if garden coordinate are toroidal (aka "infinite")."""
        self.infinite = infinite

        if not input:
            return

        for k, v in input:
            self[k] = v
            match v:
                case "S":
                    self.start = k
                case "#":
                    self.rocks.add(k)

        """The size of the garden."""
        self.size = max(self.keys()) + Vec2d(1, 1)

    @override
    def __contains__(self, __key: object) -> bool:
        if not isinstance(__key, Vec2d):
            raise TypeError

        if self.infinite:
            __key %= self.size

        return super().__contains__(__key)

    @override
    def __getitem__(self, __key: Vec2d) -> str:
        if self.infinite:
            __key %= self.size

        return super().__getitem__(__key)

    @override
    def __repr__(self) -> str:
        return super().__repr__()

    def is_plot(self, tile: Vec2d):
        if self.infinite:
            tile %= self.size

        return tile in self and tile not in self.rocks

    def neighbors(self, tile: Vec2d):
        return (tile + h for h in Heading if self.is_plot(tile + h))

    def next_step(self, step: GardenStep) -> GardenStep:
        next = GardenStep(step.step + 1)
        next.update([n for p in step for n in self.neighbors(p)])
        return next


def parse(path: Path):
    with open(path) as file:
        return Garden(
            (Vec2d(y, x), c)
            for y, r in enumerate(file)
            for x, c in enumerate(r.strip())
        )


@report
def solve_part1(garden, steps: int = 64) -> int:
    step = GardenStep()
    step.add(garden.start)

    for i in trange(steps):
        step = garden.next_step(step)

    return len(step)


@report
def solve_part2(garden, steps: int = 26501365) -> int:
    # My approach for Part 2 differs from Part 1 in two notable ways:
    #   1. we treat the garden as toroidal ("infinite")
    #   2. we numerically extrapolate the plots at step n rather than simulate it
    #
    # To extrapolate the plots at step n, we calculate the polynomial using samples we
    # observe through a similar simlulation we used for Part 1. But there are lots
    # of finicky details:
    #
    #   - Not just any polynomial, but a second-degree polynomial -- aka a quadratic.
    #   - Why quadratic? Well, when the samples are plotted with Google Sheets and then
    #     annotated with a trendline, the second-degree polynomial fits perfectly.
    #   - Also, when I got stuck, r/adventofcode confirmed it was quadratic.
    #   - Also, I'm sure there is a more substantive reason it's quadratic based on the
    #     geometry of the problem, but meh. Applied wins over pure for me in this case.
    #   - To calculate the quadratic polynomial, we need three points. (Because math.)
    #   - A subtlety, though, is that the polynomial won't come out right if you choose
    #     _any_ three points. The strategy (which I shamelessly lifted from the experts
    #     on r/adventofcode) is to choose the center points (aka "start" position) of
    #     each repeated grid.
    #   - Since the puzzle input has a clear, unobstructed path to the east and west
    #     of the start point, the idea is that we can know exactly how many steps
    #     it takes to get to the next center point without hitting any rocks. Note that
    #     this is a unique oddity of the puzzle input that isn't found in the examples.
    #   - Further, since each repeated grid is the same as all others (hence,
    #     "repeated"), steps from the center point of any grid should observe the same
    #     behavior as the original grid.
    #   - In fact, if we sample at any other points, we'll get a different (and wrong)
    #     polynomial that won't give us the right answer. (Because rocks.)
    #   - Given a grid of size (131, 131), the midpoint is (65, 65).
    #   - Given a repeated grid of size (131, 131), the midpoints of grid (m, n) are
    #     periodic and given by (131m + 65, 131n + 65).
    #   - So, we'll sample our simulation at steps (65, 196, 327), all of which are
    #     small enough to be simulated in reasonable time using our Part 1 approach
    #     (now modded for toroidal coordinates).
    #   - Then we'll plug those samples into quadratic polynomial fit function -- I
    #     used NumPy, for simplicity) and evaluate the polynomial for our answer.
    #   - The final gotcha (that had me stuck for _hours_) is that the polynomial fit
    #     is unstable and highly sensitive to your choice of x-coordinates and which
    #     NumPy polynomial routine you use. I only got the correct rounded answer
    #     when using _periods_, not steps, with the np.polynomial.polyfit function.
    #       - BAD:  [(26501365, y) | (65, y1), (196, y2), (327, y3)]
    #       - GOOD: [(  202300, y) | ( 0, y1), (  1, y2), (  2, y3)]
    #     np.polynomial.polynomial.Polynomial.fit returned an off-by-one answer.
    #   - "But wait," you ask, "where did that 202300 come from?" Haha. Well, 202300
    #     is the number of periods for 26501365 -- (26501365 − 65) / 131 == 202300.
    #   - And, of course, this means that this approach (which works for the puzzle
    #     input) won't work for the example input.
    #
    # And there you go. Thank you to the many folks on r/adventofcode who dropped
    # enough useful clues for me to figure this one out. I wouldn't have solved Part 2
    # on my own without them.

    def scale_div(x: int) -> int:
        return (x - garden.size.x // 2) // garden.size.x

    def scale_mod(x: int) -> int:
        return (x - garden.size.x // 2) % garden.size.x

    step = GardenStep()
    step.add(garden.start)

    garden.infinite = True
    samples = {}

    for i in trange(steps + 1):
        if scale_mod(i) == 0:
            samples[i] = len(step)

            # stop after taking three samples, which is all we need for fitting
            if len(samples) == 3:
                break

        step = garden.next_step(step)

    pprint(f"SAMPLES: {samples.items()}")

    y = np.array(list(samples.values()))
    x = np.arange(y.size)
    n = scale_div(steps)

    c = npp.polyfit(x, y, 2)
    r = npp.polyval(n, c)

    return round(r)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
