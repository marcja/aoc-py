from pathlib import Path

import pytest
from aoc.y2023.d01.solution import parse, solve_part1, solve_part2

DATA = Path(__file__).parent / "data"


@pytest.fixture
def ex01_path():
    return DATA / "ex01.txt"


@pytest.fixture
def ex01_data(ex01_path):
    return parse(ex01_path)


@pytest.fixture
def ex02_path():
    return DATA / "ex02.txt"


@pytest.fixture
def ex02_data(ex02_path):
    return parse(ex02_path)


def test_parse_ex01(ex01_path):
    data = parse(ex01_path)
    assert isinstance(data, list)


def test_solve_part1_ex01(ex01_data):
    assert solve_part1(ex01_data) == 142


def test_solve_part2_ex02(ex02_data):
    assert solve_part2(ex02_data) == 281
