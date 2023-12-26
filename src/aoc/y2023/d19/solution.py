import logging
import operator
import re
import sys
from abc import ABC
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, ClassVar

from aoc.utils.reporting import report


class Part(dict):
    RE: ClassVar[re.Pattern] = re.compile(
        r"{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}"
    )

    def __init__(self, input):
        m = re.fullmatch(Part.RE, input)
        self.update({k: int(m.group(k)) for k in "xmas"})

    def rating(self):
        return sum(v for k, v in self.items() if k in "xmas")


@dataclass
class Parts(list):
    def __init__(self, input):
        self += [part for part in map(Part, input.splitlines())]


@dataclass
class Action(ABC):
    @staticmethod
    def create(workflow):
        match workflow:
            case "A":
                return AcceptAction()
            case "R":
                return RejectAction()
            case str(name):
                return AssignAction(name)
            case _:
                assert False


@dataclass
class AcceptAction(Action):
    pass


@dataclass
class RejectAction(Action):
    pass


@dataclass
class AssignAction(Action):
    workflow: str


@dataclass
class Condition:
    RE: ClassVar[re.Pattern] = re.compile(r"(?P<key>[xmas])(?P<cmp>[<>])(?P<val>\d+)")

    cmp: Callable[[int, int], bool] = None
    key: str = None
    val: int = None

    def __init__(self, input):
        if input:
            m = re.fullmatch(Condition.RE, input)
            match m.group("cmp"):
                case "<":
                    self.cmp = operator.lt
                case ">":
                    self.cmp = operator.gt
                case _:
                    assert False
            self.key = m.group("key")
            self.val = int(m.group("val"))

    def check(self, part):
        return self.cmp is None or self.cmp(part[self.key], self.val)


@dataclass
class Rule:
    RE: ClassVar[re.Pattern] = re.compile(r"((?P<condition>.+):)?(?P<key>\w+)")

    action: Action
    condition: Condition

    def __init__(self, input):
        m = re.fullmatch(Rule.RE, input)
        self.action = Action.create(m.group("key"))
        self.condition = Condition(m.group("condition"))

    def check(self, part):
        if self.condition and self.condition.check(part):
            return self.action
        else:
            return None


@dataclass
class Workflow:
    RE: ClassVar[re.Pattern] = r"(?P<key>\w+)\{(?P<rules>.*)\}"

    key: str
    rules: list[Rule]

    def __init__(self, input):
        m = re.fullmatch(Workflow.RE, input)
        self.key = m.group("key")
        self.rules = list(Rule(r) for r in m.group("rules").split(","))

    def check(self, part: Part):
        for rule in self.rules:
            if r := rule.check(part):
                return r

        assert False


@dataclass
class System:
    workflows: dict[Workflow]

    def __init__(self, input):
        self.workflows = {w.key: w for w in map(Workflow, input.splitlines())}

    def check(self, part: Part):
        queue = deque()
        queue.appendleft(self.workflows["in"])

        while queue:
            w = queue.pop()
            match w.check(part):
                case AcceptAction():
                    return True
                case RejectAction():
                    return False
                case AssignAction(a):
                    queue.appendleft(self.workflows[a])


def parse(path):
    with open(path) as file:
        s, p = file.read().split("\n\n")

        return System(s), Parts(p)


@report
def solve_part1(data) -> int:
    system, parts = data

    return sum(part.rating() for part in parts if system.check(part))


@report
def solve_part2(data) -> int:
    system, parts = data

    return ...


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
