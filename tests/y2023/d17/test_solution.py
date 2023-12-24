from pathlib import Path

import pytest
from aoc.y2023.d17.solution import parse, solve_part1, solve_part2

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
    costs = parse(example_path)
    assert len(costs) == 13 * 13
    assert min(costs) == (0, 0)
    assert max(costs) == (12, 12)
    assert all([1 <= s <= 9 for s in costs.values()])


@pytest.mark.example_path("ex01.txt")
def test_solve_part1_ex01(example_data):
    assert solve_part1(example_data) == 102


@pytest.mark.example_path("ex01.txt")
def test_solve_part2_ex01(example_data):
    assert solve_part2(example_data) == 94


@pytest.mark.example_path("ex02.txt")
def test_solve_part2_ex02(example_data):
    assert solve_part2(example_data) == 71
