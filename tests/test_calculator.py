# filepath: /workspaces/Trabalho-Breno/tests/test_calculator.py
"""
Testes unitários da lógica pura em server/calculator.py
"""
import pytest
from server import calculator

def test_add():
    assert calculator.add(2,3) == 5

def test_sub():
    assert calculator.sub(5,2) == 3

def test_mul():
    assert calculator.mul(4,3) == 12

def test_div():
    assert calculator.div(6,3) == 2

def test_division_by_zero():
    with pytest.raises(ValueError):
        calculator.div(1,0)
