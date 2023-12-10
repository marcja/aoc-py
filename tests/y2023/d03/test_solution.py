from pathlib import Path

import pytest
from aoc.y2023.d03.solution import parse, solve_part1, solve_part2

DATA = Path(__file__).parent / "data"


@pytest.fixture
def ex01_path():
    return DATA / "ex01.txt"


@pytest.fixture
def ex01_data(ex01_path):
    return parse(ex01_path)


def test_parse_ex01(ex01_path):
    data = parse(ex01_path)
    assert isinstance(data, str)


def test_solve_part1_ex01(ex01_data):
    assert solve_part1(ex01_data) == 4361


def test_solve_part2_ex01(ex01_data):
    assert solve_part2(ex01_data) == 467835
