import sys
from collections import Counter
from datetime import timedelta
from functools import total_ordering
from pathlib import Path
from time import perf_counter


@total_ordering
class Hand:
    TR = str.maketrans("23456789TJQKA", "23456789ABCDE")

    def __init__(self, hand, bid, *, wild=""):
        self.hand = hand
        self.bid = int(bid)

        tr = Hand.TR
        if wild != "":
            tr = Hand.TR | str.maketrans(wild, "0" * len(wild))

        self._held = hand.translate(tr)

        counter = Counter(self._held)
        topmost = tuple(c[0] for c in counter.most_common() if c[0] != "0")
        if len(topmost) > 0:
            counter = Counter(self._held.translate(str.maketrans("0", topmost[0])))

        self._rank = [c for r, c in counter.most_common(2)]

    def __hash__(self):
        return hash((self._held, self.bid))

    def __eq__(self, that):
        return (self._held, self.bid) == (that.held, that.bid)

    def __lt__(self, that):
        if self._rank == that._rank:
            return self._held < that._held
        else:
            return self._rank < that._rank

    def __repr__(self):
        return f'Hand("{self.hand}",{self.bid},{self._rank})'


def parse(path):
    with open(path) as file:
        return file.readlines()


def solve(data, *, wild=""):
    hands = []
    for line in data:
        hand = Hand(*line.split(), wild=wild)
        hands.append(hand)
    hands.sort()

    return sum(i * h.bid for i, h in enumerate(hands, 1))


def solve_part1(data):
    return solve(data)


def solve_part2(data):
    return solve(data, wild="J")


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
