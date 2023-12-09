from pathlib import Path

import pytest
from aoc.y0000.d00.solution import parse, solve_part1, solve_part2

DATA = Path(__file__).parent / "data"


@pytest.fixture
def ex01_path():
    return DATA / "ex01.txt"


@pytest.fixture
def ex01_text(ex01_path):
    return ex01_path.read_text().rstrip()


@pytest.fixture
def ex01_data(ex01_path):
    return parse(ex01_path)


@pytest.fixture
def ex02_path():
    return DATA / "ex02.txt"


@pytest.fixture
def ex02_text(ex02_path):
    return ex01_path.read_text().rstrip()


@pytest.fixture
def ex02_data(ex02_path):
    return parse(ex02_path)


@pytest.mark.skip(reason="Not implemented")
def test_parse_ex01(ex01_path):
    data = parse(ex01_path)
    assert data == ...


@pytest.mark.skip(reason="Not implemented")
def test_solve_part1_ex01(ex01_data):
    assert solve_part1(ex01_data) == ...


@pytest.mark.skip(reason="Not implemented")
def test_solve_part2_ex01(ex01_data):
    assert solve_part2(ex01_data) == ...
