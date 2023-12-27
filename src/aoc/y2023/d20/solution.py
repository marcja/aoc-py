import logging
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum, StrEnum
from functools import reduce
from pathlib import Path
from typing import Iterable

from aoc.utils.reporting import report


class Pulse(Enum):
    LO = "low"
    HI = "high"


class ModuleType(StrEnum):
    BROADCASTER = "b"
    CONJUNCTION = "&"
    FLIP_FLOP = "%"
    OUTPUT = "#"


@dataclass(frozen=True)
class Task:
    source: str
    target: str
    pulse: Pulse


def parse(path):
    with open(path) as file:
        modules = {}
        sources = defaultdict(set)

        for line in file:
            source, target = line.split(" -> ")
            targets = tuple(t.strip(",") for t in target.split())

            match source:
                case str(key) if key[0] == ModuleType.BROADCASTER:
                    modules[key] = {
                        "type": ModuleType.BROADCASTER,
                        "targets": targets,
                    }

                case str(key) if key[0] == ModuleType.FLIP_FLOP:
                    modules[key[1:]] = {
                        "type": ModuleType.FLIP_FLOP,
                        "targets": targets,
                    }

                case str(key) if key[0] == ModuleType.CONJUNCTION:
                    modules[key[1:]] = {
                        "type": ModuleType.CONJUNCTION,
                        "targets": targets,
                    }

                case _:
                    assert False

            if source != "broadcaster":
                for target in targets:
                    sources[target].add(source[1:])

                    # for those pesky output-only modules
                    if target not in modules:
                        modules[target] = {"type": ModuleType.OUTPUT, "targets": ()}

        return modules, sources


def hash_state(iterable: Iterable):
    return reduce(lambda h, x: (h * 31) ^ hash(x), iterable, 0)


@report
def solve_part1(data, n=1000) -> int:
    modules, sources = data
    states = {key: False for key in modules}
    srcmem = defaultdict(lambda: Pulse.LO)
    cached = {}
    result_lo = 0
    result_hi = 0

    queue = deque()

    # press the broadcaster button 1000 times
    for i in range(n):
        hx = hash_state(states.items())
        # print(f"-- {i} -- {hx}")
        if hx in cached:
            print("cached!")
            lo, hi = cached[hx]
            result_lo *= n // len(cached)
            result_hi *= n // len(cached)
            break

        lo = 0
        hi = 0

        # push button
        queue.appendleft(Task("button", "broadcaster", Pulse.LO))

        while queue:
            task = queue.pop()

            source = task.source
            target = task.target
            pulse = task.pulse

            # print(f"{source} -{pulse.value}-> {target}")

            if pulse == Pulse.LO:
                lo += 1
            else:
                hi += 1

            module = modules[target]

            # process this task
            match module["type"]:
                case ModuleType.BROADCASTER:
                    # sends incoming pulse to all target modules
                    for sink in module["targets"]:
                        queue.appendleft(Task(target, sink, pulse))

                case ModuleType.FLIP_FLOP:
                    if pulse == Pulse.LO:
                        # flip between on and off
                        states[target] = not states[target]
                        # if on, send a high pulse; if off, send a low pulse
                        pulse = Pulse.HI if states[target] else Pulse.LO

                        for sink in module["targets"]:
                            queue.appendleft(Task(target, sink, pulse))

                case ModuleType.CONJUNCTION:
                    srcmem[f"{target}:{source}"] = pulse
                    # if high pulses for all inputs, send low pulse; otherwise, send high pulse
                    all_hi = all(
                        srcmem[f"{target}:{s}"] == Pulse.HI for s in sources[target]
                    )
                    pulse = Pulse.LO if all_hi else Pulse.HI

                    for sink in module["targets"]:
                        queue.appendleft(Task(target, sink, pulse))

        result_lo += lo
        result_hi += hi
        cached[hx] = (result_lo, result_hi)

    return result_lo * result_hi


@report
def solve_part2(modules) -> int:
    return 0


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
