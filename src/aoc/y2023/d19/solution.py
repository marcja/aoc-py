import logging
import re
import sys
from dataclasses import dataclass
from functools import total_ordering
from math import prod
from pathlib import Path
from typing import ClassVar, Iterable

from aoc.utils.reporting import report


class Part(dict):
    RE: ClassVar[re.Pattern] = re.compile(
        r"{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}"
    )

    @classmethod
    def parse(cls, input: str):
        m = re.fullmatch(Part.RE, input)
        return cls({k: int(m.group(k)) for k in "xmas"})

    def rating(self):
        return sum(v for k, v in self.items() if k in "xmas")


@dataclass
class Parts(list):
    @classmethod
    def parse(cls, input: str):
        return cls([part for part in map(Part.parse, input.splitlines())])

    def __init__(self, iterable: Iterable):
        super().__init__(iterable)


@dataclass(frozen=True)
@total_ordering
class PartsBlock:
    # the *inclusive* lower bound of block
    lower: int = None
    # the *inclusive* upper bound of block
    upper: int = None

    def __post_init__(self):
        if self.lower and self.upper:
            assert self.lower <= self.upper

        if self.lower is None:
            assert self.upper is None

    def __eq__(self, other):
        if not isinstance(other, PartsBlock):
            raise TypeError

        return self.lower == other.lower and self.upper == other.upper

    def __lt__(self, other):
        # subset
        if not isinstance(other, PartsBlock):
            raise TypeError

        if self.isempty():
            return True

        return self.lower >= other.lower and self.upper <= other.upper

    def __and__(self, other):
        # union
        if not isinstance(other, PartsBlock):
            raise TypeError

        if self.isempty():
            return other

        if other.isempty():
            return self

        if self.isdisjoint(other):
            return PartsBlock()

        lower = min(self.lower, other.lower)
        upper = max(self.upper, other.upper)

        return PartsBlock(lower, upper)

    def __or__(self, other):
        # intersection
        if not isinstance(other, PartsBlock):
            raise TypeError

        if self.isempty() or other.isempty():
            return PartsBlock()

        lower = max(self.lower, other.lower)
        upper = min(self.upper, other.upper)

        if lower <= upper:
            return PartsBlock(lower, upper)
        else:
            return PartsBlock()

    def __sub__(self, other):
        # difference
        if not isinstance(other, PartsBlock):
            raise TypeError

        if other.isempty():
            return self

        if self <= other:
            return PartsBlock()

        if other.lower > self.lower:
            return PartsBlock(self.lower, other.lower - 1)
        else:
            return PartsBlock(other.upper + 1, self.upper)

    def __contains__(self, other):
        if not isinstance(other, int):
            raise TypeError

        return self.lower <= other <= self.upper

    def __len__(self):
        return self.upper + 1 - self.lower

    def isdisjoint(self, other):
        return (self | other).isempty()

    def isempty(self):
        return self.lower is None and self.upper is None


@dataclass
class Condition:
    RE: ClassVar[re.Pattern] = re.compile(r"(?P<key>[xmas])(?P<cmp>[<>])(?P<val>\d+)")
    BLOCK: ClassVar[PartsBlock] = PartsBlock(1, sys.maxsize)

    key: str = None
    block: PartsBlock = BLOCK

    @classmethod
    def parse(cls, input: str):
        if not input:
            return Condition()

        m = re.fullmatch(Condition.RE, input)
        key = m.group("key")
        match m.group("cmp"):
            case "<":
                block = PartsBlock(Condition.BLOCK.lower, int(m.group("val")) - 1)
            case ">":
                block = PartsBlock(int(m.group("val")) + 1, Condition.BLOCK.upper)
            case _:
                assert False

        return cls(key, block)

    def check(self, part: Part):
        return self.key is None or part[self.key] in self.block

    def combo(self, blocks: PartsBlock):
        if self.key is None:
            return None
        else:
            lhs = self.block
            rhs = blocks[self.key]

            return (
                {self.key: rhs | lhs},
                {self.key: rhs - lhs},
            )


@dataclass
class Rule:
    RE: ClassVar[re.Pattern] = re.compile(r"((?P<condition>.+):)?(?P<key>\w+)")

    action: str
    condition: Condition

    @classmethod
    def parse(cls, input: str):
        m = re.fullmatch(Rule.RE, input)
        action = m.group("key")
        condition = Condition.parse(m.group("condition"))

        return cls(action, condition)

    def check(self, part: Part):
        return self.action if self.condition.check(part) else None

    def combo(self, blocks: PartsBlock):
        match self.condition.combo(blocks):
            case lhs, rhs:
                return self.action, blocks | lhs, blocks | rhs
            case _:
                return self.action, blocks, PartsBlock()


@dataclass
class Workflow:
    RE: ClassVar[re.Pattern] = r"(?P<key>\w+)\{(?P<rules>.*)\}"

    key: str
    rules: list[Rule]

    @classmethod
    def parse(cls, input: str):
        m = re.fullmatch(Workflow.RE, input)
        key = m.group("key")
        rules = list(Rule.parse(r) for r in m.group("rules").split(","))

        return cls(key, rules)

    def check(self, part: Part):
        for rule in self.rules:
            if r := rule.check(part):
                return r

        assert False

    def combo(self, blocks: PartsBlock):
        result = []

        for rule in self.rules:
            key, lhs, blocks = rule.combo(blocks)
            result.append((key, lhs))

        return result


@dataclass
class System:
    workflows: dict[Workflow]

    @classmethod
    def parse(cls, input: str):
        workflows = {w.key: w for w in map(Workflow.parse, input.splitlines())}

        return cls(workflows)

    def check(self, part: Part):
        stack = []
        stack.append(self.workflows["in"])

        while stack:
            workflow = stack.pop()
            match workflow.check(part):
                case "A":
                    return True
                case "R":
                    return False
                case key:
                    stack.append(self.workflows[key])

    def combo(self, key: str):
        blocks = dict({c: PartsBlock(1, 4000) for c in "xmas"})
        result = 0

        stack = []
        stack.append((key, blocks))

        while stack:
            action, blocks = stack.pop()

            for key, blocks in self.workflows[action].combo(blocks):
                combos = prod(len(block) for block in blocks.values())

                # for visualization at https://sankeymatic.com/build/
                # print(f"{action} [{combos}] {key}")

                match key:
                    case "A":
                        result += combos
                    case "R":
                        continue
                    case _:
                        stack.append((key, blocks))

        return result


def parse(path):
    with open(path) as file:
        system, parts = file.read().split("\n\n")

        return System.parse(system), Parts.parse(parts)


@report
def solve_part1(data) -> int:
    system, parts = data

    return sum(part.rating() for part in parts if system.check(part))


@report
def solve_part2(data) -> int:
    system, _ = data

    return system.combo("in")


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
