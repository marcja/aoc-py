from pathlib import Path

import pytest
from aoc.y2023.d14.solution import parse, solve_part1, solve_part2

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
    data = parse(example_path)
    assert len(data) == 10
    assert len(data[0]) == 10


@pytest.mark.example_path("ex01.txt")
def test_solve_part1_ex01(example_data):
    assert solve_part1(example_data) == 136


@pytest.mark.example_path("ex01.txt")
def test_solve_part2_ex01_times1(example_data):
    assert solve_part2(example_data, 1) == 87


@pytest.mark.example_path("ex01.txt")
def test_solve_part2_ex01_times2(example_data):
    assert solve_part2(example_data, 2) == 69


@pytest.mark.example_path("ex01.txt")
def test_solve_part2_ex01_times3(example_data):
    assert solve_part2(example_data, 3) == 69


@pytest.mark.example_path("ex01.txt")
def test_solve_part2_ex01_times1000000000(example_data):
    assert solve_part2(example_data, 1000000000) == 64
