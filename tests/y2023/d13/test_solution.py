from pathlib import Path

import pytest
from aoc.y2023.d13.solution import parse, solve_part1, solve_part2

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
    pats = parse(example_path)
    assert len(pats) == 2


@pytest.mark.example_path("ex01.txt")
def test_solve_part1_ex01(example_data):
    assert solve_part1(example_data) == 405


@pytest.mark.example_path("ex01.txt")
def test_solve_part2_ex01(example_data):
    assert solve_part2(example_data) == 400


@pytest.mark.example_path("ex02.txt")
def test_solve_part1_ex02(example_data):
    assert solve_part1(example_data) == 709


@pytest.mark.example_path("ex02.txt")
def test_solve_part2_ex02(example_data):
    assert solve_part2(example_data) == 1400


@pytest.mark.example_path("ex03.txt")
def test_solve_part1_ex03(example_data):
    assert solve_part1(example_data) == 100


@pytest.mark.example_path("ex03.txt")
def test_solve_part2_ex03(example_data):
    assert solve_part2(example_data) > 0


@pytest.mark.example_path("ex04.txt")
def test_solve_part2_ex04(example_data):
    assert solve_part2(example_data) > 0
