import operator
from pathlib import Path
from re import X

import pytest
from aoc.y2023.d19.solution import (
    AcceptAction,
    Action,
    AssignAction,
    Condition,
    Part,
    RejectAction,
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
    p = Part(input)
    assert p["x"] == value[0]
    assert p["m"] == value[1]
    assert p["a"] == value[2]
    assert p["s"] == value[3]


@pytest.mark.parametrize(
    "input, value",
    [
        ("x<100", ("x", operator.lt, 100)),
        ("m<100", ("m", operator.lt, 100)),
        ("m>100", ("m", operator.gt, 100)),
        ("m>200", ("m", operator.gt, 200)),
    ],
)
def test_condition(input, value):
    c = Condition(input)
    assert c.key == value[0]
    assert c.cmp == value[1]
    assert c.val == value[2]


@pytest.mark.parametrize(
    "input, value",
    [
        ("A", AcceptAction),
        ("R", RejectAction),
        ("foo", AssignAction),
        ("bar", AssignAction),
    ],
)
def test_action(input, value):
    a = Action.create(input)
    assert isinstance(a, value)


@pytest.mark.parametrize(
    "input, value",
    [
        ("x<100:A", ("x", operator.lt, 100, AcceptAction, None)),
        ("x<100:R", ("x", operator.lt, 100, RejectAction, None)),
        ("x<100:foo", ("x", operator.lt, 100, AssignAction, "foo")),
        ("x<100:bar", ("x", operator.lt, 100, AssignAction, "bar")),
    ],
)
def test_rule(input, value):
    r = Rule(input)
    assert r.condition.key == value[0]
    assert r.condition.cmp == value[1]
    assert r.condition.val == value[2]
    assert isinstance(r.action, value[3])
    if isinstance(r.action, AssignAction):
        assert r.action.workflow == value[4]


@pytest.mark.parametrize(
    "input, value",
    [
        ("px{a<2006:qkq,m>2090:A,rfg}", ("px", 3)),
        ("pv{a>1716:R,A}", ("pv", 2)),
        ("jkf{x<1611:A,m>2419:A,a<3305:A,R}", ("jkf", 4)),
    ],
)
def test_workflow(input, value):
    w = Workflow(input)
    assert w.key == value[0]
    assert len(w.rules) == value[1]


@pytest.mark.example_path("ex01.txt")
def test_parse_ex01(example_path):
    system, parts = parse(example_path)


@pytest.mark.example_path("ex01.txt")
def test_solve_part1_ex01(example_data):
    assert solve_part1(example_data) == 19114


@pytest.mark.xfail
@pytest.mark.example_path("ex01.txt")
def test_solve_part2_ex01(example_data):
    assert solve_part2(example_data) == ...
