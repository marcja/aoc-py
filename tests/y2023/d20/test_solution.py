from pathlib import Path
from pprint import pprint

import pytest
from aoc.y2023.d20.solution import (
    parse,
    solve_part1,
    solve_part2,
)

DATA = Path(__file__).parent / "data"


@pytest.fixture
def example_path(request):
    marker = request.node.get_closest_marker("example_path")
    if marker is None:
        pytest.fail()
    else:
        path = marker.args[0]

    return DATA / path


@pytest.fixture
def example_data(example_path):
    return parse(example_path)


@pytest.mark.example_path("ex01.txt")
def test_parse_ex01(example_path):
    modules, sources = parse(example_path)

    pprint(("modules", modules))
    assert isinstance(modules, dict)
    assert len(modules) == 5

    pprint(("sources", sources))
    assert isinstance(sources, dict)
    assert len(sources) == 4
    assert "broadcaster" not in sources


@pytest.mark.example_path("ex02.txt")
def test_parse_ex02(example_path):
    modules, sources = parse(example_path)

    pprint(("modules", modules))
    assert isinstance(modules, dict)
    assert len(modules) == 6

    pprint(("sources", sources))
    assert isinstance(sources, dict)
    assert len(sources) == 4
    assert "broadcaster" not in sources


@pytest.mark.example_path("ex01.txt")
def test_solve_part1_ex01(example_data):
    assert solve_part1(example_data) == 32000000


@pytest.mark.example_path("ex02.txt")
def test_solve_part1_ex02(example_data):
    assert solve_part1(example_data) == 11687500


@pytest.mark.example_path("ex03.txt")
def test_solve_part2_ex01(example_data):
    assert solve_part2(example_data) == 2
