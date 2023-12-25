import logging
import sys
from dataclasses import dataclass
from enum import Enum
from itertools import chain, islice, pairwise
from pathlib import Path

from aoc.utils.reporting import report


@dataclass
class Operation:
    dir: str
    len: int
    rgb: str

    def __init__(self, *args):
        assert len(args) == 3
        self.dir = args[0]
        self.len = int(args[1])
        self.rgb = args[2].strip("(#)")

    @classmethod
    def from_rgb(cls, oper):
        oper_len = int(oper.rgb[:5], base=16)
        oper_dir = None
        match oper.rgb[-1]:
            case "0":
                oper_dir = "R"
            case "1":
                oper_dir = "D"
            case "2":
                oper_dir = "L"
            case "3":
                oper_dir = "U"
            case _:
                assert False

        return cls(oper_dir, oper_len, oper.rgb)


@dataclass(order=True, frozen=True)
class Point:
    y: int = 0
    x: int = 0

    def __add__(self, rhs):
        assert isinstance(rhs, Point)
        return Point(self.y + rhs.y, self.x + rhs.x)

    def __mul__(self, rhs):
        assert isinstance(rhs, int)
        return Point(self.y * rhs, self.x * rhs)

    def det(self, rhs):
        assert isinstance(rhs, Point)
        return self.x * rhs.y - self.y * rhs.x


class Direction(Point, Enum):
    U = (-1, 0)
    R = (0, 1)
    D = (1, 0)
    L = (0, -1)


def parse(path: Path) -> dict[tuple[int, int], int]:
    with open(path) as file:
        return [Operation(*line.split()) for line in file]


def limit_graph(graph):
    graph_min_y = min(p.y for p in graph)
    graph_min_x = min(p.x for p in graph)
    graph_max_y = max(p.y for p in graph)
    graph_max_x = max(p.x for p in graph)

    graph_min = Point(graph_min_y, graph_min_x)
    graph_max = Point(graph_max_y, graph_max_x)

    return graph_min, graph_max


def print_graph(graph):
    graph_min, graph_max = limit_graph(graph)

    print(f"\nGRAPH | {graph_min}-{graph_max}\n")

    for y in range(graph_min.y, graph_max.y + 1):
        for x in range(graph_min.x, graph_max.x + 1):
            c = "."
            p = Point(y, x)
            if p in graph:
                c = "#" if p != Point(0, 0) else "S"
            print(c, end="")
        print()


def graph_area(graph, perim):
    # Shoelace algorithm (see https://en.wikipedia.org/wiki/Shoelace_formula)
    area = (
        sum(lhs.det(rhs) for lhs, rhs in pairwise(chain(graph, islice(graph, 1)))) // 2
    )

    # Pick's theorem (see https://en.wikipedia.org/wiki/Pick%27s_theorem)
    interior_points = int(area - perim // 2 + 1)
    exterior_points = perim

    return interior_points + exterior_points


def solve(data) -> int:
    start = Point(0, 0)
    graph = {start: None}
    perim = 0

    for oper in data:
        start += Direction[oper.dir].value * oper.len
        perim += oper.len
        graph[start] = oper.rgb

    return graph_area(graph, perim)


@report
def solve_part1(data) -> int:
    return solve(data)


@report
def solve_part2(data) -> int:
    return solve(map(Operation.from_rgb, data))


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
