from pathlib import Path

import pytest
from aoc.y2023.d08.solution import parse, solve_part1, solve_part2

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


@pytest.fixture
def ex03_path():
    return DATA / "ex03.txt"


@pytest.fixture
def ex03_data(ex03_path):
    return parse(ex03_path)


def test_parse_ex01(ex01_path):
    data = parse(ex01_path)
    assert isinstance(data, tuple)


def test_solve_part1_ex01(ex01_data):
    assert solve_part1(ex01_data) == 2


def test_solve_part1_ex02(ex02_data):
    assert solve_part1(ex02_data) == 6


def test_solve_part2_ex03(ex03_data):
    assert solve_part2(ex03_data) == 6
