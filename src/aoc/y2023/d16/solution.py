import sys
from collections import deque
from pathlib import Path

from aoc.utils.timing import timed

N = (-1, 0)
E = (0, 1)
W = (0, -1)
S = (1, 0)


def parse(path: Path) -> tuple[str, ...]:
    with open(path) as file:
        return tuple(line.strip() for line in file)


def tile(board: tuple[str, ...], coord: tuple[int, int]) -> str | None:
    if 0 <= coord[0] < len(board) and 0 <= coord[1] < len(board[0]):
        return board[coord[0]][coord[1]]
    else:
        return None


def next(lhs: tuple[int, int], rhs: tuple[int, int]) -> tuple[int, int]:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])


def march(board: tuple[str, ...], curr: tuple[int, int], news: tuple[int, int]) -> int:
    tiles = set()
    moves = set()
    queue = deque()

    queue.append((curr, news))

    while len(queue) > 0:
        curr, news = queue.pop()
        curr = next(curr, news)

        if (curr, news) in moves:
            continue

        match tile(board, curr):
            case "-":
                turns = {N: [E, W], S: [E, W], E: [news], W: [news]}
                queue += [(curr, d) for d in turns[news]]
            case "|":
                turns = {E: [N, S], W: [N, S], N: [news], S: [news]}
                queue += [(curr, d) for d in turns[news]]
            case "/":
                turn = {N: E, E: N, W: S, S: W}
                queue += [(curr, turn[news])]
            case "\\":
                turn = {N: W, E: S, W: N, S: E}
                queue += [(curr, turn[news])]
            case None:
                continue
            case _:
                queue += [(curr, news)]

        tiles |= {curr}
        moves |= {(curr, news)}

    return len(tiles)


@timed
def solve_part1(board: tuple[str, ...]) -> int:
    return march(board, (0, -1), E)


@timed
def solve_part2(board: tuple[str, ...]) -> int:
    res = []

    I = -1  # noqa: E741
    Y = len(board)
    X = len(board[0])

    for y in range(Y):
        res.append(march(board, (y, I), E))
        res.append(march(board, (y, X), W))

    for x in range(X):
        res.append(march(board, (I, x), S))
        res.append(march(board, (Y, x), N))

    return max(res)


def main():
    path = Path(sys.argv[1])
    data = parse(path)

    part1 = solve_part1(data)
    print(f"> solve_part1 | {part1:>20} |")

    part2 = solve_part2(data)
    print(f"> solve_part2 | {part2:>20} |")

    return 0


if __name__ == "__main__":
    sys.exit(main())
