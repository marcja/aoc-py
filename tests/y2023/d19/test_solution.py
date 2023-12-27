import sys
from pathlib import Path

import pytest
from aoc.y2023.d19.solution import (
    Condition,
    Part,
    Parts,
    PartsBlock,
    Rule,
    Workflow,
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


@pytest.mark.parametrize(
    "input, value",
    [
        ("{x=787,m=2655,a=1222,s=2876}", (787, 2655, 1222, 2876)),
        ("{x=1679,m=44,a=2067,s=496}", (1679, 44, 2067, 496)),
    ],
)
def test_part(input, value):
    p = Part.parse(input)
    assert p["x"] == value[0]
    assert p["m"] == value[1]
    assert p["a"] == value[2]
    assert p["s"] == value[3]


def test_parts():
    input = """{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
    p = Parts.parse(input)
    assert isinstance(p, Parts)
    assert len(p) == 5


def test_block_init_empty():
    b = PartsBlock()
    assert b.lower is None
    assert b.upper is None


def test_block_init_value():
    b = PartsBlock(100, 200)
    assert b.lower == 100
    assert b.upper == 200


def test_block_init_error():
    with pytest.raises(AssertionError):
        _ = PartsBlock(200, 100)


def test_block_eq():
    assert PartsBlock() == PartsBlock()
    assert PartsBlock(100, 200) == PartsBlock(100, 200)
    assert PartsBlock(100, 200) != PartsBlock(200, 300)
    assert PartsBlock(100, 200) != PartsBlock()
    assert PartsBlock() != PartsBlock(100, 200)


def test_block_lt():
    assert PartsBlock() < PartsBlock()
    assert PartsBlock() < PartsBlock(100, 400)
    assert PartsBlock(200, 300) < PartsBlock(100, 400)
    assert PartsBlock(100, 300) < PartsBlock(100, 400)
    assert PartsBlock(200, 400) < PartsBlock(100, 400)
    assert not PartsBlock(300, 600) < PartsBlock(100, 400)
    assert not PartsBlock(400, 600) < PartsBlock(100, 400)
    assert not PartsBlock(500, 600) < PartsBlock(100, 400)


def test_block_and():
    assert PartsBlock() & PartsBlock() == PartsBlock()
    assert PartsBlock() & PartsBlock(100, 400) == PartsBlock(100, 400)
    assert PartsBlock(100, 200) & PartsBlock(100, 400) == PartsBlock(100, 400)
    assert PartsBlock(100, 400) & PartsBlock(100, 400) == PartsBlock(100, 400)
    assert PartsBlock(100, 500) & PartsBlock(100, 400) == PartsBlock(100, 500)
    assert PartsBlock(400, 500) & PartsBlock(100, 400) == PartsBlock(100, 500)


def test_block_or():
    assert PartsBlock() | PartsBlock() == PartsBlock()
    assert PartsBlock() | PartsBlock(100, 400) == PartsBlock()
    assert PartsBlock(100, 200) | PartsBlock(100, 400) == PartsBlock(100, 200)
    assert PartsBlock(100, 400) | PartsBlock(100, 400) == PartsBlock(100, 400)
    assert PartsBlock(100, 500) | PartsBlock(100, 400) == PartsBlock(100, 400)
    assert PartsBlock(400, 500) | PartsBlock(100, 400) == PartsBlock(400, 400)


def test_block_sub():
    assert PartsBlock() - PartsBlock() == PartsBlock()
    assert PartsBlock() - PartsBlock(100, 400) == PartsBlock()
    assert PartsBlock(100, 400) - PartsBlock() == PartsBlock(100, 400)
    assert PartsBlock(100, 400) - PartsBlock(100, 199) == PartsBlock(200, 400)
    assert PartsBlock(100, 400) - PartsBlock(300, 400) == PartsBlock(100, 299)


@pytest.mark.parametrize(
    "input, value",
    [
        ("x<100", ("x", PartsBlock(1, 99))),
        ("m<100", ("m", PartsBlock(1, 99))),
        ("m>100", ("m", PartsBlock(101, sys.maxsize))),
        ("m>200", ("m", PartsBlock(201, sys.maxsize))),
    ],
)
def test_condition(input, value):
    c = Condition.parse(input)
    assert c.key == value[0]
    assert c.block == value[1]


@pytest.fixture
def default_blocks():
    return dict({c: PartsBlock(1, 4000) for c in "xmas"})


def test_condition_combo_empty(default_blocks):
    c = Condition()
    b = c.combo(default_blocks)
    assert b is None


def test_condition_combo_disjoint(default_blocks):
    c = Condition.parse("x>4000")
    lhs, rhs = c.combo(default_blocks)
    assert lhs["x"].isempty()
    assert rhs["x"] == default_blocks["x"]


def test_condition_combo_cover(default_blocks):
    c = Condition.parse("x>0")
    lhs, rhs = c.combo(default_blocks)
    assert lhs["x"] == default_blocks["x"]
    assert rhs["x"].isempty()


def test_condition_combo_split(default_blocks):
    c = Condition.parse("x>1000")
    lhs, rhs = c.combo(default_blocks)
    assert lhs["x"] == PartsBlock(1001, 4000)
    assert rhs["x"] == PartsBlock(1, 1000)


@pytest.mark.parametrize(
    "input, value",
    [
        ("x<100:A", ("x", PartsBlock(1, 99), "A")),
        ("x<100:R", ("x", PartsBlock(1, 99), "R")),
        ("x<100:foo", ("x", PartsBlock(1, 99), "foo")),
        ("x<100:bar", ("x", PartsBlock(1, 99), "bar")),
    ],
)
def test_rule(input, value):
    r = Rule.parse(input)
    assert r.condition.key == value[0]
    assert r.condition.block == value[1]
    assert r.action == value[2]


def test_rule_combo(default_blocks):
    r = Rule.parse("x<100:A")
    key, lhs, rhs = r.combo(default_blocks)
    assert key == "A"
    assert lhs["x"] == PartsBlock(1, 99)
    assert rhs["x"] == PartsBlock(100, 4000)


@pytest.mark.parametrize(
    "input, value",
    [
        ("px{a<2006:qkq,m>2090:A,rfg}", ("px", 3)),
        ("pv{a>1716:R,A}", ("pv", 2)),
        ("jkf{x<1611:A,m>2419:A,a<3305:A,R}", ("jkf", 4)),
    ],
)
def test_workflow(input, value):
    w = Workflow.parse(input)
    assert w.key == value[0]
    assert len(w.rules) == value[1]


def test_workflow_combo(default_blocks):
    w = Workflow.parse("in{s<1351:px,qqz}")
    o = w.combo(default_blocks)
    assert isinstance(o, list)
    assert o[0][0] == "px"
    assert o[1][0] == "qqz"


@pytest.mark.example_path("ex01.txt")
def test_parse_ex01(example_path):
    system, parts = parse(example_path)


@pytest.mark.example_path("ex01.txt")
def test_solve_part1_ex01(example_data):
    assert solve_part1(example_data) == 19114


@pytest.mark.example_path("ex01.txt")
def test_solve_part2_ex01(example_data):
    assert solve_part2(example_data) == 167409079868000
