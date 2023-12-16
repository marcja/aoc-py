import logging
import sys
from collections import deque
from pathlib import Path

from aoc.utils.reporting import report

N = (-1, 0)  # North
E = (0, 1)  # East
W = (0, -1)  # West
S = (1, 0)  # South


def parse(path: Path) -> tuple[str, ...]:
    """Returns the board as a tuple of strings.

    Args:
        path (Path): the file path for the board data

    Returns:
        tuple[str, ...]: a tuple of strings
    """

    with open(path) as file:
        return tuple(line.strip() for line in file)


def tile(board: tuple[str, ...], coord: tuple[int, int]) -> str | None:
    """Returns the tile (a single character) from the board located at coord.

    Args:
        board (tuple[str, ...]): a board
        coord (tuple[int, int]): a coordinate in (y, x) format

    Returns:
        str | None: the tile if within bounds of the board, otherwise, None.
    """

    # If the coordinate is within the bounds of the board...
    if 0 <= coord[0] < len(board) and 0 <= coord[1] < len(board[0]):
        return board[coord[0]][coord[1]]
    else:
        return None


def next(lhs: tuple[int, int], rhs: tuple[int, int]) -> tuple[int, int]:
    """Adds the rhs coordinate to the lhs coordinate.

    Args:
        lhs (tuple[int, int]): a coordinate in (y, x) format
        rhs (tuple[int, int]): a coordinate in (y, x) format

    Returns:
        tuple[int, int]: the element-wise sum of lhs + rhs
    """

    return (lhs[0] + rhs[0], lhs[1] + rhs[1])


def march(board: tuple[str, ...], curr: tuple[int, int], news: tuple[int, int]) -> int:
    """Returns the count of tiles energized by marching from curr in the direction of news.

    Args:
        board (tuple[str, ...]): a board
        curr (tuple[int, int]): a coordinate in (y, x) format from which to start the march
        news (tuple[int, int]): a coordinate in (y, x) format representing the march direction

    Returns:
        int: the count of tiles.
    """

    TURNS = {
        "-": {N: [E, W], S: [E, W]},
        "|": {E: [N, S], W: [N, S]},
        "/": {N: [E], E: [N], W: [S], S: [W]},
        "\\": {N: [W], E: [S], W: [N], S: [E]},
    }

    tiles = set()  # a set of energized tiles
    moves = set()  # a set of moves (curr, news) already marched
    stack = deque([(curr, news)])  # a stack of moves to march

    while len(stack) > 0:
        curr, news = stack.pop()
        curr = next(curr, news)

        # To reduce runtime and prevent loops, skip this move if we've already marched it.
        if (curr, news) in moves:
            continue

        match t := tile(board, curr):
            case None:
                # curr isn't within bounds of the board, so stop marching in this direction.
                continue
            case ".":
                # We found a ".", so keep marching in this direction.
                stack += [(curr, news)]
            case _:
                # Look up the list of next moves to march from TURNS.
                stack += [(curr, d) for d in TURNS[t].get(news, [news])]

        tiles |= {curr}
        moves |= {(curr, news)}

    return len(tiles)


@report
def solve_part1(board: tuple[str, ...]) -> int:
    return march(board, (0, -1), E)


@report
def solve_part2(board: tuple[str, ...]) -> int:
    res = []

    I = -1  # noqa: E741
    Y = len(board)
    X = len(board[0])

    # Generate a list of marches starting off the board on the east and west sides.
    for y in range(Y):
        res.append(march(board, (y, I), E))
        res.append(march(board, (y, X), W))

    # Generate a list of marches starting off the board on the south and north sides.
    for x in range(X):
        res.append(march(board, (I, x), S))
        res.append(march(board, (Y, x), N))

    return max(res)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
