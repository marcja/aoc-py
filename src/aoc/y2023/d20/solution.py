import logging
import sys
from collections import Counter, defaultdict, deque
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
    BROADCASTER = "broadcaster"
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
                case str(key) if key == ModuleType.BROADCASTER:
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

            if source != ModuleType.BROADCASTER:
                for target in targets:
                    sources[target].add(source[1:])

                    # for those pesky output-only modules
                    if target not in modules:
                        modules[target] = {"type": ModuleType.OUTPUT, "targets": ()}

        return modules, sources


def hash_state(iterable: Iterable):
    return reduce(lambda h, x: (h * 31) ^ hash(x), iterable, 0)


class System:
    def __init__(self, modules, sources):
        self.modules = modules
        self.sources = sources

        self.cache = {}
        self.count = Counter()
        self.queue = deque()
        self.state = {key: False for key in modules}
        self.table = defaultdict(lambda: Pulse.LO)

    def run(self, n):
        self.count.clear()

        for i in range(n):
            cache_key = hash_state(self.state.items())
            if cache_key not in self.cache:
                self._process_button()

                while self.queue:
                    task = self.queue.pop()
                    module = self.modules[task.target]

                    # update count of pulses
                    self.count.update([task.pulse])

                    # process this task
                    match module["type"]:
                        case ModuleType.BROADCASTER:
                            # sends incoming pulse to all target modules
                            self._process_broadcast(task, module)

                        case ModuleType.FLIP_FLOP:
                            self._process_flip_flop(task, module)

                        case ModuleType.CONJUNCTION:
                            self._process_conjunction(task, module)

                self.cache[cache_key] = self.count[Pulse.LO], self.count[Pulse.HI]
            else:
                self.count[Pulse.LO] *= n // len(self.cache)
                self.count[Pulse.HI] *= n // len(self.cache)
                break

        return self.count[Pulse.LO] * self.count[Pulse.HI]

    def _process_button(self):
        self.queue.appendleft(Task("button", ModuleType.BROADCASTER, Pulse.LO))

    def _process_broadcast(self, task, module):
        # send pulses to targets
        for sink in module["targets"]:
            self.queue.appendleft(Task(task.target, sink, task.pulse))

    def _process_flip_flop(self, task, module):
        if task.pulse == Pulse.LO:
            # toggle flip-flop state
            self.state[task.target] = not self.state[task.target]

            # if on, send a high pulse; if off, send a low pulse
            pulse = Pulse.HI if self.state[task.target] else Pulse.LO

            # send pulses to targets
            for sink in module["targets"]:
                self.queue.appendleft(Task(task.target, sink, pulse))

    def _process_conjunction(self, task, module):
        def key(target, source):
            return ":".join((target, source))

        # update memory for this target/source with this pulse
        self.table[key(task.target, task.source)] = task.pulse

        # if high pulses for all inputs, send low pulse; otherwise, send high pulse
        all_hi = all(
            self.table[key(task.target, source)] == Pulse.HI
            for source in self.sources[task.target]
        )
        pulse = Pulse.LO if all_hi else Pulse.HI

        # send pulses to targets
        for sink in module["targets"]:
            self.queue.appendleft(Task(task.target, sink, pulse))


@report
def solve_part1(data, n=1000) -> int:
    modules, sources = data
    system = System(modules, sources)
    return system.run(n)


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
