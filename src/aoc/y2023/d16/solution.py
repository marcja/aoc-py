import sys
from collections import deque
from pathlib import Path

from aoc.utils.timing import timed


def parse(path):
    with open(path) as file:
        return tuple(line.strip() for line in file)


def at(board, coord):
    if 0 <= coord[0] < len(board) and 0 <= coord[1] < len(board[0]):
        return board[coord[0]][coord[1]]
    else:
        return None


def go(lhs: tuple[int, int], rhs: tuple[int, int]) -> tuple[int, int]:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])


N = (-1, 0)
E = (0, 1)
W = (0, -1)
S = (1, 0)


def march(board, curr, news):
    tiles = set()
    moves = set()

    queue = deque()
    queue.append((curr, news))

    while len(queue) > 0:
        curr, news = queue.pop()
        curr = go(curr, news)

        if (curr, news) in moves:
            continue

        match at(board, curr):
            case "-":
                if news in [N, S]:
                    queue.append((curr, E))
                    queue.append((curr, W))
                else:
                    queue.append((curr, news))
            case "|":
                if news in [E, W]:
                    queue.append((curr, N))
                    queue.append((curr, S))
                else:
                    queue.append((curr, news))
            case "/":
                match news:
                    case (-1, 0):
                        queue.append((curr, E))
                    case (0, 1):
                        queue.append((curr, N))
                    case (0, -1):
                        queue.append((curr, S))
                    case (1, 0):
                        queue.append((curr, W))
            case "\\":
                match news:
                    case (-1, 0):
                        queue.append((curr, W))
                    case (0, 1):
                        queue.append((curr, S))
                    case (0, -1):
                        queue.append((curr, N))
                    case (1, 0):
                        queue.append((curr, E))
            case None:
                continue
            case _:
                queue.append((curr, news))

        tiles |= {curr}
        moves |= {(curr, news)}

    return len(tiles)


@timed
def solve_part1(board):
    return march(board, (0, -1), E)


@timed
def solve_part2(board):
    res = []
    for y in range(len(board)):
        res.append(march(board, (y, -1), E))
        res.append(march(board, (y, len(board)), W))
    for x in range(len(board[0])):
        res.append(march(board, (-1, x), S))
        res.append(march(board, (len(board), x), N))

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
