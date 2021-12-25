import math
import pytest
from pycalc.calculator import __split_formula, solve


def test_split():
    assert __split_formula("1 + 1") == ["1", "+1"]
    assert __split_formula("1 - 1") == ["1", "-1"]
    assert __split_formula("1 - (3 + 2)") == ["1", "-", "(", "3", "+2", ")"]
    assert __split_formula("(1 - 1)") == ["(", "1", "-1", ")"]
    assert __split_formula("1 + 3 - 1 // 22 - 1") == ["1", "+3", "-1", "/", "/", "22", "-1"]

    # scientific notation
    assert __split_formula("1e-3") == ["1e-3"]
    assert __split_formula("1 + 1e-3") == ["1", "+1e-3"]


def test_constants():
    assert solve("e") == math.e
    assert solve("pi") == math.pi


def test_solve_operators():
    assert solve("1") == 1
    assert solve("-3") == -3
    assert solve("1e-3 + 1e-2") == 0.011
    assert solve("1 + 2") == 1 + 2
    assert solve("1 - 1") == 1 - 1
    assert solve("3 - 10") == 3 - 10
    assert solve("3 / 3") == 1
    assert solve("4 // 3") == 1
    assert solve("4 * 7") == 4 * 7
    assert solve("7 % 4") == 3
    assert solve("2 ^ 8") == 2 ** 8
    assert solve("1 + 1 / 3") == 1 + (1 / 3)
    assert solve("1 + (1 / 3)") == 1 + (1 / 3)
    assert solve("(1 + 1) / 3") == (1+1) / 3


def test_solve_unary_fn():
    assert solve("floor(3.2238)") == 3.0
    assert solve("ceil(3.2238)") == 4.0
    assert solve("sqrt(23 ^ 2)") == 23

    assert solve("ln(e)") == pytest.approx(1)
    assert solve("ln(e ^ 42)") == pytest.approx(42)


def test_solve_unary_fn_trigonometric():
    assert solve("sin(0)") == 0
    assert solve("cos(0)") == 1
    assert solve("tan(0)") == 0

    assert solve("sin(pi / 2)") == pytest.approx(1)
    assert solve("cos(pi / 2)") == pytest.approx(0)

    assert solve("asin(sin(0.83))") == pytest.approx(0.83)
    assert solve("acos(cos(0.37))") == pytest.approx(0.37)
    assert solve("atan(tan(0.5))") == pytest.approx(0.5)


def expect_value_error(formula):
    with pytest.raises(ValueError) as e_info:
        solve(formula)


def test_raise_errors():
    expect_value_error("")
    expect_value_error("hi")
    expect_value_error("1 -")
    expect_value_error("-")
    expect_value_error("3**3")
    expect_value_error("3 /// 3")
    expect_value_error("(1-3")
    expect_value_error("1-3)")


