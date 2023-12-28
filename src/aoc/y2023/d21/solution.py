import logging
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Optional, Tuple

from aoc.utils.reporting import report
from tqdm import trange


@dataclass(frozen=True, order=True)
class Vec2d:
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
    step: int = 0


@dataclass
class Garden(dict[Vec2d, str]):
    def __init__(
        self, input: Optional[Iterable[Tuple[Vec2d, str]]] = None, /, infinite=False
    ):
        super().__init__()

        self.start: Optional[Vec2d] = None
        self.rocks: set[Vec2d] = set()
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

        self.size = max(self.keys()) + Vec2d(1, 1)

    def __contains__(self, __key: object) -> bool:
        if not isinstance(__key, Vec2d):
            raise TypeError

        if self.infinite:
            __key %= self.size

        return super().__contains__(__key)

    def __getitem__(self, __key: Vec2d) -> str:
        if self.infinite:
            __key %= self.size

        return super().__getitem__(__key)

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
    garden.infinite = True

    step = GardenStep()
    step.add(garden.start)

    for i in range(steps):
        step = garden.next_step(step)

    return len(step)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
