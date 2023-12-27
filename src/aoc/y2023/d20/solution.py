import logging
import sys
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from enum import StrEnum
from functools import reduce
from itertools import count
from math import lcm
from pathlib import Path
from typing import Iterable

from aoc.utils.reporting import report


class Pulse(StrEnum):
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
            module, target = line.split(" -> ")
            targets = tuple(t.strip(",") for t in target.split())

            # map modules to their successor modules (ie the targets for pulses sent)
            match module:
                case str(key) if key.startswith(ModuleType.BROADCASTER):
                    modules[key] = {
                        "type": ModuleType.BROADCASTER,
                        "targets": targets,
                    }

                case str(key) if key.startswith(ModuleType.FLIP_FLOP):
                    modules[key[1:]] = {
                        "type": ModuleType.FLIP_FLOP,
                        "targets": targets,
                    }

                case str(key) if key.startswith(ModuleType.CONJUNCTION):
                    modules[key[1:]] = {
                        "type": ModuleType.CONJUNCTION,
                        "targets": targets,
                    }

                case _:
                    assert False

            # map modules to their predecessor modules (ie the sources for pulses received)
            if module != ModuleType.BROADCASTER:
                for target in targets:
                    sources[target].add(module[1:])

                    # add any pesky output-only modules to modules
                    if target not in modules:
                        modules[target] = {"type": ModuleType.OUTPUT, "targets": ()}

        return modules, sources


def hashiter(iterable: Iterable):
    return reduce(lambda h, x: (h * 31) ^ hash(x), iterable, 0)


class System:
    def __init__(self, modules, sources):
        self.modules = modules
        self.sources = sources

        self.count = Counter()
        self.queue = deque()
        self.state = {key: False for key in modules}
        self.table = defaultdict(lambda: Pulse.LO)

    def cycle(self, repeat):
        self.count.clear()
        cache = {}

        for i in range(repeat):
            cache_key = hashiter(self.state.items())
            if cache_key in cache:
                self.count[Pulse.LO] *= repeat // len(cache)
                self.count[Pulse.HI] *= repeat // len(cache)
                break

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
                        self._process_conjunction(task, module, [], i)

            cache[cache_key] = self.count[Pulse.LO], self.count[Pulse.HI]

        return self.count[Pulse.LO] * self.count[Pulse.HI]

    def reach(self, target):
        self.count.clear()

        sources = list(self.sources[target])
        targets = self.sources[sources[0]]

        for i in count(1):
            self._process_button()

            while self.queue:
                task = self.queue.pop()
                module = self.modules[task.target]

                # process this task
                match module["type"]:
                    case ModuleType.BROADCASTER:
                        # sends incoming pulse to all target modules
                        self._process_broadcast(task, module)

                    case ModuleType.FLIP_FLOP:
                        self._process_flip_flop(task, module)

                    case ModuleType.CONJUNCTION:
                        self._process_conjunction(task, module, targets, i)

                if self.count.keys() == targets:
                    return lcm(*self.count.values())

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

    def _process_conjunction(self, task, module, targets, i):
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

        if task.target in targets and pulse == Pulse.HI:
            self.count[task.target] = i


@report
def solve_part1(data, repeat=1000) -> int:
    modules, sources = data
    system = System(modules, sources)
    return system.cycle(repeat)


@report
def solve_part2(data, target="rx") -> int:
    modules, sources = data
    system = System(modules, sources)
    return system.reach(target)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
