import logging
import operator
import sys
from collections import defaultdict, namedtuple
from heapq import heappop, heappush
from pathlib import Path

from aoc.utils.reporting import report


def parse(path: Path) -> dict[tuple[int, int], int]:
    """Parse the input from path into a dictionary of vertices to weights.

    Args:
        path (Path): the path to the input

    Returns:
        dict[tuple[int, int], int]: a dictionary of grid coordinates to weights
    """
    with open(path) as file:
        return {
            (y, x): int(cost)
            for y, line in enumerate(file)
            for x, cost in enumerate(line.strip())
        }


def dijkstra(states, source, target, minrun, maxrun):
    """Find the shortest path from a source vertex to a destination vertex in a graph.

    Args:
        states: a dictionary of vertices to edges
        source: the source vertex
        target: the destination vertex
        minrun: the minimum steps in the same direction required
        maxrun: the maximum steps in the same direction allowed

    Returns:
        The  shortest path from the source vertex to the destination vertex.
    """

    State = namedtuple("State", ["pos", "dir"])
    Entry = namedtuple("Entry", ["dst", "state"])

    # Initialize a priority queue with the source vertex at zero cost.
    # heap = [(0, State(source, (0, 0)))]
    heap = [Entry(0, State(source, (0, 0)))]

    # Initialize a dictionary of vertices to shortest paths found so far. If no path
    # has yet been found, return an "arbritrarily large number" (such as 1e9).
    best = defaultdict(lambda: int(1e9))
    best[heap[0].state] = heap[0].dst

    while heap:
        # Dequeue the vertex with the lowest distance.
        dst, curr = heappop(heap)

        # If the target vertex has been reached, return the cost of the shortest path.
        if curr.pos == target:
            return dst

        # For each neighbor of the current vertex...
        for next_dir in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            # ...without continuing in the same direction or doubling back in the
            # direction we came from...
            if next_dir in (curr.dir, tuple(map(operator.neg, curr.dir))):
                # NOTE: This was the source of considerable frustration and debugging
                # for me, especially once I rewired for Part 2. It was obvious that I
                # had to prevent going backwards, but I misssed having to prevent going
                # forwards. Since we greedily go forwards below up to maxrun, going any
                # further would violate maxrun.
                continue

            next_dst = dst
            next_pos = curr.pos

            # Go as far as we can in the current direction before changing direction...
            for i in range(1, maxrun + 1):
                next_pos = (
                    curr.pos[0] + i * next_dir[0],
                    curr.pos[1] + i * next_dir[1],
                )

                # Break if next_pos is not within the bounds of the grid...
                if next_pos not in states:
                    break

                next_dst += states[next_pos]
                next = State(next_pos, next_dir)

                # If we can reach this neighbor via a shorter path that has at least as
                # many steps in the current direction as required by minrun, update our
                # vertex leaderboard (best) and add it to the heap to explore further.
                if next_dst < best[next] and i >= minrun:
                    best[next] = next_dst
                    heappush(heap, Entry(next_dst, next))

    # If the target was not reachable, return None.
    return None


@report
def solve_part1(data) -> int:
    states = data
    source = min(states)
    target = max(states)

    return dijkstra(states, source, target, 1, 3)


@report
def solve_part2(data) -> int:
    states = data
    source = min(states)
    target = max(states)

    return dijkstra(states, source, target, 4, 10)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
