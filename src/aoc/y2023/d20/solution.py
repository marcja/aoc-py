import logging
import sys
from abc import ABC
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from enum import StrEnum
from functools import reduce
from itertools import count
from math import lcm
from pathlib import Path
from typing import Hashable, Iterable, override

from aoc.utils.reporting import report


class Pulse(StrEnum):
    LO = "low"
    HI = "high"


class ModuleType(StrEnum):
    BROADCASTER = "broadcaster"
    BUTTON = "button"
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
                case str(id) if id.startswith(ModuleType.BROADCASTER):
                    modules[id] = {
                        "id": id,
                        "type": ModuleType.BROADCASTER,
                        "targets": targets,
                    }

                case str(id) if id.startswith(ModuleType.FLIP_FLOP):
                    modules[id[1:]] = {
                        "id": id[1:],
                        "type": ModuleType.FLIP_FLOP,
                        "targets": targets,
                    }

                case str(id) if id.startswith(ModuleType.CONJUNCTION):
                    modules[id[1:]] = {
                        "id": id[1:],
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
                        modules[target] = {
                            "id": target,
                            "type": ModuleType.OUTPUT,
                            "targets": (),
                        }

        return modules, sources


def hashiter(iterable: Iterable[Hashable]) -> int:
    """Return a (naive) hash of an iterable of hashable elements.

    Args:
        iterable (Iterable): an iterable of hashable elements

    Returns:
        int: a hash
    """
    return reduce(lambda h, x: (h * 31) ^ hash(x), iterable, 0)


class Module(ABC):
    def __init__(self, module, system: "System") -> None:
        self.module = module
        self.system = system
        self.pulse = Pulse.LO

    @staticmethod
    def create(module: dict, system: "System") -> "Module":
        """Create a concrete subclass of Module based on `module`

        Args:
            module (dict): the module data
            system (System): the system managing this module

        Returns:
            _type_: _description_
        """
        assert module
        assert system

        match module["type"]:
            case ModuleType.BROADCASTER:
                return BroadcasterModule(module, system)
            case ModuleType.FLIP_FLOP:
                return FlipFlopModule(module, system)
            case ModuleType.CONJUNCTION:
                return ConjunctionModule(module, system)
            case ModuleType.OUTPUT:
                return OutputModule(module, system)
            case _:
                assert False

    def process(self, task):
        return ()


class BroadcasterModule(Module):
    @override
    def process(self, task):
        # send pulses to targets
        return (Task(task.target, t, task.pulse) for t in self.module["targets"])


class FlipFlopModule(Module):
    @override
    def process(self, task):
        if task.pulse == Pulse.HI:
            return ()

        # toggle flip-flop state
        state = self.system.toggle(task.target)

        # if on, send a high pulse; if off, send a low pulse
        self.pulse = Pulse.HI if state else Pulse.LO

        # send pulses to targets
        return (Task(task.target, t, self.pulse) for t in self.module["targets"])


class ConjunctionModule(Module):
    def __init__(self, module, system):
        super().__init__(module, system)

        # the memory of most recent pulses sent to this conjunction from each source
        self.input = defaultdict(lambda: Pulse.LO)

    @override
    def process(self, task):
        # update memory for this target/source with this pulse
        self.input[task.source] = task.pulse

        # if high pulses for all inputs, send low pulse; otherwise, send high pulse
        input = (self.input[source] for source in self.system.sources[task.target])
        self.pulse = Pulse.LO if all(i == Pulse.HI for i in input) else Pulse.HI

        # send pulses to targets
        return (Task(task.target, t, self.pulse) for t in self.module["targets"])


class OutputModule(Module):
    pass


class System:
    def __init__(self, modules, sources):
        self.modules = {m["id"]: Module.create(m, self) for m in modules.values()}
        self.sources = sources

        self.count = Counter()
        self.queue = deque()
        self.state = {id: False for id in modules}

    def _clear(self):
        self.count.clear()
        self.queue.clear()

    def _queue_button(self):
        self.queue.appendleft(Task(ModuleType.BUTTON, ModuleType.BROADCASTER, Pulse.LO))

    def _solve(self, loop: Iterable, targets: list) -> int:
        """Return the cycle or reach (see `cycle` and `reach`)

        Args:
            loop (Iterable): an iterable (such as range or count) to loop over
            targets (list): the target nodes (see `reach`)

        Returns:
            int: the reach, if `targets` is non-empty; otherwise, the cycle
        """

        self._clear()

        for i in loop:
            self._queue_button()

            while self.queue:
                task = self.queue.pop()

                module = self.modules[task.target]
                for t in module.process(task):
                    self.queue.appendleft(t)

                # update count of pulses
                self.count.update([task.pulse])

                if module.pulse == Pulse.HI and task.target in targets:
                    self.count[task.target] = i

                    # we're using the counter for both pulses and target periods, so be
                    # sure to filter the counter for just the targets here
                    counts = {k: v for k, v in self.count.items() if k in targets}

                    if counts.keys() == targets:
                        # HACK: All counts from the examples and puzzle input seem to
                        # be prime. Therefore, prod(_c_) should equal lcm(_c_). But
                        # using lcm here was helpful to catch an off-by-one bug.
                        return lcm(*counts.values())

        return self.count[Pulse.LO] * self.count[Pulse.HI]

    def toggle(self, id: str) -> bool:
        """Toggle the state of module `id` between ON and OFF

        Args:
            id (str): the id of the module to toggle
        """

        self.state[id] = not self.state[id]

        return self.state[id]

    def cycle(self, repeat: int) -> int:
        """Return the prodsum of pulses after pressing the button module `repeat` times

        Args:
            repeat (int): the number of times to press the button

        Returns:
            int: the count of low pulses times the count of high pulses
        """

        return self._solve(range(1, repeat + 1), [])

    def reach(self, targets: list[str]) -> int:
        """Return the count of button presses required to deliver a low pulse to 'rx'

        HACK: The list of target nodes to track (`targets`) is a bit of a hack. The
        predecessor of the `rx` module (at least in my puzzle input) is the conjunction
        module `zr`. `zr` has four predecessor nodes. The target nodes of this method
        are those four predecessor nodes of `zr`.

        Args:
            targets (list[str]): the list of target nodes to track

        Returns:
            int: the count of button presses required to deliver a low pulse to `rx`
        """

        return self._solve(count(1), targets)


@report
def solve_part1(data) -> int:
    modules, sources = data
    system = System(modules, sources)
    return system.cycle(1000)


@report
def solve_part2(data) -> int:
    modules, sources = data
    system = System(modules, sources)

    # HACK: In my puzzle input, the single source of module "rx" is a conjunction
    # module with id "zr". Our approach is to find out how many button presses are
    # required to get "zr" to send a low pulse to "rx". This only happens when all of
    # the sources of "zr" have most recently sent it a high pulse. If we can find the
    # period of each of "zr"'s sources sending a high pulse, the period of "zr"
    # sending a low pulse should be the LCM of all the sources' periods.
    return system.reach(sources["zr"])


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    path = Path(sys.argv[1])
    data = parse(path)

    solve_part1(data)
    solve_part2(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
