from itertools import islice
from pathlib import Path

import pytest
from aoc.y2023.d21.solution import (
    Garden,
    GardenStep,
    Heading,
    Vec2d,
    parse,
    solve_part1,
    solve_part2,  # noqa: F401
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


def test_vec2d_init():
    assert Vec2d()
    assert Vec2d(0, 0)
    assert Vec2d() == Vec2d(0, 0)
    assert Vec2d(1, 2).y == 1
    assert Vec2d(1, 2).x == 2


@pytest.mark.parametrize(
    "lhs, rhs, exp",
    [
        (Vec2d(1, 1), Vec2d(2, 2), Vec2d(3, 3)),
        (Vec2d(2, 2), Vec2d(1, 1), Vec2d(3, 3)),
        (Vec2d(1, 1), Vec2d(2, 0), Vec2d(3, 1)),
        (Vec2d(1, 1), Vec2d(0, 2), Vec2d(1, 3)),
    ],
)
def test_vec2d_add(lhs, rhs, exp):
    assert lhs + rhs == exp


@pytest.mark.parametrize(
    "lhs, rhs, exp",
    [
        (Vec2d(1, 1), Vec2d(5, 5), Vec2d(1, 1)),
        (Vec2d(6, 1), Vec2d(5, 5), Vec2d(1, 1)),
        (Vec2d(1, 6), Vec2d(5, 5), Vec2d(1, 1)),
        (Vec2d(6, 6), Vec2d(5, 5), Vec2d(1, 1)),
    ],
)
def test_vec2d_mod(lhs, rhs, exp):
    assert lhs % rhs == exp


def test_heading():
    assert len(Heading) == 4
    for n in Heading:
        assert isinstance(n, Vec2d)


def test_gardenstep_init():
    step = GardenStep(1)
    step.add(Vec2d(1, 1))
    assert step.step == 1
    assert len(step) == 1
    assert next(islice(step, 1)) == Vec2d(1, 1)


def test_garden_init_empty():
    assert Garden() is not None


@pytest.mark.example_path("ex01.txt")
def test_garden_start(example_data):
    garden = example_data
    assert garden.start == Vec2d(5, 5)


@pytest.mark.example_path("ex01.txt")
def test_garden_rocks(example_data):
    garden = example_data
    assert Vec2d(0, 0) not in garden.rocks
    assert Vec2d(1, 1) not in garden.rocks
    assert Vec2d(6, 6) not in garden.rocks
    assert Vec2d(2, 6) in garden.rocks
    assert Vec2d(9, 9) in garden.rocks


@pytest.mark.example_path("ex01.txt")
def test_garden_neighbors(example_data):
    garden = example_data
    neighbors = list(garden.neighbors(garden.start))
    assert len(neighbors) == 2
    assert neighbors[0] == Vec2d(4, 5)
    assert neighbors[1] == Vec2d(5, 4)


@pytest.mark.example_path("ex01.txt")
def test_garden_contains_infinite(example_data):
    garden = example_data
    assert garden.size not in garden
    garden.infinite = True
    assert garden.size in garden


@pytest.mark.example_path("ex01.txt")
def test_garden_getitem_infinite(example_data):
    garden = example_data
    garden.infinite = True

    size = garden.size
    base = Vec2d(6, 6)

    jump_e = Vec2d(0, size.x) * 7
    jump_s = Vec2d(size.y, 0) * 7
    assert garden[base] == garden[base + jump_e]
    assert garden[base] == garden[base + jump_s]

    jump_w = -Vec2d(0, size.x) * 9
    jump_n = -Vec2d(size.y, 0) * 9
    assert garden[base] == garden[base + jump_w]
    assert garden[base] == garden[base + jump_n]


@pytest.mark.example_path("ex01.txt")
def test_garden_next_step(example_data):
    garden = example_data

    prev_step = GardenStep()
    prev_step.add(garden.start)
    next_step = garden.next_step(prev_step)

    assert len(next_step) == 2
    assert garden.start not in next_step
    assert Vec2d(4, 5) in next_step
    assert Vec2d(5, 4) in next_step


@pytest.mark.example_path("ex01.txt")
def test_parse_ex01(example_path):
    data = parse(example_path)
    assert data
    assert len(data) == 11 * 11
    assert data.start == Vec2d(5, 5)


@pytest.mark.example_path("ex01.txt")
@pytest.mark.parametrize("steps, plots", [(1, 2), (2, 4), (3, 6), (6, 16)])
def test_solve_part1_ex01_t06(example_data, steps, plots):
    assert solve_part1(example_data, steps) == plots


@pytest.mark.example_path("ex01.txt")
@pytest.mark.parametrize(
    "steps, plots",
    [
        (6, 16),
        (10, 50),
        (50, 1594),
        (100, 6536),
        # (500, 167004),
        # (1000, 668697),
        # (5000, 16733044),
    ],
)
def test_solve_part2_ex01(example_data, steps, plots):
    # NOTE: We're only testing the infinite feature here, not the numerical estimation
    # approach. Therefore, we're using solve_part1, not solve_part2. Performance is
    # acceptable up to 100 steps, but it's yawningly slow above that (for example,
    # 500 steps takes ~5m)

    example_data.infinite = True
    assert solve_part1(example_data, steps) == plots
